# -*- coding: utf-8 -*-
import uuid
import trade
from constant import TimeFrame
from apscheduler.schedulers.background import BackgroundScheduler

trade_scheduler = BackgroundScheduler()
trade_scheduler.add_job(
    func=trade.loop,
    trigger='interval',
    minutes=2,
    kwargs={
        "timeframe": TimeFrame.MINUTE_15,
        "tickers": [
            "BTC/KRW",
            "ETH/KRW",
            "BCH/KRW",
            "SOL/KRW",
            "ETC/KRW",
        ]
    },
    id=str(uuid.uuid4())
)