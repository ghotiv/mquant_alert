from web3 import Web3
import json
from see import see

private_key = 'CEC8B042507730E92DC09A08AF4EDD2AA3D893CD34D187CBE4E708D3705F3664'

# infura_url = 'http://127.0.0.1:8545/'
infura_url = 'https://mainnet.infura.io/v3/745c8928dc934545a1056b325e1d0382'
# infura_url = 'https://rinkeby.infura.io/v3/745c8928dc934545a1056b325e1d0382'

def get_w3(infura_url):
    w3 = Web3(Web3.HTTPProvider(infura_url))
    if w3.isConnected():
        return w3
    else:
        return None

W3 = get_w3(infura_url=infura_url)

def get_contract(contract_path,contract_address):
    with open(contract_path, "r") as f:
        info_json = json.load(f)
    abi = info_json['abi']
    contract = W3.eth.contract(
        address=Web3.toChecksumAddress(contract_address), 
        abi=abi
    )
    return contract

def see_contract_fuctions(contract):
    return see(contract.functions)

def contract_functions(contract, func_name, *args, **kwargs):
    res = getattr(contract.functions,func_name)(*args, **kwargs).call()
    return res


