# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager
from fastapi import FastAPI
from logger import LoggerFactory
from scheduler import trade_scheduler

logger = LoggerFactory().get_logger("server", "UpbitTrading")

@asynccontextmanager
async def lifespan(app):
    logger.info("==================")
    logger.info("     START UP     ")
    logger.info("==================")
    trade_scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)