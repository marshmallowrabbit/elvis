import ccxt
import pandas as pd
import numpy as np
import time
import sys

ids = ['ftx','binance'] #,'ascendex','mexc','gateio','huobi'

def dump(*args):
    print(' '.join([str(arg) for arg in args]))
    
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
    askbid = [df1.asks.iloc[0], df1.bids.iloc[0]]
    return askbid

proxies = [
    '',  # no proxy by default
    'https://crossorigin.me/',
    'https://cors-anywhere.herokuapp.com/',
]

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

# get all unique symbols
uniqueSymbols = list(set(allSymbols))

# filter out symbols that are not present on at least two exchanges
arbitrableSymbols = sorted([symbol for symbol in uniqueSymbols if allSymbols.count(symbol) > 1])

df = pd.DataFrame(arbitrableSymbols)
dfT = []
for id in ids:
    for symbol in arbitrableSymbols:
        if symbol in exchanges[id].symbols:
            dfT.append(askbid(exchanges[id],symbol))
        else:
            dfT.append('')
    dfT = pd.DataFrame(dfT)
    df[id] = pd.concat([dfT],axis=1)
    dfT = []

pd.set_option('display.max_rows', df.shape[0]+1)
print(df)
