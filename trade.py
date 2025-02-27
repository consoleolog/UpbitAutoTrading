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
    status = mapper.get_status(ticker)
    buy_price = float(status["price"])
    return ((curr_price - buy_price) / buy_price) * 100.0

def update_status(ticker):
    status = mapper.get_status(ticker)
    if status["side"] == "bid":
        price = (float(status["price"]) + exchange.get_current_price(ticker)) / 2
        mapper.update_status(ticker, price, "bid")
    else:
        mapper.update_status(ticker, exchange.get_current_price(ticker), "bid")

def execute(ticker, timeframe: TimeFrame):
    info = {}
    data = utils.get_data(ticker, timeframe, 5, 8, 13)
    stage = EMADto.get_stage(data)
    rsi = data[RSI.LONG].iloc[-1]
    balance = exchange.get_balance(ticker)

    peekout = all([
        data[MACD.SHORT_HIST].iloc[-1] > data[MACD.SHORT_HIST].iloc[-7:].min(),
        data[MACD.MID_HIST].iloc[-1] > data[MACD.MID_HIST].iloc[-7:].min(),
        data[MACD.LONG_HIST].iloc[-1] > data[MACD.LONG_HIST].iloc[-7:].min()
    ])
    bullish = all([
        data[MACD.SHORT_BULLISH].iloc[-2:].isin([True]).any(),
        data[MACD.MID_BULLISH].iloc[-2:].isin([True]).any(),
        data[MACD.LONG_BULLISH].iloc[-2:].isin([True]).any(),
    ])
    if bullish and rsi <= 40 and stage in [Stage.STABLE_DECREASE, Stage.END_OF_DECREASE, Stage.START_OF_INCREASE]:
        update_status(ticker)
        exchange.create_buy_order(ticker, 20000)
    info["data"] = f"[MACD: {peekout} | RSI: {rsi}]"

    if balance != 0:
        profit = calculate_profit(ticker, exchange.get_current_price(ticker))
        if profit > 0.1 and stage in [Stage.STABLE_INCREASE, Stage.END_OF_INCREASE, Stage.START_OF_DECREASE]:
            mapper.update_status(ticker, exchange.get_current_price(ticker), "ask")
            exchange.create_sell_order(ticker, balance)
        info["profit"] = profit
    info["info"] = f"[Ticker: {ticker} | Stage: {stage}]"
    return info

def loop(tickers, timeframe, workers=3):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(execute, ticker, timeframe) for ticker in tickers]
        result = [f.result() for f in futures]
        logger.info(result)

