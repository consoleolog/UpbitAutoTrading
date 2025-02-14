from apscheduler.schedulers.background import BackgroundScheduler

from job_factory import JobFactory
from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from models.type.ema import EMA

from models.type.interval_type import IntervalType
from models.type.unit_type import UnitType

tickers = [
    "KRW-BTC",
    "KRW-ETH",
    "KRW-BCH",
    "KRW-AAVE",
    "KRW-SOL",
    "KRW-BSV",
]

logger = Logger().get_logger("scheduler")

job_factory = JobFactory()

scheduler = BackgroundScheduler()

for ticker in tickers:

    scheduler.add_job(
        func=job_factory.main,
        trigger='interval',
        minutes=UnitType.MINUTE_5,
        kwargs={
            "candle_request_dto": CandleRequestDto(
                ticker=ticker,
                interval=IntervalType(UnitType.MINUTE_5).MINUTE
            ),
            "ema": EMA(
                short=14,
                middle=30,
                long=60,
            )
        },
        id=f"{ticker}_{IntervalType(UnitType.MINUTE_5).MINUTE}"
    )

    scheduler.add_job(
        func=job_factory.main,
        trigger='interval',
        minutes=UnitType.HALF_HOUR,
        kwargs={
            "candle_request_dto": CandleRequestDto(
                ticker=ticker,
                interval=IntervalType(UnitType.HALF_HOUR).MINUTE
            ),
            "ema": EMA(
                short=14,
                middle=30,
                long=60,
            )
        },
        id=f"{ticker}_{IntervalType(UnitType.HALF_HOUR).MINUTE}"
    )

    scheduler.add_job(
        func=job_factory.main,
        trigger='interval',
        minutes=UnitType.HOUR,
        kwargs={
            "candle_request_dto": CandleRequestDto(
                ticker=ticker,
                interval=IntervalType(UnitType.HOUR).MINUTE
            ),
            "ema": EMA(
                short=14,
                middle=30,
                long=60,
            )
        },
        id=f"{ticker}_{IntervalType(UnitType.HOUR).MINUTE}"
    )

    scheduler.add_job(
        func=job_factory.main,
        trigger='interval',
        minutes=UnitType.HOUR_4,
        kwargs={
            "candle_request_dto": CandleRequestDto(
                ticker=ticker,
                interval=IntervalType(UnitType.HOUR_4).MINUTE
            )
        },
        id=f"{ticker}_{IntervalType(UnitType.HOUR_4).MINUTE}"
    )