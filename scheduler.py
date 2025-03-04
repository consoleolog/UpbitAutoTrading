# -*- coding: utf-8 -*-
import uuid
import trade
from constant import TimeFrame
from apscheduler.schedulers.background import BackgroundScheduler

trade_scheduler = BackgroundScheduler()
tickers = [
    "BTC/KRW",
    "ETH/KRW",
    "BCH/KRW",
    "SOL/KRW",
    "AAVE/KRW",
    "BSV/KRW"
]
trade_scheduler.add_job(
    func=trade.loop,
    trigger='interval',
    minutes=TimeFrame.KEYS[TimeFrame.MINUTE_10],
    kwargs={
        "timeframe": TimeFrame.MINUTE_15,
        "tickers": tickers
    },
    id=str(uuid.uuid4())
)