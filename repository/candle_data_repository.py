import pandas as pd

from database import engine
from logger import Logger
from models.entity.candle_data import CandleData
from models.type.interval_type import IntervalType


class CandleDataRepository:
    def __init__(self, connection):
        self.connection  = connection
        self.logger = Logger().get_logger(__class__.__name__)

    def init(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS CANDLE_DATA(
                CANDLE_ID SERIAL PRIMARY KEY,
                DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                TICKER VARCHAR(20),
                CLOSE FLOAT,
                EMA_SHORT FLOAT,
                EMA_MIDDLE FLOAT,
                EMA_LONG FLOAT,
                STAGE INTEGER,
                MACD_UPPER FLOAT,
                MACD_MIDDLE FLOAT,
                MACD_LOWER FLOAT,
                INTERVAL VARCHAR(20)
            );
            """)
            self.connection.commit()

    def find_all_by_ticker_and_interval(self, ticker:str, interval: IntervalType):
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
        try:
            return pd.read_sql(sql, engine, params=(ticker, interval))
        except Exception:
            return pd.read_sql(sql, self.connection, params=(ticker, interval))

    def save(self, candle_data: CandleData):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO CANDLE_DATA(
                TICKER,
                CLOSE,
                EMA_SHORT,
                EMA_MIDDLE,
                EMA_LONG,
                STAGE,
                MACD_UPPER,
                MACD_MIDDLE,
                MACD_LOWER,
                INTERVAL 
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """, (
                candle_data.ticker,
                candle_data.close,
                candle_data.ema_short,
                candle_data.ema_middle,
                candle_data.ema_long,
                candle_data.stage,
                candle_data.macd_upper,
                candle_data.macd_middle,
                candle_data.macd_lower,
                candle_data.interval
            )
                           )
            self.connection.commit()
