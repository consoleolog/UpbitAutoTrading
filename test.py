import os

import psycopg2
from dotenv import load_dotenv

from mappers import CandleMapper, OrderMapper
from services import CandleService, OrderService

load_dotenv()

connection = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PWD'),
    port=os.getenv('DB_PORT'),
)

candle_service = CandleService(
    connection=connection,
    candle_mapper=CandleMapper()
)

order_service = OrderService(
    connection=connection,
    order_mapper=OrderMapper()
)

def init():
    candle_service.init()
    order_service.init()





