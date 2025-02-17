import asyncio
import platform

import ccxt.pro as ccxtpro
import exchange
import mapper
import utils
from constant import MACD, RSI, Stage, TimeFrame
from dto import TickerInfo, EMADto

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def main(ticker, timeframe):
    data = utils.get_data(ticker, timeframe)
    balance = exchange.get_balance(ticker)
    stage = EMADto.get_stage(data)

    if balance == 0:
        bullish = data[MACD.SHORT_BULLISH].iloc[-2:].isin([True]).any()
        rsi = data[RSI.LONG].iloc[-1]
        if bullish and rsi <= 40 and stage in [Stage.STABLE_DECREASE, Stage.END_OF_DECREASE, Stage.STABLE_INCREASE]:
            pass

def get_profit(order, curr_price):
    buy_price = float(order["price"])
    return (curr_price - buy_price) / buy_price * 100.0

async def loop(ex, ticker):
    while True:
        await watch_ticker(ex, ticker)


async def watch_ticker(ex, ticker):
    while True:
        ticker_data = await ex.watch_ticker(symbol=ticker)

        if isinstance(ticker_data, dict) and 'symbol' in ticker_data:
            ticker_info = TickerInfo.from_dict(ticker_data)
            orders = mapper.get_buy_order(ticker)
            profit = get_profit(orders.iloc[-1], ticker_info.last)


async def socket():
    ex = ccxtpro.upbit()
    symbols = ['BTC/KRW', 'ETH/KRW', 'XRP/KRW']

    try:
        coros = [loop(ex, symbol) for symbol in symbols]
        await asyncio.gather(*coros)
    finally:
        await ex.close()



asyncio.run(socket())

