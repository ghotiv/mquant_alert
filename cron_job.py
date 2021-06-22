import arrow
import time
import requests
from web3_util import get_contract,contract_functions,\
            see_contract_fuctions
from log_util import logger
TZ = 'Asia/Shanghai'

alpha_address = '0x40C36799490042b31Efc4D3A7F8BDe5D3cB03526'
contract_as = get_contract('contracts/AlphaStrategy.json',alpha_address)

def cron_get_twap_gap():
    # time_now = arrow.utcnow().to(TZ).format('YYYY-MM-DD_HH:mm:ss')
    # url = 'http://8.211.165.131:8008/get_twap_gap?twap_duration=60'
    # r = requests.get(url)
    # logger.info(r.json())
    bt = contract_functions(contract_as,'baseThreshold')
    lt = contract_functions(contract_as,'limitThreshold')
    tick = contract_functions(contract_as,'getTick')
    last_tick = contract_functions(contract_as,'lastTick')
    twap = contract_functions(contract_as,'getTwap')
    twap_duration = contract_functions(contract_as,'twapDuration')
    max_twap_deviation = contract_functions(contract_as,'maxTwapDeviation')

    deviation = abs(tick - twap)
    should_rebalance = abs(tick - last_tick) > lt // 4
    logger.info('should_rebalance,last_tick_gap,lt//4', should_rebalance, abs(tick - last_tick), lt // 4)
    logger.info('last_tick',tick,last_tick,abs(tick - last_tick))
    logger.info('tick_twap_gap,max',tick,twap,deviation,max_twap_deviation)
    

while 1:
    time.sleep(5)
    try:
        cron_get_twap_gap()
    except Exception as e:
        print(e)



