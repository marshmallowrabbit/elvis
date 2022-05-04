import pandas as pd
import asyncio
import ccxt

def test(id, symbol):
    orderbook = id.fetch_order_book(symbol)
    # exchange.close()
    return orderbook
    
def askbid(id,symbol):
    orderbook = test(id,symbol)
    df = pd.DataFrame(orderbook)
    del df['nonce']
    del df['timestamp']
    del df['datetime']
    del df['symbol']
    df1 = pd.DataFrame()
    df1[['ask','asks q']] = pd.DataFrame(df.asks.tolist(),index=df.index)
    df1[['bid','bids q']] = pd.DataFrame(df.bids.tolist(),index=df.index)
    del df1['asks q']
    del df1['bids q']
    askbid = df1.iat[0,0]
    return askbid
id = ccxt.ftx()
symbol = 'BTC/USDT'
print(askbid(id,symbol))
