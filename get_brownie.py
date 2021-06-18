import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from brownie import project

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://183.61.252.7",
    "http://183.61.252.7:8000",
    "http://8.211.165.131",
    "http://8.211.165.131:8005",
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

def get_pool():
    factory_address = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
    UniswapV3Core = project.load("Uniswap/uniswap-v3-core@1.0.0")
    eth = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    usdc = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
    factory = UniswapV3Core.interface.IUniswapV3Factory(factory_address)
    pool = UniswapV3Core.interface.IUniswapV3Pool(factory.getPool(eth, usdc, 3000))
    return pool

def get_twap(twap_duration=60,pool=None):
    if not pool:
        pool = get_pool()
    tickCumulatives,_ = pool.observe([twap_duration,0])
    res = (tickCumulatives[1] - tickCumulatives[0])/twap_duration
    return res

def get_twap_gap(twap_duration=60,pool=None):
    if not pool:
        pool = get_pool()
    twap = get_twap(twap_duration,pool)
    tick = pool.slot0()[1]
    res = abs(twap-tick)
    return res

@app.get("/get_twap")
async def fast_get_twap(twap_duration: int=60):
    res = get_twap(twap_duration=twap_duration)
    return res

@app.get("/get_twap_gap")
async def fast_get_twap(twap_duration: int=60):
    res = get_twap_gap(twap_duration=twap_duration)
    return res

@app.get("/get_pool_prices")
async def fast_get_pool_prices():
    res = {'a':1,'b':2}
    return res

uvicorn.run(app, host="0.0.0.0", port=8008, log_level="info")





