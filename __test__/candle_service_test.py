import unittest

import pyupbit
from scipy.stats import linregress

from database import connection
from models.dto.candle_request_dto import CandleRequestDto
from models.dto.candle_response_dto import CandleResponseDto
from models.type.ema import EMA
from models.type.interval_type import IntervalType
from models.type.macd import MACD
from models.type.stage_type import StageType
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


    def test_get_candle_data(self):

        candle_request_dto = CandleRequestDto(
            ticker=self.ticker,
            interval=IntervalType.DAY,
        )
        data = self.upbit_module.get_candles_data(candle_request_dto)



    def test_create_sub_data(self):
        candle_request_dto = CandleRequestDto(
            ticker=self.ticker,
            interval=IntervalType.DAY,
        )
        data = self.upbit_module.get_candles_data(candle_request_dto)
        data[EMA.SHORT] = data[CandleResponseDto.CLOSE].ewm(span=self.ema.short).mean()
        data[EMA.MIDDLE] = data[CandleResponseDto.CLOSE].ewm(span=self.ema.middle).mean()
        data[EMA.LONG] = data[CandleResponseDto.CLOSE].ewm(span=self.ema.long).mean()

        data[MACD.UPPER] = data[EMA.SHORT] - data[EMA.MIDDLE]
        data[MACD.MIDDLE] = data[EMA.SHORT] - data[EMA.LONG]
        data[MACD.LOWER] = data[EMA.MIDDLE] - data[EMA.LONG]

        data[MACD.UP_INCREASE] = data[MACD.UPPER] > data[MACD.UPPER].shift(1)
        data[MACD.MID_INCREASE] = data[MACD.MIDDLE] > data[MACD.MIDDLE].shift(1)
        data[MACD.LOW_INCREASE] = data[MACD.LOWER] > data[MACD.LOWER].shift(1)

        a = data[MACD.LOWER]

        print(data[MACD.LOWER].tolist())
        print(is_upward_trend(data[MACD.LOWER].tolist()))


    def test_loop(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        last_five_reversed = data[-5:][::-1]
        print(last_five_reversed)


if __name__ == '__main__':
    unittest.main()
