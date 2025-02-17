import pandas as pd
import psycopg2

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from dto import OrderInfo

load_dotenv()
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT")
db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(db_url)

conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port,
)

async def insert_order(order_info: OrderInfo):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO UPBIT_ORDER(TICKER, PRICE, SIDE)
        VALUES (%s, %s, %s);
        """,(order_info.market, order_info.locked, order_info.side),
    )
    conn.commit()
    cur.close()

def get_buy_order(_ticker):
    ticker = _ticker.split("/")[1] + "-" + _ticker.split("/")[0]
    sql = """
    SELECT O.ORDER_ID,
           O.TICKER,
           O.PRICE,
           O.SIDE,
           O.CREATED_AT
    FROM UPBIT_ORDER AS O
    WHERE O.TICKER = %(ticker)s
    AND O.SIDE = 'bid'
    ORDER BY O.CREATED_AT DESC;
    """
    params = {"ticker": ticker}
    return pd.read_sql(sql, engine, params=params)

