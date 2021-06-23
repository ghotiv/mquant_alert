from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from data_util import get_pool_prices,get_tick,get_twap,\
       get_tick_twap_gap
from calc_util import get_av_args

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://183.61.252.7",
    "http://183.61.252.7:8000",
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # Credentials (Authorization headers, Cookies, etc)
    allow_credentials=True,
    # Specific HTTP methods (POST, PUT) or all of them with the wildcard "*".
    allow_methods=["*"],
    # Specific HTTP headers or all of them with the wildcard "*".
    allow_headers=["*"],
)

@app.get("/get_pool_prices")
async def fast_get_pool_prices():
    res = get_pool_prices()
    return res

@app.get("/get_tick")
async def fast_get_tick():
    res = get_tick()
    return res

@app.get("/get_twap")
async def fast_get_twap(twap_duration: int=60):
    res = get_twap(twap_duration=twap_duration)
    return res

@app.get("/get_tick_twap_gap")
async def fast_get_tick_twap_gap(twap_duration: int=60):
    res = get_tick_twap_gap(twap_duration=twap_duration)
    return res

@app.get("/get_av_args")
async def fast_get_av_args(bt:int=2977,lt:int=577,amount0:float=92.387,\
        amount1:float=280000.0,tick: int=None):
    if not tick:
        tick = get_tick()
    res = get_av_args(bt,lt,amount0,amount1,tick)
    return res