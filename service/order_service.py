from typing import Union

from pandas import DataFrame, Series

from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from models.dto.order_request_dto import OrderRequestDto
from models.dto.order_response_dto import OrderResponseDto
from models.entity.order_data import OrderData
from models.type.interval_type import IntervalType
from models.type.macd import MACD
from models.type.stage_type import StageType
from module.upbit_module import UpbitModule
from repository.order_data_repository import OrderDataRepository
from util import data_util


class OrderService:
    def __init__(self,
                 upbit_module: UpbitModule,
                 order_data_repository: OrderDataRepository):
        self.order_data_repository = order_data_repository
        self.upbit_module = upbit_module
        self.logger = Logger().get_logger(__class__.__name__)

    def save_data(self, order_response_dto: OrderResponseDto):
        order_data = OrderData.create_by_order_response_dto(order_response_dto)
        self.order_data_repository.save(order_data)

    def is_profit(self, ticker):
        try:
            profit = self.upbit_module.get_profit(ticker)
            if profit is None:
                return False
            self.logger.info(f"""
            =======================
                  ABOUT PROFIT
                TICKER : {ticker}
                PROFIT : {self.upbit_module.get_profit(ticker)}
            =======================
            """)
            if profit > 0.1:
                return True
            else:
                return False
        except Exception as err:
            self.logger.warn(f"""
            =======================
                   {ticker}
                err: {str(err)}
            =======================
            """)

    def buy_market_order(self, order_request_dto: OrderRequestDto):
        self.logger.info(f"""
        =======================
              BUY SIGNAL
            TICKER : {order_request_dto.ticker}
        =======================
        """)
        try:
            result = self.upbit_module.buy_market_order(order_request_dto)
            return OrderResponseDto(
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
        except Exception as err:
            self.logger.warn(f"""
            =======================
                  {order_request_dto.ticker}
                err: {str(err)}
            =======================
            """)

    def sell_market_order(self, order_request_dto: OrderRequestDto):
        self.logger.info(f"""
        =======================
              SELL SIGNAL
            TICKER : {order_request_dto.ticker}
            PROFIT : {self.upbit_module.get_profit(order_request_dto.ticker)}
        =======================
        """)
        try:
            result = self.upbit_module.sell_market_order(order_request_dto)
            return OrderResponseDto(
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
        except Exception as err:
            self.logger.warn(f"""
            =======================
                     {order_request_dto.ticker}
                err: {str(err)}
            =======================
            """)

    def create_order_request_dto(self, candle_request_dto: CandleRequestDto ,data: DataFrame, stage:int):
        MY_KRW = self.upbit_module.get_balance("KRW")
        MY_VOL = self.upbit_module.get_balance(candle_request_dto.ticker)
        try:
            up: Union[Series, None, DataFrame] = data[MACD.UPPER]
            mid: Union[Series, None, DataFrame] = data[MACD.MIDDLE]
            low: Union[Series, None, DataFrame] = data[MACD.LOWER]

            if stage == StageType.STABLE_DECREASE and MY_KRW / 2 > 6000 and MY_VOL == 0:

                ui = data_util.is_upward_trend(up.tolist()[-3:][::-1])
                mi = data_util.is_upward_trend(mid.tolist()[-3:][::-1])
                li = data_util.is_upward_trend(low.tolist()[-2:][::-1])

                if ui == True and mi == True and li == True:

                    return OrderRequestDto(
                        ticker=candle_request_dto.ticker,
                        price=MY_KRW / 2
                    )

            elif stage == StageType.STABLE_INCREASE and self.is_profit(candle_request_dto.ticker) == True and MY_VOL != 0:

                ud = data_util.is_downward_trend(up.tolist()[-2:][::-1])
                md = data_util.is_downward_trend(mid.tolist()[-2:][::-1])
                ld = data_util.is_downward_trend(low.tolist()[-2:][::-1])

                if ud == True and md == True and ld == True:
                    return OrderRequestDto(
                        ticker=candle_request_dto.ticker,
                        volume=MY_VOL,
                    )

        except Exception as e:
            self.logger.warn(e)