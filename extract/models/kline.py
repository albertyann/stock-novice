import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class KLine(Base):
    __tablename__ = 'klines'
    id     = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Integer)
    symbol = Column(String(32))
    data   = Column(String(3000))

    def __repr__(self):
        return "<KLine(timestamp='%s', symbol='%s', data='%s')>" % (self.timestamp, self.symbol, self.data)
    
class Stock(Base):
    __tablename__ = 'stocks'
    id     = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(32))
    name   = Column(String(32))

    def __repr__(self):
        return "<Stock(symbol='%s', name='%s')>" % (self.symbol, self.name)
    
class StockTag(Base):
    __tablename__ = 'stock_tag'
    id     = Column(Integer, primary_key=True, autoincrement=True)
    tag    = Column(String(32))
    symbol = Column(String(32))

    def __repr__(self):
        return "<StockTag(tag='%s', symbol='%s')>" % (self.tag, self.symbol)
    
class FavoriteStock(Base):
    __tablename__ = 'favorite_stocks'
    id     = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(32))
    name    = Column(String(32))
    create_time = Column(DateTime)

    def __repr__(self):
        return "<FavoriteStock(symbol='%s', name='%s', create_time='%s')>" % (self.symbol, self.name, self.create_time)
    
class StockZan(Base):
    __tablename__ = 'stock_zan'
    id          = Column(Integer, primary_key=True, autoincrement=True)
    symbol      = Column(String(32))
    name        = Column(String(32))
    create_time = Column(DateTime)

    def __repr__(self):
        return "<StockZan(name='%s', symbol='%s', create_time='%s')>" % (self.name, self.symbol, self.create_time)
    
class StockMain(Base):
    __tablename__ = 'stock_main'
    id          = Column(Integer, primary_key=True, autoincrement=True)
    symbol      = Column(String(32))
    name        = Column(String(32))
    create_time = Column(DateTime)

    def __repr__(self):
        return "<StockMain(name='%s', symbol='%s', create_time='%s')>" % (self.name, self.symbol, self.create_time)
    
class RiseStock(Base):
    __tablename__ = 'rise_stocks'
    id     = Column(Integer, primary_key=True, autoincrement=True)
    time   = Column(Integer)
    date   = Column(String(32))
    symbol = Column(String(32))
    name   = Column(String(32))

    def __repr__(self):
        return "<RiseStock(time='%s', date='%s', symbol='%s', name='%s')>" % (self.time, self.date, self.symbol, self.name)

dirname = os.path.dirname((os.path.abspath(__file__)))

engine = create_engine(f'sqlite:///{dirname}/../../data/stock.db', echo=True)

Base.metadata.create_all(engine, checkfirst = True)
