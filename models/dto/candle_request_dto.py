from typing import Any

from models.type.interval_type import IntervalType


class CandleRequestDto:
    def __init__(
            self,
            ticker: str = "KRW-BTC",
            count: int = 200,
            interval: IntervalType = IntervalType.DAY,
            to: Any = None
    ):
        self.ticker = ticker
        self.count = count
        self.interval = interval
        self.to = to

    def __str__(self):
        return f"""CandleRequestDto(
            ticker={self.ticker},
            count={self.count},
            interval={self.interval},
            to={self.to}
        )"""