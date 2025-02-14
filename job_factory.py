from database import connection
from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from models.entity.candle_data import CandleData
from models.dto.candle_response_dto import CandleResponseDto
from models.type.ema import EMA
from models.type.macd import MACD
from module.upbit_module import UpbitModule
from repository.candle_data_repository import CandleDataRepository
from repository.order_data_repository import OrderDataRepository
from service.candle_service import CandleService
from service.order_service import OrderService
from utils import data_utils

class JobFactory:
    def __init__(self):
        self.connection = connection
        self.upbit_module = UpbitModule()
        self.candle_data_repository = CandleDataRepository(connection=self.connection)
        self.order_data_repository = OrderDataRepository(connection=self.connection)
        self.order_service = OrderService(
            upbit_module=self.upbit_module,
            order_data_repository=self.order_data_repository,
            candle_data_repository=self.candle_data_repository,
        )
        self.logger = Logger().get_logger(__class__.__name__)

    def init(self):
        self.candle_data_repository.init()
        self.order_data_repository.init()

    def main(self,
             ema: EMA = EMA(),
             candle_request_dto: CandleRequestDto = CandleRequestDto(),
             ):

        candle_service = CandleService(
            ema=ema,
            candle_data_repository=self.candle_data_repository,
            upbit_module=self.upbit_module
        )

        data = candle_service.get_candle_data(candle_request_dto)

        stage = data_utils.get_stage_from_ema(data=data)

        if stage != 0:

            candle_data = CandleData(
                ticker=candle_request_dto.ticker,
                close=float(data[CandleResponseDto.CLOSE].iloc[-1]),
                ema_short=float(data[EMA.SHORT].iloc[-1]),
                ema_middle=float(data[EMA.MIDDLE].iloc[-1]),
                ema_long=float(data[EMA.LONG].iloc[-1]),
                stage=stage,
                macd_upper=float(data[MACD.UPPER].iloc[-1]),
                macd_middle=float(data[MACD.MIDDLE].iloc[-1]),
                macd_lower=float(data[MACD.LOWER].iloc[-1]),
                interval=candle_request_dto.interval,
            )

            candle_service.save_data(candle_data=candle_data)

            order_request_dto = self.order_service.create_order_request_dto(
                candle_request_dto=candle_request_dto,
                data=data,
                stage=stage
            )

            if order_request_dto is not None:
                # 매수 신호
                if order_request_dto.price is not None:
                    order_response_dto = self.order_service.buy_market_order(order_request_dto)
                    self.order_service.save_data(order_response_dto)

                # 매도 신호
                if order_request_dto.volume is not None:
                    order_response_dto = self.order_service.sell_market_order(order_request_dto)
                    self.order_service.save_data(order_response_dto)

            # order_request_dto 가 None 일 때 pass
            else:
                pass
        # stage 가 0 일 때 pass
        else:
            pass

