import os
import unittest
import uuid

import jwt
import pyupbit
import requests
from dotenv import load_dotenv
from pyupbit import Upbit

from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from models.type.interval_type import IntervalType
from models.type.unit_type import UnitType
from module.upbit_module import UpbitModule
from util import data_util


class UpbitModuleTest(unittest.TestCase):
    load_dotenv()

    def setUp(self):
        self.access_key = os.getenv("UPBIT_ACCESS_KEY")
        self.secret_key = os.getenv("UPBIT_SECRET_KEY")
        self.Upbit = Upbit(self.access_key, self.secret_key)
        self.logger = Logger().get_logger(__class__.__name__)

        self.upbit_module = UpbitModule()

    def test_get_candles_data(self):
        candle_request_dto = CandleRequestDto(ticker="KRW-AAVE", interval=IntervalType(UnitType.MINUTE_5).MINUTE)

        if not data_util.is_empty(candle_request_dto):
            data = pyupbit.get_ohlcv(
                ticker=candle_request_dto.ticker,
                count=candle_request_dto.count,
                interval=candle_request_dto.interval
            )
            self.logger.debug(data)
            self.logger.debug(data.iloc[-1])
    def test_get_currencies(self):
        server_url = "https://api.upbit.com"
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(payload, self.secret_key)
        authorization = 'Bearer {}'.format(jwt_token)
        headers = { 'Authorization': authorization }
        res = requests.get(server_url + '/v1/accounts', headers=headers)
        self.logger.debug(res.status_code)
        self.logger.debug(res.json())
        self.logger.debug(type(res.json()))

        for c in res.json():
            if c['currency'] != 'KRW':
                profit = self.upbit_module.get_profit(f"KRW-{c['currency']}")
                self.logger.debug(f"{c['currency']} - {profit}")
    def test_get_balances(self):
        balances = self.Upbit.get_balances()
        self.logger.debug(balances)
        self.logger.debug(type(balances))

    def test_get_current_price(self):
        ticker = "KRW-AAVE"
        try :
            current_price =  pyupbit.get_current_price(ticker)
            self.logger.debug(current_price)
            self.logger.debug(type(current_price))
        except (KeyError, TypeError) as e:
            self.logger.error(e)
            self.logger.debug("Retrying...")
            server_url = "https://api.upbit.com"
            params = { "markets": ticker}
            res = requests.get(server_url + "/v1/ticker", params=params)
            self.logger.debug(res.status_code)
            self.logger.error(res.json())
            current_price = res.json()[0]['trade_price']
            self.logger.info(current_price)
            self.logger.info(type(current_price))

    def test_get_balance(self):
        ticker = "KRW-ETH"
        try:
            balance = self.Upbit.get_balance(ticker)
            self.logger.debug(balance)
            self.logger.debug(type(balance))
        except Exception as e:
            self.logger.error(e)
            currencies = self.upbit_module.get_currencies()
            format_ticker = ticker.replace("KRW-", "")
            for c in currencies:
                if c["currency"] == format_ticker:
                     balance = float(c['balance'])
                     self.logger.debug(balance)
                     self.logger.debug(type(balance))
                     self.logger.debug(c["balance"])
                     self.logger.debug(type(c["balance"]))

    def test_get_avg_price(self):
        ticker = "KRW-ETH"
        try:
            avg_price = self.Upbit.get_avg_buy_price(ticker)
            self.logger.debug(avg_price)
            self.logger.debug(type(avg_price))
        except Exception as e:
            self.logger.error(e)
            currencies = self.upbit_module.get_currencies()
            format_ticker = ticker.replace("KRW-", "")
            for c in currencies:
                if c["currency"] == format_ticker:
                    avg_price = float(c['avg_buy_price'])
                    self.logger.debug(avg_price)
                    self.logger.debug(type(avg_price))

    def test_get_profit(self):
        ticker = "KRW-ETH"
        current_price = self.upbit_module.get_current_price(ticker)
        avg_buy_price = self.upbit_module.get_avg_buy_price(ticker)
        if not data_util.is_empty(current_price) and not data_util.is_empty(avg_buy_price):
            profit = (current_price - avg_buy_price) / avg_buy_price * 100.0
            self.logger.debug(profit)
            self.logger.debug(type(profit))