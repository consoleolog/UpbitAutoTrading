from datetime import datetime

from models.type.interval_type import IntervalType
from models.type.stage_type import StageType

class CandleData:
    def __init__(
            self,
            date: datetime = None,
            ticker: str = None,
            close: float = None,
            ema_short: float = None,
            ema_middle: float = None,
            ema_long: float = None,
            stage: StageType = None,
            macd_upper: float = None,
            macd_middle: float = None,
            macd_lower: float = None,
            interval: IntervalType = None
    ):
        self.date = date
        self.ticker = ticker
        self.close = close
        self.ema_short = ema_short
        self.ema_middle = ema_middle
        self.ema_long = ema_long
        self.stage = stage
        self.macd_upper = macd_upper
        self.macd_middle = macd_middle
        self.macd_lower = macd_lower
        self.interval = interval