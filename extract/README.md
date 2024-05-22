获取股票数据

```
python install pysnowball

pip install sqlalchemy
```

依赖三个接口

* K线
https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SH601127&begin=1715665920106&period=day&type=before&count=-103&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance

```
"column": [
    "timestamp",
    "volume",
    "open",
    "high",
    "low",
    "close",
    "chg",
    "percent",
    "turnoverrate",
    "amount",
    "volume_post",
    "amount_post",
    "pe",
    "pb",
    "ps",
    "pcf",
    "market_capital",
    "balance",
    "hold_volume_cn",
    "hold_ratio_cn",
    "net_volume_cn",
    "hold_volume_hk",
    "hold_ratio_hk",
    "net_volume_hk"
],
```

* 涨跌幅版
https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=1&size=100&order=desc&order_by=percent&market=CN&type=sha

* 实时价格
https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=SH601127


雪球没有公开的，实用的接口 token 需要从浏览器中获取
受限的请求头需要添加 Cookie: xq_a_token=a239e31d3b1c46e724f672dccaeebd5941800ac2
公开的接口可以直接访问。

这里有一个文档：https://blog.crackcreed.com/diy-xue-qiu-app-shu-ju-api/
