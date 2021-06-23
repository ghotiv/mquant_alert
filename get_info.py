from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from data_util import get_pool_prices,get_tick,get_twap,\
       get_tick_twap_gap
from calc_util import get_av_args,get_tick_by_price,get_price_by_tick

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

@app.get("/get_av_args")
async def fast_get_av_args(bt:int=3600,lt:int=1200,
            amount0:float=92.387, amount1:float=280000.0, tick:float=None):
    if not tick:
        tick = get_tick()
    res = get_av_args(bt,lt,amount0,amount1,tick)
    return res

@app.get("/get_av_args_by_price")
async def fast_get_av_args(base_price_percent:float=43.75,limit_price_percent:float=12.76,
            amount0:float=114.65, amount1:float=222530.63, current_price: float=None):
    if not current_price:
        tick = get_tick()
        current_price = get_price_by_tick(tick)
    else:
        tick = get_tick_by_price(current_price)
    bt_price_add = get_tick_by_price(current_price*(1+base_price_percent/100.0))
    lt_price_add = get_tick_by_price(current_price*(1+limit_price_percent/100.0))
    bt = abs(bt_price_add-tick)
    lt = abs(lt_price_add-tick)
    res = get_av_args(bt,lt,amount0,amount1,tick)
    return res

@app.get("/manual_rebalance")
async def fast_manual_rebalance(last_price:float,limit_price_lower:float=None,
            limit_price_upper:float=None):
    current_price = get_price_by_tick(get_tick())
    if not limit_price_lower and not limit_price_upper:
        limit_percent = 3.19/100.0
    if limit_price_lower and current_price:
        limit_percent = abs(current_price-limit_price_lower)/min(current_price,limit_price_lower)
    current_price_percent = abs(current_price-last_price)/min(current_price,last_price)
    res = current_price_percent > limit_percent
    return res

