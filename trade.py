# -*- coding: utf-8 -*-
import exchange
import utils
import mapper
from constant import RSI, MACD, TimeFrame, Stage
from dto import EMADto, OrderInfo
from concurrent.futures import ThreadPoolExecutor
from logger import LoggerFactory

logger = LoggerFactory().get_logger("trade", "UpbitTrading")

def execute(ticker, timeframe: TimeFrame):
    info = {}
    data = utils.get_data(ticker, timeframe)
    stage = EMADto.get_stage(data)
    rsi = data[RSI.LONG].iloc[-1]
    balance = exchange.get_balance(ticker)

    if balance == 0:
        bullish = data[MACD.SHORT_BULLISH].iloc[-2:].isin([True]).any()
        if bullish and rsi <= 43 and stage in [Stage.STABLE_DECREASE, Stage.END_OF_DECREASE, Stage.START_OF_INCREASE]:
            res = exchange.create_buy_order(ticker, 20000)
            order_info = OrderInfo.from_buy(res["info"])
            mapper.insert_order(order_info)
        info["data"] = f"[MACD: {bullish} | RSI: {rsi}]"
    else:
        orders = mapper.get_buy_order(ticker)
        profit = utils.get_profit(orders.iloc[-1], data["close"].iloc[-1])
        if profit >= 0.1:
            res = exchange.create_sell_order(ticker, balance)
            order_info = OrderInfo.from_sell(res["info"])
            mapper.insert_order(order_info)
        info["profit"] = f"[Profit: {profit}]"
    info["info"] = f"[Ticker: {ticker} | Stage: {stage}]"
    return info

def loop(tickers, timeframe, workers=3):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(execute, ticker, timeframe) for ticker in tickers]
        result = [f.result() for f in futures]
        logger.info(result)

