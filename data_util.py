import requests
import json

URL_GRAPH='https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v3-testing'

def get_graphs(query,url=URL_GRAPH):
    return requests.post(url,json={'query': query}).json()

def get_pool_prices():
    pool_dict = {
        #eth-usdt
        'eth/usdt':'0x4e68ccd3e89f51c3074ca5072bbac773960dfa36',
        # 'wbtc':'0x9db9e0e53058c89e5b94e29621a205198648425b',
        #uni-usdt
        'uni/usdt':'0x3470447f3cecffac709d3e783a307790b0208d60',
        #lin-usdc
        'link/usdt':'0xfad57d2039c21811c8f2b5d5b65308aa99d31559',
        'uni/eth':'0x1d42064fc4beb5f8aaf85f4617ae8b3b5b8bd801',
        'link/eth':'0xa6cc3c2531fdaa6ae1a3ca84c2855806728693e8',
    }
    pools = list(pool_dict.values())
    pools_str = ','.join(['"'+str(i)+'"' for i in pools])
    print(pools_str)
    query = """
        query pools {
            pools(where: {id_in: [%s]}){
                token1Price
                token0{
                    symbol
                }
                token1{
                    symbol
                }
            }
        }
    """%pools_str
    res = get_graphs(query)
    pools = res['data']['pools']
    prices = [{'symbol':str(i['token0']['symbol'])+'/'+str(i['token1']['symbol']),
                'price':float(i['token1Price'])}
                for i in pools]
    for i in prices:
        if i['symbol']=='UNI/WETH':
            i['symbol']='ETH/UNI'
            i['price']=1/i['price']
        if i['symbol']=='LINK/WETH':
            i['symbol']='ETH/LINK'
            i['price']=1/i['price']
    for i in prices:
        i['price']=round(float(i['price']),5)
    for i in prices:
        i['symbol']=i['symbol'].replace('WETH','ETH').replace('USDC','USDT') 
    return prices

