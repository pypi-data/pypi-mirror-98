from typing import List, Optional
import os
import pandas as pd

from sqlalchemy.orm import Session
from .database import SessionLocal, engine, create_table, query_to_db

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException

import asyncio
from aiocache import cached, Cache
import uvicorn
import typer


typer_app = typer.Typer()
app = FastAPI()
cache = Cache.MEMORY(timeout=None)


async def read_csv(file):
    "Receives the file as a parameter and returns the dataframe"
    data = file.file
    table_name = file.filename.split(".csv")[0]
    df = pd.read_csv(file.filename)
    df = df.convert_dtypes()
    return table_name, df

async def evict_cache(table_name):
    "When data set is changed, the cache evict"
    old_cache = cache._cache.copy()
    if old_cache:
        for key in old_cache:
            if table_name in key: 
                await cache.delete(key)


def get_db():
    "db session for time using orm"
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_engine():
    "Engine for direct query"
    engine = engine()
    try:
        yield engine
    finally:
        engine.close()


@app.get("/")
def read_root():
    return { "Hello": "World" }

@app.post("/table")
async def create_upload_csvfiles(files: List[UploadFile] = File(...)):
    "Upload csvfile to sqlite table"
    UPLOAD_DIRECTORY = "./"
    return_dict = {}
    for file in files:
        if file.filename.endswith('.csv'):
            table_name, df = await read_csv(file)
            await evict_cache(table_name)
            result = await create_table(engine, table_name, df)
            return_dict[table_name] = result
    return {"upload success": return_dict}


@app.get("/cache")
async def read_cache():
    "Check what's in the cache"
    return cache._cache

@app.get("/cache/clear")
async def clear_cache():
    await cache.clear()
    return "{cleared : True}"

@app.get("/table")
async def read_table_list():
    q = "SELECT name FROM sqlite_master WHERE type='table'"
    try:
        query_result = await asyncio.wait_for(query_to_db(engine, q), timeout=600)
        return query_result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="408 Request Timeout")


@app.get("/table/")
async def read_table(table_name: str, where: Optional[str] = None, select: Optional[str] = None, limit: Optional[int] = None,):
    "As parameters, table name, filter, column name to be loaded, number of rows to be called, and query result in db"
    q = f"SELECT * FROM {table_name}"
    if select:
        q= f"SELECT {select} FROM {table_name}"
    if where:
        q += f" where {where}"
    if limit:
        q += f" limit {limit}"

    if await cache.exists(q):
        return await cache.get(q)

    try:
        query_result = await asyncio.wait_for(query_to_db(engine, q), timeout=600)
        await cache.set(q, query_result)
        return query_result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="408 Request Timeout")


@typer_app.command()
def main(
    host: str = typer.Option("127.0.0.1", help="IP to run the API on"),
    port: int = typer.Option(8000, help="Port to run the API on"),
):
    """Simple command line interface that starts an API"""
    typer.echo("🦄 Starting with uvicorn...")
    typer.echo(
        "💡 Check out the API docs at "
        + typer.style(f"http://{host}:{port}/docs", bold=True)
    )
    typer.echo("-" * 80)
    uvicorn.run(app, host="127.0.0.1", port=8000)
