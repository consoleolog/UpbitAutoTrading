import unittest

import pyupbit

from database import connection
from models.dto.candle_request_dto import CandleRequestDto
from models.dto.candle_response_dto import CandleResponseDto
from models.type.ema import EMA
from models.type.interval_type import IntervalType
from models.type.macd import MACD
from module.upbit_module import UpbitModule
from repository.candle_data_repository import CandleDataRepository


class CandleServiceTest(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def setUp(self):
        self.ticker = "KRW-BTC"

        self.candle_data_repository = CandleDataRepository(connection)
        self.ema = EMA()
        self.upbit_module = UpbitModule()


    def test_get_candle_data(self):
        data1 = pyupbit.get_ohlcv(
            ticker=self.ticker,
            interval=IntervalType.DAY,
        )

        candle_request_dto = CandleRequestDto(
            ticker=self.ticker,
            interval=IntervalType.DAY,
        )
        data2 = self.upbit_module.get_candles_data(candle_request_dto)
        self.assertEqual(data1, data2)

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

    # def test_save_data(self):



if __name__ == '__main__':
    unittest.main()
