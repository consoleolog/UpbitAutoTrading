import unittest
from typing import List

from scipy.stats import linregress

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


def is_upward_trend(data):
    """
    데이터의 기울기를 계산하여 우상향 여부를 판단
    :param data: 숫자 리스트
    :return: bool (True: 우상향, False: 우하향)
    """
    if len(data) < 2:
        raise ValueError("데이터는 최소 2개 이상의 값을 포함해야 합니다.")

    x = list(range(len(data)))
    slope, _, _, _, _ = linregress(x, data)

    return slope > 0

class CandleServiceTest(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def setUp(self):
        self.ticker = "KRW-BTC"

        self.candle_data_repository = CandleDataRepository(connection)
        self.ema = EMA()
        self.upbit_module = UpbitModule()
        self.logger = Logger().get_logger(__class__.__name__)

    def test_create_sub_data(self):
        candle_request_dto = CandleRequestDto(
            ticker=self.ticker,
            interval=IntervalType(UnitType.MINUTE_5).MINUTE,
        )
        data = self.candle_data_repository.find_all_by_ticker_and_interval(
            ticker=candle_request_dto.ticker,
            interval=candle_request_dto.interval,
        )
        self.logger.debug(data)
        self.logger.debug(data.iloc[-1])
        self.logger.debug(data["close"].iloc[-1])
        data[EMA.SHORT] = data[CandleResponseDto.CLOSE].ewm(span=self.ema.short).mean()
        data[EMA.MIDDLE] = data[CandleResponseDto.CLOSE].ewm(span=self.ema.middle).mean()
        data[EMA.LONG] = data[CandleResponseDto.CLOSE].ewm(span=self.ema.long).mean()

        data[MACD.UPPER] = data[EMA.SHORT] - data[EMA.MIDDLE]
        data[MACD.MIDDLE] = data[EMA.SHORT] - data[EMA.LONG]
        data[MACD.LOWER] = data[EMA.MIDDLE] - data[EMA.LONG]

        print(data[MACD.LOWER].tolist())
        print(is_upward_trend(data[MACD.LOWER].tolist()))


    def test_loop(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        last_five_reversed = data[-5:][::-1]
        self.logger.info(last_five_reversed)

    def test_check_minutes30_and_days(self):
        ticker = "KRW-BSV"
        minutes30 = IntervalType(UnitType.HALF_HOUR).MINUTE
        days = IntervalType.DAY

        minutes30_data = self.candle_data_repository.find_all_by_ticker_and_interval(ticker, minutes30)
        days_data = self.candle_data_repository.find_all_by_ticker_and_interval(ticker, days)

        self.logger.info(minutes30_data)
        self.logger.info(CandleData(*minutes30_data[0]))

        minutes30_last_data = CandleData(*minutes30_data[0])
        days_last_data = CandleData(*days_data[0])

        self.logger.debug(minutes30_last_data)
        self.logger.debug(days_last_data)

        if (CandleData(*minutes30_data[0]).stage == StageType.STABLE_DECREASE or
            CandleData(*minutes30_data[0]).stage == StageType.END_OF_DECREASE and
            CandleData(*days_data[0]).stage == StageType.STABLE_DECREASE or
            CandleData(*days_data[0]).stage == StageType.END_OF_DECREASE
        ):
            self.logger.info("Not yet")



if __name__ == '__main__':
    unittest.main()
