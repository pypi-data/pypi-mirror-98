from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import json
import pandas as pd

SQLALCHEMY_DATABASE_URL = "sqlite:///./main.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def create_table(engine, table_name, df):
    "Create a data frame as a table"
    try:
        df.to_sql(f"{table_name}", con=engine, if_exists='replace',)
        return True
    except Exception as e:
        print(e)

async def query_to_db(engine, sql_query):
    """Executes a SQL query on the database and returns rows as list of dicts."""
    cur = engine.execute(sql_query)
    dicts = cur.fetchall()
    return dicts

