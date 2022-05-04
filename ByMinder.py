import ccxt
import pandas as pd
import numpy as np
import time
import sys

ids = ['ftx'] #,'ascendex','mexc','gateio','huobi'

def dump(*args):
    print(' '.join([str(arg) for arg in args]))
    
def test(id, symbol):
    orderbook = id.fetch_order_book(symbol)
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
    ask = df1.iat[0,0]
    bid = df1.iat[0,1]
    return ask, bid

exchanges = {}
for id in ids:
    exchange = getattr(ccxt, id)()
    exchanges[id] = exchange
    markets = exchange.load_markets()
    try:
        exchange.load_markets()
    except ccxt.DDoSProtection as e:
        dump(type(e).__name__, e.args)
    except ccxt.RequestTimeout as e:
        dump(type(e).__name__, e.args)
    except ccxt.AuthenticationError as e:
        dump(type(e).__name__, e.args)
    except ccxt.ExchangeNotAvailable as e:
        dump(type(e).__name__, e.args)
    except ccxt.ExchangeError as e:
        dump(type(e).__name__, e.args)
    except ccxt.NetworkError as e:
        dump(type(e).__name__, e.args)
    except Exception as e:  # reraise all other exceptions
        raise
    dump((id), 'loaded', str(len(exchange.symbols)), 'markets')
dump('Loaded all markets')

allSymbols = [symbol for id in ids for symbol in exchanges[id].symbols]
df = pd.DataFrame(allSymbols)
dfA = []
dfB = []
for id in ids:
    for symbol in allSymbols:
        if symbol in exchanges[id].symbols:
            ask, bid = askbid(exchanges[id], symbol)
            dfA.append(ask)
            dfB.append(bid)
        else:
            dfA.append('')
            dfB.append('')
            
    dfA = pd.DataFrame(dfA)
    dfB = pd.DataFrame(dfB)
    df['{} ask'.format(id)] = pd.concat([dfA],axis=1)
    df['{} bid'.format(id)] = pd.concat([dfB],axis=1)
    dfA = []
    dfB = []

pd.set_option('display.max_rows', df.shape[0]+1)
print(df)

# for id in ids:
#     for symbol in allSymbols:
#         ask, bid = askbid(exchanges[id], symbol)
#         dfA.append(ask)
#         dfB.append(bid)            
            
#     dfA = pd.DataFrame(dfA)
#     dfB = pd.DataFrame(dfB)
#     df['{} ask'.format(id)] = pd.concat([dfA],axis=1)
#     df['{} bid'.format(id)] = pd.concat([dfB],axis=1)

