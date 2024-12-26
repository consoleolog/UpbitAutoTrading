from database import connection
from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from models.entity.candle_data import CandleData
from models.dto.candle_response_dto import CandleResponseDto
from models.entity.order_data import OrderData
from models.type.ema import EMA
from models.type.macd import MACD
from module.upbit_module import UpbitModule
from repository.candle_data_repository import CandleDataRepository
from repository.order_data_repository import OrderDataRepository
from service.candle_service import CandleService
from service.order_service import OrderService
from util import data_util


class JobFactory:
    def __init__(self):
        self.upbit_module = UpbitModule()
        self.candle_data_repository = CandleDataRepository(connection=connection)
        self.order_data_repository = OrderDataRepository(connection=connection)
        self.order_service = OrderService(
            upbit_module=self.upbit_module,
            order_data_repository=self.order_data_repository
        )
        self.logger = Logger().get_logger(__class__.__name__)


    def before_starting_job(self):
        self.candle_data_repository.init()
        self.order_data_repository.init()

    def main(self,
             ema: EMA = EMA(),
             candle_request_dto: CandleRequestDto = CandleRequestDto(),
             ):
        candle_service = CandleService(
            candle_data_repository=self.candle_data_repository,
            ema=ema,
        )

        data = self.upbit_module.get_candles_data(candle_request_dto)
        data = candle_service.create_sub_data(data=data)

        stage = data_util.get_stage_from_ema(data=data)

        candle_data = CandleData(
            ticker=candle_request_dto.ticker,
            close=data[CandleResponseDto.CLOSE].iloc[-1],
            ema_short=data[EMA.SHORT].iloc[-1],
            ema_middle=data[EMA.MIDDLE].iloc[-1],
            ema_long=data[EMA.LONG].iloc[-1],
            stage=stage,
            macd_upper=data[MACD.UPPER].iloc[-1],
            macd_middle=data[MACD.MIDDLE].iloc[-1],
            macd_lower=data[MACD.LOWER].iloc[-1],
            interval=candle_request_dto.interval,
        )

        candle_service.save_data(candle_data=candle_data)

        order_request_dto = self.order_service.create_order_request_dto(
            ticker=candle_request_dto.ticker,
            data=data
        )

        if order_request_dto is None:
            self.logger.warn()
        else:
            # 매수 신호
            if order_request_dto.price is not None:
                order_response_dto = self.order_service.buy_market_order(order_request_dto)
                self.order_service.save_data(order_response_dto)

            # 매도 신호
            elif order_request_dto.volume is not None:
                is_profit = self.order_service.is_profit(candle_request_dto.ticker)
                if is_profit:
                    order_response_dto = self.order_service.sell_market_order(order_request_dto)
                    self.order_service.save_data(order_response_dto)



