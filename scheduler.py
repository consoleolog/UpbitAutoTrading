
from apscheduler.schedulers.background import BackgroundScheduler

from job_factory import JobFactory
from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from models.type.interval_type import IntervalType
from models.type.unit_type import UnitType

tickers = [
    "KRW-BTC",
    "KRW-ETH",
    "KRW-BCH",
    "KRW-AAVE",
    "KRW-SOL",
    "KRW-BSV",
    # "KRW-AVAX",
    # "KRW-EGLD",
    # "KRW-ENS",
]

logger = Logger().get_logger("scheduler")

job_factory = JobFactory()

scheduler = BackgroundScheduler()

try :
    for ticker in tickers:

        scheduler.add_job(
            func=job_factory.main,
            trigger='interval',
            minutes=UnitType.HOUR,
            kwargs={
                "candle_request_dto": CandleRequestDto(
                    ticker=ticker,
                    interval=IntervalType(UnitType.HOUR).MINUTE
                ),
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

        scheduler.add_job(
            func=job_factory.main,
            trigger='interval',
            minutes=UnitType.MINUTE_5,
            kwargs={
                "candle_request_dto": CandleRequestDto(
                    ticker=ticker,
                    interval=IntervalType(UnitType.MINUTE_5).MINUTE
                ),
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
            },
            id=f"{ticker}_{IntervalType(UnitType.HALF_HOUR).MINUTE}"
        )

except Exception as e:
    logger.warn(f"""
    {"-" * 40}
          FAIL TO ADD JOB
          {str(e)}
    {"-" * 40}
    """)