

from pandas import DataFrame

from logger import Logger
from models.dto.order_request_dto import OrderRequestDto
from models.dto.order_response_dto import OrderResponseDto
from models.entity.order_data import OrderData
from models.type.macd import MACD
from module.upbit_module import UpbitModule
from repository.order_data_repository import OrderDataRepository


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

    def create_order_request_dto(self, ticker ,data: DataFrame):
        up: DataFrame = data[MACD.UP_INCREASE]
        mid: DataFrame = data[MACD.MID_INCREASE]
        low: DataFrame = data[MACD.LOW_INCREASE]

        UP_INCREASE = all([
            up.iloc[-1] == True,
            up.iloc[-2] == True,
            up.iloc[-3] == False,
            up.iloc[-4] == False,
        ])
        MID_INCREASE = all([
            mid.iloc[-1] == True,
            mid.iloc[-2] == True,
            mid.iloc[-3] == False,
            mid.iloc[-4] == False,
        ])
        LOW_INCREASE = all([
            low.iloc[-1] == True,
            low.iloc[-2] == True,
            low.iloc[-3] == False,
            low.iloc[-4] == False,
        ])

        UP_DECREASE = all([
            up.iloc[-1] == False,
            up.iloc[-2] == False,
            up.iloc[-3] == False,
        ])

        MID_DECREASE = all([
            mid.iloc[-1] == False,
            mid.iloc[-2] == False,
            mid.iloc[-3] == False,
        ])

        LOW_DECREASE = all([
            mid.iloc[-1] == False,
            mid.iloc[-2] == False,
        ])

        if UP_INCREASE and MID_INCREASE and LOW_INCREASE :
            krw = self.upbit_module.get_balance("KRW")
            price = krw / 7.5
            if price > 6000:
                return OrderRequestDto(
                    ticker=ticker,
                    price=price,
                )
        elif UP_DECREASE and MID_DECREASE and LOW_DECREASE:
            my_vol = self.upbit_module.get_balance(ticker)
            return OrderRequestDto(
                ticker=ticker,
                volume=my_vol,
            )