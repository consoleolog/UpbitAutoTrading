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
        try:
            return pyupbit.get_ohlcv(
                ticker=candle_request_dto.ticker,
                count=candle_request_dto.count,
                interval=candle_request_dto.interval,
                to=candle_request_dto.to,
            )
        except Exception as e:
            self.logger.error(e)

    def sell_market_order(self, order_request_dto: OrderRequestDto):
        try:
            return self.Upbit.sell_market_order(
                ticker=order_request_dto.ticker,
                volume=order_request_dto.volume,
            )
        except Exception as e:
            self.logger.error(e)

    def buy_market_order(self, order_request_dto: OrderRequestDto):
        try:
            return self.Upbit.buy_market_order(
                ticker=order_request_dto.ticker,
                price=order_request_dto.price,
            )
        except Exception as e:
            self.logger.error(e)


    def get_currencies(self):
        try:
            return self.Upbit.get_balances()
        except Exception as e:
            self.logger.warn(e)
    def get_balance(self, ticker):
        try:
            return self.Upbit.get_balance(ticker)
        except Exception as e:
            self.logger.error(e)
    def get_current_price(self, ticker):
        try:
            return pyupbit.get_current_price(ticker)
        except Exception as e:
            self.logger.error(e)

    def get_profit(self, ticker):
        try:
            currencies = self.get_currencies()
            for c in currencies:
                if isinstance(c, dict):
                    if c['currency'] == ticker.replace("KRW-", ""):
                        current_price = self.get_current_price(ticker=ticker)
                        return (current_price - float(c['avg_buy_price'])) / float(c['avg_buy_price']) * 100.0
                else:
                    self.logger.error(f"Unexpected type for 'c': {type(c)}. Expected dict.")
        except TypeError as e:
            self.logger.error(f"TypeError occurred for ticker {ticker}: {str(e)}. Retrying...")
            time.sleep(2)
            return self.get_profit(ticker)
        except Exception as e:
            self.logger.error(f"Error occurred for ticker {ticker}: {str(e)}")
        finally:
            return self.get_profit(ticker)