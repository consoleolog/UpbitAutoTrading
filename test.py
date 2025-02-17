import platform

import ccxt.pro as ccxtpro
import asyncio
import datetime

import exchange
from dto import TickerInfo
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

queue = asyncio.Queue()  # 비동기 Queue 생성
