import pandas as pd
import asyncio
import ccxt

def test(exchange, symbol):
    
    temp_exchange = ccxt.exchange({'enableRateLimit': True,})
    orderbook = temp_exchange.fetch_order_book(symbol)
    # exchange.close()
    return orderbook
    
def askbid(exchange,symbol):
    orderbook = asyncio.get_event_loop().run_until_complete(test(exchange=exchange, symbol=symbol))
    df = pd.DataFrame(orderbook, columns = ['asks','bids'])
    df1 = pd.DataFrame()
    df1[['asks','asks q']] = pd.DataFrame(df.asks.tolist(), index= df.index)
    df1[['bids','bids q']] = pd.DataFrame(df.bids.tolist(), index= df.index)
    askbid = df1[['asks','bids']].iloc[0]
    return askbid
exchange = 'ftx'
symbol = 'BTC/USDT'
print(test(exchange,symbol),askbid(exchange,symbol))
