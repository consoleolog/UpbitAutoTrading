import os
from typing import Optional

from dotenv import load_dotenv
from pandas import DataFrame
from slack_sdk import WebClient

from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto
from models.dto.order_request_dto import OrderRequestDto
from models.dto.order_response_dto import OrderResponseDto
from models.entity.order_data import OrderData
from models.type.interval_type import IntervalType
from models.type.macd import MACD
from models.type.stage_type import StageType
from models.type.unit_type import UnitType
from module.upbit_module import UpbitModule
from repository.candle_data_repository import CandleDataRepository
from repository.order_data_repository import OrderDataRepository
from utils import data_utils

load_dotenv()
class OrderService:
    def __init__(self,
                 order_data_repository: OrderDataRepository,
                 candle_data_repository: CandleDataRepository,
                 upbit_module: UpbitModule = UpbitModule(),
        ):
        self.order_data_repository = order_data_repository
        self.upbit_module = upbit_module
        self.candle_data_repository = candle_data_repository

        self.client = WebClient(token=os.getenv('SLACK_TOKEN'))

        self.logger = Logger().get_logger(__class__.__name__)

    def save_data(self, order_response_dto: OrderResponseDto):
        if order_response_dto is not None:
            order_data = OrderData.create_by_order_response_dto(order_response_dto)
            self.order_data_repository.save(order_data)
        else:
            self.logger.warning("OrderResponseDto is Empty")

    def is_profit(self, ticker)->Optional[bool]:
        profit = self.upbit_module.get_profit(ticker)
        self._print_profit(ticker, profit)
        if profit is not None:
            if profit > 0.1:
                return True
            else:
                return False
        else:
            return None

    def buy_market_order(self, order_request_dto: OrderRequestDto):
        self._print_buy_log(order_request_dto)
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

    def sell_market_order(self, order_request_dto: OrderRequestDto):
        self._print_sell_log(order_request_dto)
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
    def _print_sell_log(self, order_request_dto: OrderRequestDto):
        self.logger.info(f"""
        =======================
                  SELL 
            TICKER : {order_request_dto.ticker}
            PROFIT : {self.upbit_module.get_profit(order_request_dto.ticker)}
        =======================
        """)
    def _print_buy_log(self, order_request_dto: OrderRequestDto):
        self.logger.info(f"""
        =======================
                  BUY
            TICKER : {order_request_dto.ticker}
        =======================
        """)
    def _print_profit(self, ticker, profit):
        self.logger.info(f"""
        =======================
              ABOUT PROFIT
            TICKER : {ticker}
            PROFIT : {profit}
        =======================
        """)
    def _print_buy_signal_report(self, candle_request_dto, stage, up, mid, low, krw, vol):
        self.logger.info(f"""
        {'-' * 55}
        HISTOGRAM PEEK OUT (MINUS)
        {candle_request_dto.ticker} 매수 검토 
        STAGE    : {stage}
        Ticker   : {candle_request_dto.ticker}
        Interval : {candle_request_dto.interval}

        MACD (상)  
        List   : {up.tolist()[-6:]}
        Result : {data_utils.get_slope(up.tolist()[-6:])} 

        MACD (중) :
        List   : {mid.tolist()[-6:]}
        Result : {data_utils.get_slope(mid.tolist()[-6:])} 

        MACD (하)
        List   : {low.tolist()[-6:]}
        Result : {data_utils.get_slope(low.tolist()[-6:])} 

        KRW    : {krw}
        MY_VOL : {vol}
        {'-' * 55}""")

    def _print_sell_signal_report(self, candle_request_dto, stage, up, mid, low, krw, vol):
        self.logger.info(f"""
        {'-' * 55} 
        {candle_request_dto.ticker} 매도 검토 
        STAGE    : {stage}
        Ticker   : {candle_request_dto.ticker}
        Interval : {candle_request_dto.interval}

        MACD (상)  
        List   : {up.tolist()[-3:]}
        Result : {data_utils.get_slope(up.tolist()[-3:])} 

        MACD (중) :
        List   : {mid.tolist()[-3:]}
        Result : {data_utils.get_slope(mid.tolist()[-3:])} 

        MACD (하)
        List   : {low.tolist()[-3:]}
        Result : {data_utils.get_slope(low.tolist()[-3:])} 

        KRW    : {krw}
        MY_VOL : {vol}
        {'-' * 55}""")

    def create_order_request_dto(self, candle_request_dto: CandleRequestDto ,data: DataFrame, stage: StageType)->Optional[OrderRequestDto]:
        MY_KRW = self.upbit_module.get_balance("KRW")
        PRICE = 7000

        if MY_KRW:
            up, mid, low = data[MACD.UPPER], data[MACD.MIDDLE], data[MACD.LOWER]
            up_hist, mid_hist, low_hist = data[MACD.UP_HIST], data[MACD.MID_HIST], data[MACD.LOW_HIST]

            MY_VOL = self.upbit_module.get_balance(candle_request_dto.ticker)
            if MY_VOL is None or MY_VOL == 0 and MY_KRW > PRICE:
                # 매수 검토
                if stage == StageType.STABLE_DECREASE or stage == StageType.END_OF_DECREASE or stage == StageType.START_OF_INCREASE:
                    peekout = all(
                        [up_hist[-10:].min() < 0, up_hist.iloc[-1] < 0, mid_hist[-10:].min() < 0, mid_hist.iloc[-1] < 0,
                         low_hist[-10:].min() < 0, low_hist.iloc[-1] < 0,
                         up_hist[-6:].min() < up_hist.iloc[-1], mid_hist[-6:].min() < mid_hist.iloc[-1],
                         low_hist[-6:].min() < low_hist.iloc[-1]])
                    increase = data_utils.get_slope(up.tolist()[-6:]) > 100 and data_utils.get_slope(mid.tolist()[-6:]) > 100 and data_utils.get_slope(low.tolist()[-6:]) > 100
                    # Histogram 의 피크아웃을 판단
                    if peekout and increase:
                        self._print_buy_signal_report(candle_request_dto, stage, up, mid, low, MY_KRW, MY_VOL)
                        # MACD (상) (중) (하) 의 기울기가 우상향이라면
                        if candle_request_dto.interval == IntervalType(UnitType.MINUTE_5).MINUTE:
                            return OrderRequestDto(ticker=candle_request_dto.ticker, price=PRICE)

            # 매도 검토
            elif stage == StageType.STABLE_INCREASE or stage == StageType.END_OF_INCREASE or stage == StageType.START_OF_DECREASE:
                    self._print_sell_signal_report(candle_request_dto, stage, up, mid, low, MY_KRW, MY_VOL)
                    decrease = 100 > data_utils.get_slope(up.tolist()[-3:]) and 100 > data_utils.get_slope(mid.tolist()[-3:]) and 100 > data_utils.get_slope(low.tolist()[-3:])
                    # MACD (상) (중) (하) 가 모두 우하향이라면
                    if decrease or (data_utils.get_slope(up.tolist()[-3:]) < 0 and data_utils.get_slope(mid.tolist()[-3:]) < 0) :
                        # 수익률이 0.1 이 넘는다면
                        if self.is_profit(candle_request_dto.ticker):
                            return OrderRequestDto(ticker=candle_request_dto.ticker, volume=MY_VOL)

