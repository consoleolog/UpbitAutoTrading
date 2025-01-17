import unittest

from database import connection
from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from models.dto.candle_response_dto import CandleResponseDto
from models.entity.candle_data import CandleData
from models.type.ema import EMA
from models.type.interval_type import IntervalType
from models.type.macd import MACD
from models.type.stage_type import StageType
from models.type.unit_type import UnitType
from module.upbit_module import UpbitModule
from repository.candle_data_repository import CandleDataRepository
from service.candle_service import CandleService
from util.data_util import is_empty


class CandleServiceTest(unittest.TestCase):
    def setUp(self):
        self.candle_data_repository = CandleDataRepository(connection)
        self.upbit_module = UpbitModule()
        self.logger = Logger().get_logger(__class__.__name__)

        self.ema = EMA()

        self.candle_service = CandleService(
            self.candle_data_repository,
            self.ema,
            self.upbit_module
        )

    def test_get_candles_data(self):
        ticker = "KRW-AAVE"
        interval = IntervalType(UnitType.MINUTE_5).MINUTE
        candle_request_dto = CandleRequestDto(ticker=ticker,interval=interval)
        data = self.candle_service.get_candle_data(candle_request_dto)
        self.logger.debug(data)
        self.logger.debug(type(data))

    def test_create_sub_data(self):
        ticker = "KRW-AAVE"
        interval = IntervalType(UnitType.MINUTE_5).MINUTE
        candle_request_dto = CandleRequestDto(ticker=ticker,interval=interval)

        data = self.candle_data_repository.find_all_by_ticker_and_interval(
            ticker=ticker,
            interval=interval
        )
        if not is_empty(data):

            data[EMA.SHORT] = data[CandleResponseDto.CLOSE].ewm(span=self.ema.short).mean()
            data[EMA.MIDDLE] = data[CandleResponseDto.CLOSE].ewm(span=self.ema.middle).mean()
            data[EMA.LONG] = data[CandleResponseDto.CLOSE].ewm(span=self.ema.long).mean()

            data[MACD.UPPER] = data[EMA.SHORT] - data[EMA.MIDDLE]
            data[MACD.MIDDLE] = data[EMA.SHORT] - data[EMA.LONG]
            data[MACD.LOWER] = data[EMA.MIDDLE] - data[EMA.LONG]

            data[MACD.SIGNAL] = data[CandleResponseDto.CLOSE].ewm(span=9).mean()
            data[MACD.UP_HIST] = data[MACD.UPPER] - data[MACD.SIGNAL]
            data[MACD.MID_HIST] = data[MACD.MIDDLE] - data[MACD.SIGNAL]
            data[MACD.LOW_HIST] = data[MACD.LOWER] - data[MACD.SIGNAL]

            self.logger.debug(data)

    def test_save_data(self):
        candle_data = CandleData(
            ticker="KRW-AAVE",
            close=123,
            ema_short=123,
            ema_middle=123,
            ema_long=123,
            stage=StageType.STABLE_DECREASE,
            macd_upper=123,
            macd_middle=123,
            macd_lower=123,
            interval=IntervalType(UnitType.MINUTE_5).MINUTE,
        )

        if not is_empty(candle_data):
            self.logger.debug(candle_data)

