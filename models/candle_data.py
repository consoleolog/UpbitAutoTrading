from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Float

from models.candles_dto import ResponseCandlesDto
from server import Base


class CandleData(Base):
    __tablename__ = 'candle_data'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow())
    close = Column(Float, nullable=False)
    ema_short = Column(Float, nullable=False)
    ema_middle = Column(Float, nullable=False)
    ema_long = Column(Float, nullable=False)
    macd_upper = Column(Float, nullable=False)
    macd_middle = Column(Float, nullable=False)
    macd_lower = Column(Float, nullable=False)

