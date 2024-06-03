import os
import json
import time
from datetime import datetime
from sqlalchemy import create_engine, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from models import *

import requests
import numpy as np

from flask import Flask, jsonify
from flask_cors import CORS

import pysnowball as ball

ball.set_token("xq_a_token=a6d94c522a38e130310a73b9b6cf97666efeedb2")

app = Flask(__name__)
CORS(app)  # 启用CORS

dirname = os.path.dirname((os.path.abspath(__file__)))
engine = create_engine(f'sqlite:///{dirname}/../data/stock.db', echo=True)

session = Session(engine)


@app.route('/api/set/token/<token>')
def set_token(token):
    ball.set_token('xq_a_token=' + token)
    return jsonify({
        'code': 0,
        'message': 'Token set successfully'
    })

@app.route('/api/get/token')
def get_token():
    return jsonify({
        'code': 0,
        'token': ball.get_token()
    })

@app.route('/api/stock/tag/<symbol>/<tag>')
def stock_set_tag(symbol, tag):
    session.add(StockTag( tag=tag, symbol=symbol))
    session.commit()
    return jsonify({
        'code': 0
    })


@app.route('/api/stock/favorite/<symbol>')
def favorite_stock(symbol):
    favorite = session.query(FavoriteStock).filter(FavoriteStock.symbol == symbol).first()
    if favorite:
        return jsonify({
            'code': 0
        })

    stock = session.query(Stock).filter(Stock.symbol == symbol).first()
    session.add(FavoriteStock(symbol=symbol, name=stock.name, create_time=datetime.now()))
    session.commit()
    return jsonify({
        'code': 0
    })

@app.route('/api/stock/unfavorite/<symbol>')
def unfavorite_stock(symbol):
    stock = session.query(FavoriteStock).filter(FavoriteStock.symbol == symbol).first()
    app.logger.info(stock)
    if stock is None:
        return jsonify({
            'code': 0
        })
    else:
        session.delete(stock)
        session.commit()

    return jsonify({
        'code': 0
    })

@app.route('/api/stock/favorite')
def get_favorite_stock():
    stocks = session.query(FavoriteStock).order_by(FavoriteStock.create_time.desc()).all()
    data = []
    for stock in stocks:
        tags = session.query(StockTag).filter(StockTag.symbol == stock.symbol).all()
        data_tags = [tag.tag for tag in tags]
        data.append({
            'symbol': stock.symbol,
            'name'  : stock.name,
            'tags'  : data_tags,
            'favorite': 1 
        })
    ret = {
        'code': 0,
        'data': data
    }
    return jsonify(ret)

@app.route('/api/stock/tag/<symbol>')
def get_stock_tag(symbol):
    tags = session.query(StockTag).filter(StockTag.symbol == symbol).all()
    data = []
    for tag in tags:
        data.append({
            'tag': tag.tag,
            'symbol': tag.symbol
        })
    ret = {
        'code': 0,
        'data': data
    }
    return jsonify(ret) 


@app.route('/api/last/stock')
def selectLastStock():
    last_stock = session.query(RiseStock).order_by(RiseStock.date.desc()).first()
    stocks = session.query(RiseStock).filter(RiseStock.date == last_stock.date).all()
    favorite_stocks = session.query(FavoriteStock).all()
    favorite_data = [stock.symbol for stock in favorite_stocks]

    data = []
    for stock in stocks:
        tags = session.query(StockTag).filter(StockTag.symbol == stock.symbol).all()
        data_tags = [tag.tag for tag in tags]

        data.append({
            'symbol'   : stock.symbol,
            'name'     : stock.name,
            'tags'     : data_tags,
            'favorite' : 0 if stock.symbol not in favorite_data else 1
        })
    ret = {
        'code': 0,
        'data': data
    }
    return jsonify(ret)

# 计算近三十个交易日的波动
def std_third(kline_data):
    today = datetime.timestamp(datetime.now()) * 1000 - 30 * 24 * 60 * 60 * 1000

    price_data = []
    for item in kline_data:
        data = json.loads(item.data)
        if data[0] < today:
            continue

        price_data.append(data[5])
    
    # 计算30日数据方差
    variance = np.var(price_data)
    app.logger.info(f'kline_data: {variance}')

    return variance


@app.route('/api/stock/solve/zan')
def selectZanStock():
    # 获取当前日期
    today = datetime.now().date()

    # 将时间设置为0点0分0秒
    min_night = datetime.combine(today, datetime.min.time())

    # 转换为时间戳
    min_today_timestamp = int(time.mktime(min_night.timetuple()))

    last_stock = session.query(RiseStock).order_by(RiseStock.date.desc()).first()
    stocks = session.query(RiseStock).filter(RiseStock.date == last_stock.date).all()
    

    # last_stock_list = session.query(StockZan).filter(StockZan.create_time > min_today_timestamp).all()
    data = []
    for stock in stocks:
        tags = session.query(StockTag).filter(StockTag.symbol == stock.symbol).all()
        kline_data = session.query(KLine).filter(KLine.symbol == stock.symbol).all()
        app.logger.info(f'kline_data: {kline_data[0]}')
        variance = std_third(kline_data)

        data_tags = [tag.tag for tag in tags]
        data.append({
            'symbol'   : stock.symbol,
            'name'     : stock.name,
            'tags'     : data_tags,
            'favorite' : 0,
            'variance' : "{:.2f}".format(variance)
        })
    ret = {
        'code': 0,
        'data': data
    }
    return jsonify(ret)


def get_stock_data(page):
    # app.logger.info(f'page: {page}')
    data = requests.get(f"https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page={page}&size=90&order=desc&order_by=percent&market=CN&type=sh_sz",
                headers={
                    "Cookie": ball.get_token(),
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
                })
    
    return data

