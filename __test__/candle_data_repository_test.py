import unittest

import pandas as pd

from database import connection
from logger import Logger
from models.type.interval_type import IntervalType
from models.type.unit_type import UnitType


class CandleDataRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.connection = connection
        self.logger = Logger().get_logger(__class__.__name__)

    def tearDown(self):
        self.connection = None


    def test_get_all_by_ticker(self):
        ticker = "KRW-BTC"
        interval = IntervalType(UnitType.MINUTE_5).MINUTE
        sql = """
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
            
        """
        data = pd.read_sql(sql, self.connection, params=(ticker, interval))
        self.logger.debug(data)




