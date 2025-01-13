from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from pydantic import BaseModel
from scheduler import scheduler, create_table_if_not_exist
from logger import Logger

logger = Logger().get_logger(__name__)

@asynccontextmanager
async def lifespan(app):
    logger.info("========================")
    logger.info("        START UP        ")
    logger.info("========================")
    create_table_if_not_exist()
    scheduler.start()
    logger.info("========================")

    logger.info("========================")
    yield

app = FastAPI(lifespan=lifespan)

class HealthCheck(BaseModel):
    status: str = "OK"
@app.get(
    "/health",
    tags=["health_check"],
    summary="Perform a Health Check",
    response_description="Return Http Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def health_check():
    return HealthCheck(status="OK")