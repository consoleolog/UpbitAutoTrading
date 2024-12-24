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


class EmaDto:
    def __init__(self, short=10, middle=20, long=40):
        self.short = short
        self.middle = middle
        self.long = long

        self.SHORT = self._EmaField(name="EMA_SHORT", value=self.short)
        self.MIDDLE = self._EmaField(name="EMA_MIDDLE", value=self.middle)
        self.LONG = self._EmaField(name="EMA_LONG", value=self.long)

    class _EmaField:
        def __init__(self, name, value):
            self.name = name
            self.value = value

        def __repr__(self):
            return f"{self.name}: {self.value}"

    def __repr__(self):
        return (f"EmaDto(short={self.short}, middle={self.middle}, long={self.long}, "
                f"SHORT={self.SHORT}, MIDDLE={self.MIDDLE}, LONG={self.LONG})")


class MacdDto:
    class UPPER:
        name = "MACD_UPPER"
        INCREASE = "MACD_UPPER_INCREASE"

    class MIDDLE:
        name = "MACD_MIDDLE"
        INCREASE = "MACD_MIDDLE_INCREASE"


    class LOWER:
        name = "MACD_LOWER"
        INCREASE = "MACD_LOWER_INCREASE"


class RequestOrderDto:
    class OrdType:
        BUY = 'BUY'
        SELL = 'SELL'

    def __init__(
            self,
            mode=None,
            price=None,
            volume=None,
    ):
        self.mode = mode
        self.price = price
        self.volume = volume

    def set_mode(self, mode):
        self.mode = mode
        return self
    def set_price(self, price):
        self.price = price
        return self
    def set_volume(self, volume):
        self.volume = volume
        return self
    def build(self):
        if not self.mode:
            raise ValueError("Mode is required")
        return self

    def __str__(self): return f"""RequestOrderDto(
        mode={self.mode},
        price={self.price},
        volume={self.volume}
    )"""

class ResponseOrderDto:
    def __init__(
            self,
            uuid=None,
            side=None,
            ord_type=None,
            price=None,
            volume=None,
            state=None,
            market=None,
            created_at=None,
            reserved_fee=None,
            remaining_fee=None,
            remaining_volume=None,
            paid_fee=None,
            locked=None,
            executed_volume=None,
            trades_count=None
    ):
        self.uuid = uuid
        self.side = side
        self.ord_type = ord_type
        self.price = price
        self.volume = volume
        self.state = state
        self.market = market
        self.created_at = created_at
        self.reserved_fee = reserved_fee
        self.remaining_fee = remaining_fee
        self.remaining_volume = remaining_volume
        self.paid_fee = paid_fee
        self.locked = locked
        self.executed_volume = executed_volume
        self.trades_count = trades_count

    @staticmethod
    def created_by_buy_res(dicts):
        return ResponseOrderDto(
            uuid=dicts['uuid'],
            side=dicts['side'],
            ord_type=dicts['ord_type'],
            price=dicts['price'],
            state=dicts['state'],
            market=dicts['market'],
            created_at=dicts['created_at'],
            reserved_fee=dicts['reserved_fee'],
            remaining_fee=dicts['remaining_fee'],
            paid_fee=dicts['paid_fee'],
            locked=dicts['locked'],
            executed_volume=dicts['executed_volume'],
            trades_count=dicts['trades_count']
        )

    @staticmethod
    def created_by_sell_res(dicts):
        return ResponseOrderDto(
            uuid=dicts['uuid'],
            side=dicts['side'],
            ord_type=dicts['ord_type'],
            market=dicts['market'],
            state=dicts['state'],
            created_at=dicts['created_at'],
            volume=dicts['volume'],
            remaining_volume=dicts['remaining_volume'],
            reserved_fee=dicts['reserved_fee'],
            remaining_fee=dicts['remaining_fee'],
            paid_fee=dicts['paid_fee'],
            locked=dicts['locked'],
            executed_volume=dicts['executed_volume'],
            trades_count=dicts['trades_count']
        )

    def __str__(self):
        return f"""
        ResponseOrderDto(
            uuid={self.uuid},
            side={self.side},
            ord_type={self.ord_type},
            price={self.price},
            volume={self.volume},
            state={self.state},
            market={self.market},
            created_at={self.created_at},
            reserved_fee={self.reserved_fee},
            remaining_fee={self.remaining_fee},
            remaining_volume={self.remaining_volume},
            paid_fee={self.paid_fee},
            locked={self.locked},
            executed_volume={self.executed_volume},
            trades_count={self.trades_count}
        )
        """