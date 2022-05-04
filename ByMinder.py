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
proxies = ['']

exchanges = {}
for id in ids:  # load all markets from all exchange exchanges

    # instantiate the exchange by id
    exchange = getattr(ccxt, id)()

    # save it in a dictionary under its id for future use

    exchanges[id] = exchange

    # load all markets from the exchange
    markets = exchange.load_markets()

    # basic round-robin proxy scheduler
    currentProxy = -1
    maxRetries = len(proxies)

    for numRetries in range(0, maxRetries):

        # try proxies in round-robin fashion
        currentProxy = (currentProxy + 1) % len(proxies)

        try:  # try to load exchange markets using current proxy

            exchange.proxy = proxies[currentProxy]
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
    dfA = pd.DataFrame(dfA)
    dfB = pd.DataFrame(dfB)
    for symbol in allSymbols:
    
        if symbol in exchanges[id].symbols:
            dfA = pd.concat(symbol)
            dfB = pd.concat(symbol)
        else:
            dfA.append('')
            dfB.append('')
    
    df[['{}asks'.format(id),'{}bids'.format(id)]] = pd.concat([[dfA,dfB]],axis=1)
    dfA = []
    dfB = []

pd.set_option('display.max_rows', df.shape[0]+1)
print(df)

