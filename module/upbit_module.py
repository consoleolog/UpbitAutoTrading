import os
import time

import pyupbit
from dotenv import load_dotenv
from pyupbit import Upbit

from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from models.dto.order_request_dto import OrderRequestDto

load_dotenv()

class UpbitModule:
    def __init__(self):
        self.Upbit = Upbit(os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY"))
        self.logger = Logger().get_logger(__class__.__name__)

    def get_candles_data(self, candle_request_dto: CandleRequestDto):
        return pyupbit.get_ohlcv(
            ticker=candle_request_dto.ticker,
            count=candle_request_dto.count,
            interval=candle_request_dto.interval,
            to=candle_request_dto.to,
        )


    def sell_market_order(self, order_request_dto: OrderRequestDto):
        return self.Upbit.sell_market_order(
            ticker=order_request_dto.ticker,
            volume=order_request_dto.volume,
        )

    def buy_market_order(self, order_request_dto: OrderRequestDto):
        return self.Upbit.buy_market_order(
            ticker=order_request_dto.ticker,
            price=order_request_dto.price,
        )


    def get_currencies(self):
        return self.Upbit.get_balances()

    def get_balance(self, ticker):
        return self.Upbit.get_balance(ticker)

    def get_profit(self, ticker):
        try:
            current_price = pyupbit.get_current_price(ticker)
            currencies = self.get_currencies()
            for c in currencies:
                if c['currency'] == ticker.replace("KRW-", ""):
                    return (current_price - float(c['avg_buy_price'])) / float(c['avg_buy_price']) * 100.0
        except TypeError:
            return self.get_profit(ticker)
