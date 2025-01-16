import os
import unittest

import pyupbit
import requests
from dotenv import load_dotenv
from pyupbit import Upbit

from logger import Logger

load_dotenv()

class UpbitModuleTest(unittest.TestCase):
    def setUp(self):
        self.Upbit = Upbit(os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY"))
        self.logger = Logger().get_logger(__class__.__name__)

    def test_get_currencies(self):
        currencies = self.Upbit.get_balances()
        self.logger.debug(currencies.__len__())
        self.logger.info(len(currencies))

    def test_get_tickers(self):
        tickers = pyupbit.get_tickers(fiat="KRW")
        self.logger.info(tickers)

    def test_get_current_price(self):
        server_url = "https://api.upbit.com"
        params = {"markets": "KRW-AAVE"}
        res = requests.get(server_url + "/v1/ticker", params=params)
        self.logger.info(res.json()[0]['trade_price'])

    def test_get_avg_buy_price(self):
        a = self.Upbit.get_avg_buy_price("KRW-AAVE")
        self.logger.info(a)