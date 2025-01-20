import os
import uuid
from typing import Optional
import jwt
import pyupbit
import requests
from dotenv import load_dotenv
from pyupbit import Upbit

from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from models.dto.order_request_dto import OrderRequestDto

load_dotenv()

class UpbitModule:
    def __init__(self):
        self.access_key = os.getenv("UPBIT_ACCESS_KEY")
        self.secret_key = os.getenv("UPBIT_SECRET_KEY")
        self.Upbit = Upbit(self.access_key, self.secret_key)
        self.logger = Logger().get_logger(__class__.__name__)

    def get_candles_data(self, candle_request_dto: CandleRequestDto):
        if candle_request_dto:
            return pyupbit.get_ohlcv(
                ticker=candle_request_dto.ticker,
                count=candle_request_dto.count,
                interval=candle_request_dto.interval,
            )
        else:
            self.logger.warning("CandleRequestDto is Empty")

    def sell_market_order(self, order_request_dto: OrderRequestDto):
        if order_request_dto is not None:
            if order_request_dto.volume is None:
                return self.Upbit.sell_market_order(
                    ticker=order_request_dto.ticker,
                    volume=self.Upbit.get_balance(ticker=order_request_dto.ticker),
                )
            else:
                return self.Upbit.sell_market_order(
                    ticker=order_request_dto.ticker,
                    volume=order_request_dto.volume,
                )
        else:
            self.logger.warning("OrderRequestDto is Empty")

    def buy_market_order(self, order_request_dto: OrderRequestDto):
        if order_request_dto:
            return self.Upbit.buy_market_order(
                ticker=order_request_dto.ticker,
                price=order_request_dto.price,
            )
        else:
            self.logger.warning("OrderRequestDto is Empty")

    def get_currencies(self)->list:
        server_url = "https://api.upbit.com"
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(payload, self.secret_key)
        authorization = 'Bearer {}'.format(jwt_token)
        headers = { 'Authorization': authorization }
        res = requests.get(server_url + '/v1/accounts', headers=headers)
        if res.status_code == 200:
            return res.json()
        else:
            return self.Upbit.get_balances()

    def get_balance(self, ticker: str) -> Optional[float]:
        try:
            return self.Upbit.get_balance(ticker)
        except Exception as e:
            self.logger.error(e)
            currencies = self.get_currencies()
            format_ticker = ticker.replace("KRW-", "")
            for c in currencies:
                if c["currency"] == format_ticker:
                    return float(c["balance"])
            return None

    def get_current_price(self, ticker)-> Optional[float]:
        try :
            return pyupbit.get_current_price(ticker)
        except (KeyError, TypeError) as e:
            self.logger.error(e)
            self.logger.debug("Retrying...")
            server_url = "https://api.upbit.com"
            params = { "markets": ticker}
            res = requests.get(server_url + "/v1/ticker", params=params)
            if res.status_code == 200:
                return res.json()[0]['trade_price']
            else:
                return None

    def get_avg_buy_price(self, ticker: str)->Optional[float]:
        try:
            return self.Upbit.get_avg_buy_price(ticker)
        except Exception as e:
            self.logger.error(e)
            currencies = self.get_currencies()
            format_ticker = ticker.replace("KRW-", "")
            for c in currencies:
                if c["currency"] == format_ticker:
                    return float(c["avg_buy_price"])
            return None


    def get_profit(self, ticker)-> Optional[float]:
        current_price = self.get_current_price(ticker)
        avg_buy_price = self.get_avg_buy_price(ticker)
        if current_price and avg_buy_price:
            return (current_price - avg_buy_price) / avg_buy_price * 100.0
        else:
            return None