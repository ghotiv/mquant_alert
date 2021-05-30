import requests
import json
import arrow
import talib as ta
import numpy as np

URL_GRAPH='https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v3-testing'

def get_graphs(query,url=URL_GRAPH):
    return requests.post(url,json={'query': query}).json()

query = '''
{
	poolDayDatas(where: {pool__id_in: ["0x4e68ccd3e89f51c3074ca5072bbac773960dfa36"]}){
    id
    date
    pool {
      id
    }
    liquidity
    sqrtPrice
    token0Price
    token1Price
    tick
    tvlUSD
    volumeToken0
    volumeToken1
    volumeUSD
    txCount
  }
}
'''

query = '''
query transactions($address: Bytes="0x4e68ccd3e89f51c3074ca5072bbac773960dfa36") {
  swaps(
    first: 100
    orderBy: timestamp
    orderDirection: desc
    where: {pool: $address}
  ) {
    timestamp
    transaction {
      id
      __typename
    }
    pool {
      token0 {
        id
        symbol
        __typename
      }
      token1 {
        id
        symbol
        __typename
      }
      __typename
    }
    origin
    amount0
    amount1
    amountUSD
    __typename
  }
}
'''

query = '''
query ($timestamp: Int=1620835200, $token: String="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2") {
  tokenDayDatas(where: {token: $token, date_gt: $timestamp}) {
    priceUSD
    __typename
  }
}
'''

res = get_graphs(query)
# print(res)
prices = [i['priceUSD'] for i in res['data']['tokenDayDatas']]
print(prices)
prices = [float(i) for i in prices if float(i)]
lib = np.array(prices)

u, m, l = ta.BBANDS(
                lib,
                timeperiod=len(prices),
                # number of non-biased standard deviations from the mean
                nbdevup=2,
                nbdevdn=2,
                # Moving average type: simple moving average here
                matype=0)
print(u, m, l)

# for i in res['data']['swaps'][:10]:
#     print(arrow.get(int(i['timestamp'])),i['amount1'])

