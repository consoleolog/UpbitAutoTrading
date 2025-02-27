# -*- coding: utf-8 -*-
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine

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

def init_status(ticker):
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO UPBIT_STATUS(TICKER)
            VALUES (%s);
            """, (ticker,)
        )
        conn.commit()
        cur.close()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()

def update_status(ticker, price, side):
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE UPBIT_STATUS
        SET PRICE = %s,
            SIDE = %s,
            UPDATED_AT = NOW()
        WHERE UPBIT_STATUS.TICKER = %s;
        """,(price, side, ticker)
    )
    conn.commit()
    cur.close()

def get_status(ticker):
    sql = """
    SELECT S.TICKER,
           S.PRICE,
           S.SIDE,
           S.CREATED_AT,
           S.UPDATED_AT
    FROM UPBIT_STATUS AS S 
    WHERE S.TICKER = %(ticker)s
    """
    params = {"ticker": ticker}
    data = pd.read_sql(sql, engine, params=params)
    return data.iloc[-1]