# -*- coding: utf-8 -*-
import exchange
import mapper
import utils
from constant import RSI, MACD, TimeFrame, Stage
from dto import EMADto
from concurrent.futures import ThreadPoolExecutor
from logger import LoggerFactory

logger = LoggerFactory().get_logger("trade", "UpbitTrading")

def calculate_profit(ticker, curr_price):
    orders = mapper.get_buy_order(ticker)
    buy_price = float(orders.iloc[-1]["price"])
    return ((curr_price - buy_price) / buy_price) * 100.0

def execute(ticker, timeframe: TimeFrame):
    info = {}
    data = utils.get_data(ticker, timeframe, 5, 8, 13)
    stage = EMADto.get_stage(data)
    rsi = data[RSI.LONG].iloc[-1]
    balance = exchange.get_balance(ticker)

    if balance == 0:
        short_bullish = data[MACD.SHORT_BULLISH].iloc[-2:].isin([True]).any()
        long_bullish = data[MACD.LONG_BULLISH].iloc[-2:].isin([True]).any()
        if (short_bullish or long_bullish) and rsi <= 45 and stage in [Stage.STABLE_DECREASE, Stage.END_OF_DECREASE, Stage.START_OF_INCREASE]:
            mapper.insert_order(ticker, exchange.get_current_price(ticker), "bid")
            exchange.create_buy_order(ticker, 20000)
        info["data"] = f"[MACD: 1020 {short_bullish} | 1326 {long_bullish} | RSI: {rsi}]"
    else:
        profit = calculate_profit(ticker, float(data["close"].iloc[-1]))
        if profit > 0.1:
            mapper.insert_order(ticker, exchange.get_current_price(ticker), "ask")
            exchange.create_sell_order(ticker, balance)
        info["profit"] = profit
    info["info"] = f"[Ticker: {ticker} | Stage: {stage}]"
    return info

def loop(tickers, timeframe, workers=3):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(execute, ticker, timeframe) for ticker in tickers]
        result = [f.result() for f in futures]
        logger.info(result)

