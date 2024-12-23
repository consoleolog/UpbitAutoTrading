import pyupbit

from pyupbit import Upbit

from config.app_properties import AppProperties
from logger import Logger
from models.candles_dto import RequestCandlesDto
from models.ma_dto import EmaDto, MacdDto
from models.order_dto import ResponseOrderDto
from components.strategy_component import StrategyComponent


class UpbitComponent:
    def __init__(self, app_properties: AppProperties):
        self.logger = Logger().get_logger(__class__.__name__)
        self.Upbit = Upbit(
            app_properties.upbit_access_key,
            app_properties.upbit_secret_key,
        )

    def get_balances(self):
        return self.Upbit.get_balances()

    def get_balance(self, ticker):
        return self.Upbit.get_balance(ticker)

    def get_current_price(self, ticker):
        return pyupbit.get_current_price(ticker)

    def create_sell_order(self, ticker, volume):
        res = self.Upbit.sell_market_order(
            ticker=ticker,
            volume=volume,
        )
        return ResponseOrderDto.created_by_sell_res(res)

    def create_buy_order(self, ticker, price):
        res = self.Upbit.buy_market_order(
            ticker=ticker,
            price=price,
        )
        return ResponseOrderDto.created_by_buy_res(res)


    def get_candles(self, request_candles_dto: RequestCandlesDto):
        ticker = request_candles_dto.ticker
        count = request_candles_dto.count
        to = request_candles_dto.to
        interval = request_candles_dto.interval
        unit = request_candles_dto.unit

        if request_candles_dto.interval == RequestCandlesDto.Interval.MINUTE and unit:
            interval = f"{interval}{unit}"

        return pyupbit.get_ohlcv(
            ticker=ticker,
            count=count,
            interval=interval,
            to=to,
        )