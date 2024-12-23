

class RequestCandlesDto:
    class Interval:
        SECOND = "seconds"
        MINUTE = "minutes"
        DAY = "days"
        MONTHS = "months"
        YEAR = "years"

    class Unit:
        MINUTE = 1
        MINUTE_3 = 3
        MINUTE_5 = 5
        MINUTE_10 = 10
        MINUTE_15 = 15
        HALF_HOUR = 30
        HOUR = 60
        HOUR_4 = 240

    def __init__(self):
        self.ticker = None
        self.interval = None
        self.count = None
        self.to = None
        self.unit = None

    def set_ticker(self, ticker: str = "KRW-BTC"):
        self.ticker = ticker
        return self

    def set_interval(self, interval: Interval = Interval.DAY):
        self.interval = interval
        return self

    def set_count(self, count: int = 200 ):
        self.count = count
        return self

    def set_to(self, to: float = None):
        self.to = to
        return self

    def set_unit(self, unit:Unit = Unit.MINUTE):
        self.unit = unit
        return self

    def build(self):
        if not self.ticker:
            raise ValueError("ticker is required")
        if not self.interval:
            raise ValueError("interval is required")
        if self.count is None:
            raise ValueError("count is required")
        if self.interval == RequestCandlesDto.Interval.MINUTE and not self.unit:
            raise ValueError("unit is required")
        return self

class ResponseCandlesDto:
    class Df:
        OPEN = "open"
        HIGH = "high"
        LOW = "low"
        CLOSE = "close"
        VOLUME = "volume"
        VALUE = "value"

    open: float
    high: float
    low: float
    close: float
    volume: float
    value: float

    def __init__(
            self,
            open,
            high,
            low,
            close,
            volume,
            value
    ):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.value = value

    @staticmethod
    def create_by_dict(candles_dict):
        return ResponseCandlesDto(
            open=candles_dict["open"],
            high=candles_dict["high"],
            low=candles_dict["low"],
            close=candles_dict["close"],
            volume=candles_dict["volume"],
            value=candles_dict["value"]
        )

    def __str__(self):
        return f"""
        ResponseCandlesDto(
            open={self.open},
            high={self.high},
            low={self.low},
            close={self.close},
            volume={self.volume},
            value={self.value}
        )"""