def get_all_stock_list():
    db_stocks = session.query(Stock).all()
    all_stocks = []
    for stock in db_stocks:
        all_stocks.append(stock.symbol)

    return all_stocks

# 今日上涨的股票
@app.route('/api/stock/today/down')
def rise():
    '''
    获取今日上涨的股票，每页90条，获取2页
    '''
    all_stocks = get_all_stock_list()

    favorite_stocks = session.query(FavoriteStock).all()
    favorite_data = [stock.symbol for stock in favorite_stocks]

    # 获取当前日期
    today = datetime.now().date()

    # 将时间设置为0点0分0秒
    min_night = datetime.combine(today, datetime.min.time())

    # 转换为时间戳
    min_today_timestamp = int(time.mktime(min_night.timetuple()))

    insert_stocks = []
    insert_count = 0
    for page in range(1, 3):
        data = get_stock_data(page)
        stock_list = data.json()['data']['list']

        # 获取的股票数量
        insert_count += len(stock_list)

        rise_stocks = []
        for stock in stock_list:
            symbol = stock['symbol']
            if symbol not in all_stocks:
                insert_stocks.append({
                    'symbol': symbol,
                    'name'  : stock['name']
                })
            
            # 不关注ST股票
            if 'ST' in stock['name']:
                continue

            rise_stocks.append({
                'symbol': symbol,
                'name'  : stock['name'],
                'time'  : min_today_timestamp,
                'date'  : today.strftime("%Y-%m-%d"),
                'favorite' : 0 if symbol not in favorite_data else 1
            })
            
        session.bulk_insert_mappings(RiseStock, rise_stocks)
        session.commit()
    
    # 如果已知列表中没有今天的股票，更新股票列表
    if len(insert_stocks) >0:
        session.bulk_insert_mappings(Stock, insert_stocks)
        session.commit()

    ret = {
        'code': 0,
        'add_count': len(insert_stocks),
        'rise_count': insert_count
    }

    return ret

@app.route('/api/kline/<symbol>')
def get_kline(symbol):
    klines = session.query(KLine).filter(KLine.symbol == symbol).all()
    data = []
    for line in klines:
        data.append(json.loads(line.data))

    ret = {
        'code'  : 0,
        'symbol': symbol,
        'data'  : data
    }
    return jsonify(ret)


@app.route('/api/stock/search/<symbol>')
def stock_search(symbol):
    last_kline = session.query(KLine).filter(KLine.symbol == symbol).order_by(KLine.timestamp.desc()).all()
    quote_detail= ball.quote_detail(symbol)
    app.logger.info(quote_detail)

    data = []
    if len(last_kline) > 0:
        for line in last_kline:
            data.append(json.loads(line.data))

        ret = {
            'code'  : 0,
            'symbol': symbol,
            'data'  : {
                "symbol": symbol,
                "name"  : quote_detail['data']['quote']['name'],
                "favorite": 0
            }
        }
        return jsonify(ret)
    
    
    stock = None
    if quote_detail:
        name = quote_detail['data']['quote']['name']
        app.logger.info(quote_detail)
        stock = Stock(
            symbol = symbol,
            name   = name,
        )
        session.add(stock)
        session.commit()
    
    last_timestamp = data[0] if data else 0
    app.logger.info(last_timestamp)
    
    new_kline = ball.kline(symbol)
    if new_kline:
        if len(data) == 0:
            for row in new_kline['data']['item']:
                timestamp = row[0]
                k_data = json.dumps(row)
                kline  = KLine(timestamp = timestamp, symbol = symbol, data = k_data)
                session.add(kline)
                session.commit()
        else:
            for row in new_kline['data']['item'][-10:]:
                timestamp = row[0]
                # 如果时间戳小于上次的时间戳，则跳过
                if timestamp <= last_timestamp:
                    continue
                else:
                    app.logger.info("add new kline", timestamp)
                    k_data = json.dumps(row)
                    kline  = KLine(timestamp = timestamp, symbol = symbol, data = k_data)
                    session.add(kline)
                    session.commit()

    ret = {
        'code'  : 0,
        'data'  : {
            "symbol": stock.symbol,
            "name": stock.name,
        }
    }
    return jsonify(ret)

@app.route('/api/fetch/kline/<symbol>')
def fetch_kline(symbol):
    last_kline = session.query(KLine).filter(KLine.symbol == symbol).order_by(KLine.timestamp.desc()).limit(1).all()
    data = None
    
    app.logger.info(last_kline)
    for stock in last_kline:
        data = json.loads(stock.data)

    app.logger.info(data)
    last_timestamp = data[0] if data else 0
    app.logger.info(last_timestamp)

    new_kline = ball.kline(symbol)
    if new_kline:
        if data is None:
            for row in new_kline['data']['item']:
                timestamp = row[0]
                k_data = json.dumps(row)
                kline  = KLine(timestamp = timestamp, symbol = symbol, data = k_data)
                session.add(kline)
                session.commit()
        else:
            n_klines = new_kline['data']['item'][-10:]
            kline = n_klines[-1]
            app.logger.info(kline)
            stmt = delete(KLine).where(KLine.timestamp > kline[0]).where(KLine.symbol == symbol)
            
            app.logger.info(stmt)

            for row in n_klines:
                timestamp = row[0]
                # 如果时间戳小于上次的时间戳，则跳过
                if timestamp <= last_timestamp:
                    continue
                else:
                    app.logger.info("add new kline", timestamp)
                    k_data = json.dumps(row)
                    kline  = KLine(timestamp = timestamp, symbol = symbol, data = k_data)
                    session.add(kline)
                    session.commit()

    return jsonify({"data": {"code": 0}})

if __name__ == '__main__':
    app.run(debug=True)