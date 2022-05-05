import pandas as pd
import asyncio
import ccxt

def askbid(id,symbol):
    orderbook = id.fetch_order_book(symbol, limit = 1)
    s = pd.Series(orderbook)
    s = s[['asks','bids']]
    for a in s.asks:
        ask = a[0] 
    for b in s.bids:
        bid = b[0]
    return ask, bid

id = ccxt.ftx()
symbol = 'BTC/USDT'
print(askbid(id,symbol))
