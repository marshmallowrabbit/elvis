import ccxt
import pandas as pd
import numpy as np
import time
import sys

ids = ['ftx','binance'] #,'ascendex','mexc','gateio','huobi'

def dump(*args):
    print(' '.join([str(arg) for arg in args]))
    
def askbid(id,symbol):
    orderbook = id.fetch_order_book(symbol, limit = 1)
    s = pd.Series(orderbook)
    s = s[['asks','bids']]
    for a in s.asks:
        ask = a[0] 
    for b in s.bids:
        bid = b[0]
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
uniqueSymbols = list(set(allSymbols))
arbitrableSymbols = sorted([symbol for symbol in uniqueSymbols if allSymbols.count(symbol) > 1])

df = pd.DataFrame(arbitrableSymbols)
dfA = []
dfB = []
for id in ids:
    for symbol in arbitrableSymbols:
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


