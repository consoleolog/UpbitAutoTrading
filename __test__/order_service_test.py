import unittest

from database import connection
from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from module.upbit_module import UpbitModule
from repository.candle_data_repository import CandleDataRepository
from repository.order_data_repository import OrderDataRepository
from service.candle_service import CandleService
from service.order_service import OrderService
from util.data_util import is_empty, is_upward_trend, is_downward_trend, get_stage_from_ema


class OrderServiceTest(unittest.TestCase):
    def setUp(self):
        self.order_data_repository = OrderDataRepository(connection)
        self.upbit_module = UpbitModule()

        self.logger = Logger().get_logger(__class__.__name__)

        self.candle_data_repository = CandleDataRepository(connection)
        self.candle_service = CandleService(self.candle_data_repository)

        self.order_service = OrderService(self.order_data_repository, self.candle_data_repository)

    def test_is_profit(self):
        ticker = "KRW-ETH"
        profit = self.upbit_module.get_profit(ticker)
        self.logger.debug(profit)
        if not is_empty(profit):
            if profit > 0.1:
                self.logger.debug("+")
            else:
                self.logger.debug("-")
        else:
            return None

    def test_create_order_request_dto(self):
        candle_request_dto = CandleRequestDto()
        data = self.candle_service.get_candle_data(candle_request_dto)

        stage = get_stage_from_ema(data)

        order_request_dto = self.order_service.create_order_request_dto(candle_request_dto, data, stage)

        self.logger.debug(order_request_dto)


