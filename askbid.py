import pandas as pd
import asyncio
import ccxt.async_support as ccxt  # noqa: E402

async def test(name_of_exchange, symbol):

    exchange = ccxt.name_of_exchange({
        'enableRateLimit': True,  # required accoding to the Manual
    })

    try:
        orderbook = await exchange.fetch_order_book(symbol)
        await exchange.close()
        return orderbook
    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        raise e
    
def askbid(name_of_exchange,symbol):
    orderbook = asyncio.get_event_loop().run_until_complete(test(name_of_exchange,symbol))
    df = pd.DataFrame(orderbook, columns = ['asks','bids'])
    df1 = pd.DataFrame()
    df1[['asks','asks q']] = pd.DataFrame(df.asks.tolist(), index= df.index)
    df1[['bids','bids q']] = pd.DataFrame(df.bids.tolist(), index= df.index)
    askbid = df1[['asks','bids']].iloc[0]
    return askbid
