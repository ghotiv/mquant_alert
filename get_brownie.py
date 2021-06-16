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

pool = get_pool()

# uvicorn.run("example:app", host="127.0.0.1", port=5000, log_level="info")

def get_twap(pool,twap_duration=60):
    tickCumulatives,_ = pool.observe([twap_duration,0])
    res = (tickCumulatives[1] - tickCumulatives[0])/twap_duration
    return res




