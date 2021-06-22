from brownie import accounts, AlphaStrategy
from brownie.network.gas.strategies import GasNowScalingStrategy
import os
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

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

keeper = accounts.load('deployer')
gas_strategy = GasNowScalingStrategy()
strategy = AlphaStrategy.at('0xAc9AcD08c7D034EfcFf29F3AB5582E4d317071B0')

def rinkeby_rebalance():
    tick = strategy.getTick()
    lastTick = strategy.lastTick()
    shouldRebalance = abs(tick - lastTick) > 100
    if shouldRebalance:
        res= 'Rebalancing...'
        strategy.rebalance({"from": keeper, "gas_price": gas_strategy})
    else:
        res = 'Deviation too low so skipping'
    return res

@app.get("/rinkeby_rebalance")
async def fast_rinkeby_rebalance():
    res = rinkeby_rebalance()
    return res

uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info")