from fastapi import FastAPI
import codechef
import time
from scraper import scrape
import asyncio
import os
import shutil
from fastapi.openapi.utils import get_openapi
app = FastAPI(title="Unofficial Codechef Api", redoc_url="/")


@app.get("/gimme")
async def gimme(handle, level: str):
    resp = await codechef.gimme(handle, level)
    return resp


@app.get("/stalk")
async def stalk(handle: str, limit: int = 120):
    resp = await codechef.stalk(handle, limit)
    return resp


@app.get("/upsolve")
async def upsolve(handle: str, limit: int = 50):
    resp = await codechef.upsolve(handle, limit)
    return resp


@app.on_event("startup")
async def startup():
    try:
        os.mkdir("data")
    except FileExistsError:
        shutil.rmtree("data")
        os.mkdir("data")
    await scrape()


@app.on_event("shutdown")
def shutdown():
    shutil.rmtree("data")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Unofficial Codechef API",
        version="1.1.0",
        description="",
        routes=app.routes,
    )
    print(openapi_schema["info"])
    openapi_schema["info"]["x-logo"] = {
        "url": "https://imgur.com/a/BaXuCsh"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
