import unittest
from typing import List

from database import connection
from logger import Logger
from models.entity.candle_data import CandleData


class CandleDataRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.connection = connection
        self.logger = Logger().get_logger(__class__.__name__)

    def tearDown(self):
        self.connection = None


    def test_get_all_by_ticker(self):
        ticker = "KRW-BTC"
        interval = "minutes30"
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT C.CANDLE_ID,
                   C.DATE,
                   C.TICKER,
                   C.CLOSE,
                   C.EMA_SHORT,
                   C.EMA_MIDDLE,
                   C.EMA_LONG,
                   C.STAGE,
                   C.MACD_UPPER,
                   C.MACD_MIDDLE,
                   C.MACD_LOWER,
                   C.INTERVAL
            FROM CANDLE_DATA C 
            WHERE TICKER = %s
            AND INTERVAL = %s
            ORDER BY DATE DESC """,
            (ticker, interval))
            result: List[CandleData] = cursor.fetchall()
            self.logger.debug(result)
            self.logger.debug(type(result))
            self.logger.debug()


