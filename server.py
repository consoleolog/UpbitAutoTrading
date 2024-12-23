from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///trade.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)

from fastapi import FastAPI

from run_scheduler import scheduler


@asynccontextmanager
async def lifespan(app):
    scheduler.start()
    yield
    print("lifespan finished")

app = FastAPI(lifespan=lifespan)

@app.on_event("startup")
async def startup():
    pass