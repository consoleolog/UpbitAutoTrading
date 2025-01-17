import os

import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

connection = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PWD'),
    port=os.getenv('DB_PORT'),
)

db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PWD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(db_url)