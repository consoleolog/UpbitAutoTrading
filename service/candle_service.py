from pandas import DataFrame
from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from models.entity.candle_data import CandleData
from models.dto.candle_response_dto import CandleResponseDto
from models.type.ema import EMA
from models.type.macd import MACD
from module.upbit_module import UpbitModule
from repository.candle_data_repository import CandleDataRepository

class CandleService:
    def __init__(self,
                 candle_data_repository: CandleDataRepository,
                 ema: EMA = EMA(),
                 upbit_module: UpbitModule=UpbitModule()):
        self.candle_data_repository = candle_data_repository
        self.ema = ema
        self.upbit_module = upbit_module
        self.logger = Logger().get_logger(__class__.__name__)

    def create_sub_data(self, data: DataFrame)->DataFrame:
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
        return data

    def get_candle_data(self, candle_request_dto: CandleRequestDto)->DataFrame:
        try:
            data = self.upbit_module.get_candles_data(candle_request_dto)
            if data:
                data = self.create_sub_data(data=data)
                return data
            else:
                raise ValueError()
        except ValueError:
            data = self.candle_data_repository.find_all_by_ticker_and_interval(
                ticker=candle_request_dto.ticker,
                interval=candle_request_dto.interval,
            )
            data = self.create_sub_data(data=data)
            return data


    def save_data(self, candle_data: CandleData) -> None:
        if candle_data:
            self.candle_data_repository.save(candle_data)
        else:
            self.logger.warning("CandleData is Empty")



