import requests
import json

URL_GRAPH='https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v3-testing'

def get_graphs(query,url=URL_GRAPH):
    return requests.post(url,json={'query': query}).json()

def get_pool_prices():
    pool_dict = {
        #eth-usdt
        'eth':'0x4e68ccd3e89f51c3074ca5072bbac773960dfa36',
        # 'wbtc':'0x9db9e0e53058c89e5b94e29621a205198648425b',
        #uni-usdt
        'uni':'0x3470447f3cecffac709d3e783a307790b0208d60',
        #lin-usdc
        'link':'0xfad57d2039c21811c8f2b5d5b65308aa99d31559',
    }
    pools = list(pool_dict.values())
    pools_str = ','.join(['"'+str(i)+'"' for i in pools])
    query = """
        query pools {
            pools(where: {id_in: [%s]}){
                token1Price
                token0{
                    symbol
                }
            }
        }
    """%pools_str
    res = get_graphs(query)
    pools = res['data']['pools']
    prices = [{'symbol':i['token0']['symbol'],'price':round(float(i['token1Price']),5)} 
                for i in pools]
    return prices

