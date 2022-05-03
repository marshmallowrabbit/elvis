import pandas as pd
import asyncio
import ccxt

def test(id, symbol):
    orderbook = id.fetch_order_book(symbol)
    # exchange.close()
    return orderbook
    
def askbid(id,symbol):
    orderbook = test(id,symbol)
    df = pd.DataFrame(orderbook, columns = ['asks','bids'])
    df1 = pd.DataFrame()
    df1[['asks','asks q']] = pd.DataFrame(df.asks.tolist(), index= df.index)
    df1[['bids','bids q']] = pd.DataFrame(df.bids.tolist(), index= df.index)
    askbid = df1[['asks','bids']].iloc[0]
    return askbid
id = ccxt.ftx()
symbol = 'BTC/USDT'
print(askbid(id,symbol))
