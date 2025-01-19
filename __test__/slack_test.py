import os
import unittest

import pandas as pd
from dotenv import load_dotenv
from slack_sdk import WebClient

from database import connection
from models.dto.candle_request_dto import CandleRequestDto
from models.type.interval_type import IntervalType
from models.type.unit_type import UnitType
from module.upbit_module import UpbitModule
from repository.candle_data_repository import CandleDataRepository


class SlackTest(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.slack_token = os.getenv('SLACK_TOKEN')
        self.client = WebClient(token=self.slack_token)
        # response = self.client.chat_postMessage(channel='#public-bot', text="MORE!")
        self.candle_data_repository = CandleDataRepository(connection)
        self.upbit_module = UpbitModule()

    def test_test(self):
        self.client = WebClient(token=self.slack_token)
        response = self.client.chat_postMessage(channel='#public-bot', text="MORE!")
        print(response)

    def test_send_message(self):
        self.client = WebClient(token=self.slack_token)

        candle_request_dto = CandleRequestDto(
            ticker="KRW-BCH"
        )

        data_min30 = self.candle_data_repository.find_all_by_ticker_and_interval(candle_request_dto.ticker,
                                                                                 IntervalType(
                                                                                     UnitType.HALF_HOUR).MINUTE)
        data_hour = self.candle_data_repository.find_all_by_ticker_and_interval(candle_request_dto.ticker,
                                                                                IntervalType(UnitType.HOUR).MINUTE)
        data_hour4 = self.candle_data_repository.find_all_by_ticker_and_interval(candle_request_dto.ticker,
                                                                                 IntervalType(UnitType.HOUR_4).MINUTE)

        message = f"""
{'-' * 40}
        Ticker : {candle_request_dto.ticker}
    
        Profit         : {self.upbit_module.get_profit(candle_request_dto.ticker)}
        Minute30 Stage : {data_min30.iloc[-1]["stage"]}
        Minute60 Stage : {data_hour.iloc[-1]["stage"]}
        Minute240 Stage : {data_hour4.iloc[-1]["stage"]}
        {'-' * 40}"""

        self.client.chat_postMessage(channel='#public-bot', text=message)

    def test_send_df(self):
        df = pd.DataFrame({
            "Ticker": ["KRW-BTC", "KRW-ETH", "KRW-SOL"],
            "Price": [50000000, 3000000, 20000],
            "Volume": [1234, 5678, 91011]
        })
        # Block Kit 메시지 작성
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Ticker Prices and Volume*"
                }
            },
            {"type": "divider"}
        ]

        for _, row in df.iterrows():
            blocks.append({
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Ticker:*\n{row['Ticker']}"},
                    {"type": "mrkdwn", "text": f"*Price:*\n{row['Price']}"},
                    {"type": "mrkdwn", "text": f"*Volume:*\n{row['Volume']}"}
                ]
            })
            blocks.append({"type": "divider"})

        # Slack 메시지 전송
        response = self.client.chat_postMessage(
            channel='#public-bot',
            text="Ticker Prices and Volume",
            blocks=blocks
        )
