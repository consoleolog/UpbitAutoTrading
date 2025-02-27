# -*- coding: utf-8 -*-
import psycopg2.errors

import mapper
from contextlib import asynccontextmanager
from fastapi import FastAPI
from logger import LoggerFactory
from scheduler import trade_scheduler, tickers

logger = LoggerFactory().get_logger("server", "UpbitTrading")

def ticker_init():
    for ticker in tickers:
        mapper.init_status(ticker)


@asynccontextmanager
async def lifespan(app):
    logger.info("==================")
    logger.info("     START UP     ")
    logger.info("==================")
    ticker_init()
    trade_scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)