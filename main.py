from fastapi import FastAPI
import codechef, time
#import scrape from scraper
app = FastAPI()

@app.get("/gimme")
async def gimme(handle, level: str):
    resp = await codechef.gimme(handle, level)
    return resp


@app.get("/stalk")
async def stalk(handle: str, limit: int = 5):
    resp = await codechef.stalk(handle, limit)
    return resp


@app.get("/upsolve")
async def upsolve(handle):
    resp = await codechef.upsolve(handle)
    return resp