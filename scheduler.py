from logging import Logger

from apscheduler.schedulers.background import BackgroundScheduler

from job_factory import JobFactory
from models.dto.candle_request_dto import CandleRequestDto
from models.type.interval_type import IntervalType
from models.type.unit_type import UnitType

job_factory = JobFactory()


scheduler = BackgroundScheduler()

scheduler.add_job(
    func=job_factory.main,
    trigger='interval',
    seconds=10,
    kwargs={
        "candle_request_dto": CandleRequestDto(
            ticker="KRW-BTC",
            interval=IntervalType(UnitType.MINUTE).MINUTE
        )
    }
)

def create_table_if_not_exist():
    job_factory.before_starting_job()