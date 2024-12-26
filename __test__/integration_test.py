import unittest

from database import connection
from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from models.dto.candle_response_dto import CandleResponseDto
from models.dto.order_request_dto import OrderRequestDto
from models.dto.order_response_dto import OrderResponseDto
from models.entity.candle_data import CandleData
from models.entity.order_data import OrderData
from models.type.ema import EMA
from models.type.interval_type import IntervalType
from models.type.macd import MACD
from models.type.unit_type import UnitType
from module.upbit_module import UpbitModule
from repository.candle_data_repository import CandleDataRepository
from repository.order_data_repository import OrderDataRepository
from service.candle_service import CandleService
from service.order_service import OrderService
from util import data_util


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.upbit_module = UpbitModule()
        self.candle_data_repository = CandleDataRepository(connection=connection)
        self.order_data_repository = OrderDataRepository(connection=connection)
        self.order_service = OrderService(
            upbit_module=self.upbit_module,
            order_data_repository=self.order_data_repository
        )
        self.logger = Logger().get_logger(__class__.__name__)
        self.ema = EMA()
        self.candle_request_dto = CandleRequestDto(
            ticker="KRW-BTC",
            interval=IntervalType(UnitType.MINUTE).MINUTE
        )
        self.candle_service = CandleService(
            candle_data_repository=self.candle_data_repository,
            ema=self.ema,
        )

    def test_init(self):
        self.candle_data_repository.init()
        self.order_data_repository.init()

    def test_get_b(self):
        self.logger.info(self.upbit_module.get_balance("KRW-BTC"))

    def test_buy_market_order(self):
        order_request_dto = OrderRequestDto(
            ticker="KRW-XRP",
            price= 5500,
        )
        result = self.upbit_module.buy_market_order(order_request_dto)
        self.logger.info(result)
        order_response_dto = OrderResponseDto(
            uuid=result['uuid'],
            side=result['side'],
            ord_type=result['ord_type'],
            price=result['price'],
            state=result['state'],
            market=result['market'],
            created_at=result['created_at'],
            reserved_fee=result['reserved_fee'],
            remaining_fee=result['remaining_fee'],
            paid_fee=result['paid_fee'],
            locked=result['locked'],
            executed_volume=result['executed_volume'],
            trades_count=result['trades_count']
        )
        self.logger.info(order_response_dto)
        order_data = OrderData.create_by_order_response_dto(order_response_dto)
        self.logger.info(order_data)
        self.order_data_repository.save(order_data)

    def test_sell_market_order(self):
        volume = self.upbit_module.get_balance("KRW-XRP")
        order_request_dto = OrderRequestDto(
            ticker="KRW-XRP",
            volume=volume
        )
        result = self.upbit_module.sell_market_order(order_request_dto)
        self.logger.info(result)
        order_response_dto = OrderResponseDto(
            uuid=result['uuid'],
            side=result['side'],
            ord_type=result['ord_type'],
            market=result['market'],
            state=result['state'],
            created_at=result['created_at'],
            volume=result['volume'],
            remaining_volume=result['remaining_volume'],
            reserved_fee=result['reserved_fee'],
            remaining_fee=result['remaining_fee'],
            paid_fee=result['paid_fee'],
            locked=result['locked'],
            executed_volume=result['executed_volume'],
            trades_count=result['trades_count']
        )
        self.logger.info(order_response_dto)
        order_data = OrderData.create_by_order_response_dto(order_response_dto)
        self.logger.info(order_data)
        self.order_data_repository.save(order_data)

    def test_get_data(self):
        data = self.upbit_module.get_candles_data(self.candle_request_dto)
        # self.logger.info(data.iloc[-1])

        data = self.candle_service.create_sub_data(data)
        # self.logger.info(data.iloc[-1])

        stage = data_util.get_stage_from_ema(data)
        # self.logger.info(stage)

        candle_data = CandleData(
            ticker=self.candle_request_dto.ticker,
            close=data[CandleResponseDto.CLOSE].iloc[-1],
            ema_short=data[EMA.SHORT].iloc[-1],
            ema_middle=data[EMA.MIDDLE].iloc[-1],
            ema_long=data[EMA.LONG].iloc[-1],
            stage=stage,
            macd_upper=data[MACD.UPPER].iloc[-1],
            macd_middle=data[MACD.MIDDLE].iloc[-1],
            macd_lower=data[MACD.LOWER].iloc[-1],
            interval=self.candle_request_dto.interval,
        )
        # self.logger.info(candle_data)

        # self.candle_service.save_data(candle_data=candle_data)










