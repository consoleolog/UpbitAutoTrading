from contextlib import asynccontextmanager
from fastapi import FastAPI

from scheduler import scheduler, init
from logger import Logger

logger = Logger().get_logger(__name__)



@asynccontextmanager
async def lifespan(app):
    logger.info("========================")
    logger.info("        START UP        ")
    logger.info("========================")
    init()
    scheduler.start()
    yield
    logger.info("========================")
    logger.info("        SHUT DOWN       ")
    logger.info("========================")


app = FastAPI(lifespan=lifespan)