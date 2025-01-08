from logger import Logger
from models.entity.candle_data import CandleData


class CandleDataRepository:
    def __init__(self, connection):
        self.connection  = connection
        self.logger = Logger().get_logger(__class__.__name__)

    def init(self):
        try:
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
        except Exception as e:
            self.logger.warn(e)

    def save(self, candle_data: CandleData):
        try:
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
        except Exception as e:
            self.logger.warn(e)