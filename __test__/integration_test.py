import os
import smtplib
import unittest
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from typing import Union
import statistics
import pandas as pd
from dotenv import load_dotenv
from pandas import Series, DataFrame

from database import connection
from logger import Logger
from models.dto.candle_request_dto import CandleRequestDto

from models.dto.order_request_dto import OrderRequestDto
from models.dto.order_response_dto import OrderResponseDto

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

load_dotenv()
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
        self.ema = EMA(long=40)
        self.candle_request_dto = CandleRequestDto(
            ticker="KRW-XRP",
            interval=IntervalType(UnitType.MINUTE_5).MINUTE
        )
        self.candle_service = CandleService(
            candle_data_repository=self.candle_data_repository,
            ema=self.ema,
            upbit_module=self.upbit_module
        )
        self.connection = connection

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
        ticker = "KRW-AAVE"
        volume = self.upbit_module.get_balance(ticker)
        order_request_dto = OrderRequestDto(
            ticker=ticker,
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
        data = self.candle_service.get_candle_data(self.candle_request_dto)
        up: Union[Series, None, DataFrame] = data[MACD.UPPER]
        mid: Union[Series, None, DataFrame] = data[MACD.MIDDLE]
        low: Union[Series, None, DataFrame] = data[MACD.LOWER]

        up_hist: Union[Series, None, DataFrame] = data[MACD.UP_HIST]
        mid_hist: Union[Series, None, DataFrame] = data[MACD.MID_HIST]
        low_hist: Union[Series, None, DataFrame] = data[MACD.LOW_HIST]

        up_list = up.tolist()[-2:]
        mid_list = mid.tolist()[-2:]
        low_list = low.tolist()[-2:]

        up_hist_list = up_hist.tolist()[-7:]
        mid_hist_list = mid_hist.tolist()[-7:]
        low_hist_list = low_hist.tolist()[-7:]

        self.logger.info(f"""
        {'-'*30}
        
        UP   : {up_list}
        {data_util.is_upward_trend(up.tolist()[-5:])}
        HIST : {up_hist_list}
        {up_hist.max()}
        {up_hist.iloc[-1]}
        
        {'-'*30}
        
        MID  : {mid_list}
        {data_util.is_upward_trend(mid.tolist()[-5:])}
        HIST : {mid_hist_list}
        {mid_hist.max()}
        {mid_hist.iloc[-1]}
        
        {'-'*30}
        
        LOW : {low_list}
        {data_util.is_upward_trend(low.tolist()[-5:])}
        LOW : {low_hist_list}
        {low_hist.max()}
        {low_hist.iloc[-1]}

        
        {'-'*30}
        """)

        is_plus = all([
            up_hist.max() > 0,
            up_hist.iloc[-1] > 0,
            mid_hist.max() > 0,
            mid_hist.iloc[-1] > 0,
            low_hist.max() > 0,
            low_hist.iloc[-1] > 0,
        ])
        is_minus = all([
            up_hist.min() < 0,
            up_hist.iloc[-1] < 0,
            mid_hist.min() < 0,
            mid_hist.iloc[-1] < 0,
            low_hist.min() < 0,
            low_hist.iloc[-1] < 0,
        ])

        self.logger.info(up_hist[-10:])

        # 히스토그램이 양수일 때
        if is_plus and ( up_hist.max() > up_hist.iloc[-1] and
                         mid_hist.max() > mid_hist.iloc[-1] and
                         low_hist.max() > low_hist.iloc[-1] ):
            pass
        elif is_minus and ( up_hist.min() < up_hist.iloc[-1] and
                            mid_hist.min() < mid_hist.iloc[-1] and
                            low_hist.min() < low_hist.iloc[-1]):
            pass




        # std_dev = statistics.stdev([10, 20, 30, 40, 50, 40])
        #
        # self.logger.debug(std_dev)
        #
        # #짧은 구간 동안 기울기가 세개다 상승인지 판단
        # if data_util.is_upward_trend(up.tolist()[-5:]) and data_util.is_upward_trend(mid.tolist()[-5:]) and data_util.is_upward_trend(low.tolist()[-5:]):
        #     self.logger.info("증가")



        # elif data_util.is_downward_trend(up.tolist()[-5:]) and data_util.is_downward_trend(mid.tolist()[-5:]) and data_util.is_downward_trend(low.tolist()[-5:]):
        #     self.logger.info("감소")





    def test_refresh(self):
        SQL = """
        SELECT C.CANDLE_ID,
               C.DATE,
               C.TICKER,
               C.CLOSE,
               C.EMA_SHORT,
               C.EMA_MIDDLE,
               C.EMA_LONG,
               C.STAGE,
               C.MACD_UPPER,
               C.MACD_MIDDLE,
               C.MACD_LOWER,
               C.INTERVAL
        FROM CANDLE_DATA C;  
        """
        data = pd.read_sql(SQL, self.connection)
        data.to_csv("data.csv", encoding="utf-8")
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '[Upbit Auto Trading] 로그 파일 백업'
        msg['From'] = os.getenv('SMTP_FROM')
        msg['To'] = os.getenv('SMTP_TO')
        with open("data.csv", 'rb') as handler:
            file = MIMEBase('application', 'octet-stream')
            file.set_payload(handler.read())
            encoders.encode_base64(file)
            file.add_header("Content-Disposition", f'attachment; filename=data.csv')
            msg.attach(file)
        s = smtplib.SMTP(os.getenv('SMTP_HOST'), os.getenv('SMTP_PORT') or 587)
        s.starttls()
        s.login(os.getenv("SMTP_ID"), os.getenv("SMTP_PASSWORD"))
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.close()

    def test_get_balance(self):
        self.logger.debug(self.upbit_module.get_currencies())

        ticker = "KRW-BCH"
        balance = self.upbit_module.get_profit(ticker)

        self.logger.debug(balance)

    def test_get_currency(self):
        currencies = self.upbit_module.get_currencies()
        my_currency = []
        for c in currencies:
            self.logger.info(c["currency"])
            if c["currency"] != "KRW":
                my_currency.append(c["currency"])

        for ticker in my_currency:
            self.logger.info(self.upbit_module.get_profit(f"KRW-{ticker}"))









