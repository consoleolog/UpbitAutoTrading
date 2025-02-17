# -*- coding: utf-8 -*-
import os
from pprint import pprint

import ccxt
import ccxt.pro as ccxtpro
import pandas as pd
from dotenv import load_dotenv
from constant import TimeFrame
from dto import TickerInfo

load_dotenv()
accessKey = os.getenv("ACCESS_KEY")
secretKey = os.getenv("SECRET_KEY")
ex = getattr(ccxt, os.getenv("ID"))({
    'apiKey': accessKey,
    'secret': secretKey,
    'enableRateLimit': True,
})

def get_ticker_info(ticker:str) -> TickerInfo:
    tickers = ex.fetch_tickers()
    info = tickers[ticker]
    return TickerInfo.from_dict(info)

def get_krw() -> float:
    balances = ex.fetch_balance()
    krw = balances["KRW"]
    return float(krw["free"])

async def create_buy_order(ticker:str, amount: float):
    ex.options['createMarketBuyOrderRequiresPrice'] = False
    return ex.create_market_buy_order(
        symbol=ticker,
        amount=amount
    )

async def create_sell_order(ticker:str, amount: float):
    return ex.create_market_sell_order(
        symbol=ticker,
        amount=amount
    )

def get_current_price(ticker:str)->float:
    ticker_info = get_ticker_info(ticker)
    return float(ticker_info.close)

def get_avg_buy_price(ticker:str)->float:
    ticker_info = get_ticker_info(ticker)
    return float(ticker_info.average)

def get_profit(ticker:str)->float:
    current_price = get_current_price(ticker)
    avg_buy_price = get_avg_buy_price(ticker)
    return (current_price - avg_buy_price) / avg_buy_price * 100.0

def get_balance(ticker: str) -> float:
    format_ticker = ticker.replace("/KRW", "")
    balances = ex.fetch_balance()
    balance = balances[format_ticker]
    return float(balance['free'])

def get_candles(ticker, timeframe: TimeFrame) -> pd.DataFrame:
    ohlcv = ex.fetch_ohlcv(symbol=ticker, timeframe=str(timeframe))
    df = pd.DataFrame(ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    pd_ts = pd.to_datetime(df['datetime'], utc=True, unit='ms')
    pd_ts = pd_ts.dt.tz_convert("Asia/Seoul")
    pd_ts = pd_ts.dt.tz_localize(None)
    df.set_index(pd_ts, inplace=True)
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    return df


