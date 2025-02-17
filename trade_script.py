import asyncio
import platform

import ccxt.pro as ccxtpro
import exchange
import mapper
import utils
from constant import MACD, RSI, Stage, TimeFrame
from dto import TickerInfo, EMADto, OrderInfo

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def get_profit(order, curr_price):
    buy_price = float(order["price"])
    return (curr_price - buy_price) / buy_price * 100.0

async def loop(ex, ticker):
    while True:
        await watch_ticker(ex, ticker)


async def watch_ticker(ex, ticker):
    count = 0
    prev_price = 0
    prev = False
    while True:
        ticker_data = await ex.watch_ticker(symbol=ticker)
        if isinstance(ticker_data, dict) and 'symbol' in ticker_data:
            ticker_info = TickerInfo.from_dict(ticker_data)

            if not prev:
                prev_price = ticker_info.last
                prev = True
            else:
                try:
                    change_percentage = ((ticker_info.last - prev_price) / prev_price) * 100
                except ZeroDivisionError:
                    change_percentage = 0
                print(f"가격 변화율: {change_percentage:.2f}%")

                prev_price = ticker_info.last

            # try:
            #     balance = exchange.get_balance(ticker)
            # except KeyError:
            #     balance = 0
            # if balance == 0:
            #     data = utils.get_data(ticker, TimeFrame.MINUTE)
            #     stage = EMADto.get_stage(data)
            #     print(stage)
            #     rsi = data[RSI.LONG].iloc[-1]
            #     if rsi <= 40 and stage in [Stage.STABLE_DECREASE, Stage.END_OF_DECREASE, Stage.STABLE_INCREASE]:
            #         res = await exchange.create_buy_order(ticker, 8000)
            #         order_info = OrderInfo.from_buy(res["info"])
            #         await mapper.insert_order(order_info)
            # else:
            #     orders = mapper.get_buy_order(ticker)
            #     profit = get_profit(orders.iloc[-1], ticker_info.last)
            #     if profit > 0.1:
            #         res = await exchange.create_sell_order(ticker, balance)
            #         order_info = OrderInfo.from_sell(res["info"])
            #         await mapper.insert_order(order_info)

async def main():
    ex = ccxtpro.upbit()
    symbols = ['XRP/KRW']

    try:
        coros = [loop(ex, symbol) for symbol in symbols]
        await asyncio.gather(*coros)
    finally:
        await ex.close()

if __name__ == "__main__":
    asyncio.run(main())

