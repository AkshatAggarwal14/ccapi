from fastapi import FastAPI
import codechef
import time
# import scrape from scraper
app = FastAPI()


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
