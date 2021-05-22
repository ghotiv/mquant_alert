import requests
import json
import arrow
from twisted.internet import reactor
from apscheduler.schedulers.twisted import TwistedScheduler

TZ = 'Asia/Shanghai'

# url_search = 'https://debank.com/profile/0x2f591ddf47366c899bab6c9e73668898fbc47d75'
#交易记录
url_trade = 'https://api.debank.com/history/list?chain=eth&user_addr=0x2f591ddf47366c899bab6c9e73668898fbc47d75'
#钱包的币
url_wallet = 'https://api.debank.com/token/balance_list?user_addr=0x2f591ddf47366c899bab6c9e73668898fbc47d75'
#v3 币对和价格
# url = 'https://api.debank.com/portfolio/project_list?user_addr=0x2f591ddf47366c899bab6c9e73668898fbc47d75'
#v3 币对和价格 代流量 
url_v3 = 'https://api.debank.com/portfolio/list?project_id=uniswap3&user_addr=0x2f591ddf47366c899bab6c9e73668898fbc47d75'


def get_time_now():
    return arrow.utcnow().to(TZ).format('YYYY-MM-DD HH:mm:ss')

def get_r(url):
    res = requests.get(url).json()
    return res

def format_digit(x):
    return str(round(x,2)) if str(x).replace('.','').isdigit() else str(x)

def format_msg(lia):
    return ' '.join(map(format_digit,lia))+'\n'

def get_wallet_balance():
    res_wallet = get_r(url_wallet)
    res_wallets = res_wallet['data']
    # print(res_wallets)
    wallets = []
    for i in res_wallets:
        # balance/10**decimals
        amount = i['balance']/10**i['decimals']
        asset = amount*i['price']
        wallet_dict = {'symbol':i['symbol'],'price':i['price'],'amount':amount,'asset':asset}
        # print('钱包币种',wallet_dict['symbol'],'价格',wallet_dict['price'],'数量',wallet_dict['amount'],'金额',wallet_dict['asset'])
        if wallet_dict['asset']<100:
            continue
        wallets.append(wallet_dict)
    return wallets

def get_v3_balance():
    res_wallet = get_r(url_v3)
    ticks = res_wallet['data']['portfolio_list']
    # print(res_wallets)
    wallets = []
    for i in ticks:
        tick_asset = i['stats']['asset_usd_value']
        tick_symbol = i['detail']['supply_token_list'][0]
        # print('tick --币种',tick_symbol['symbol'],'数量',tick_symbol['amount'],'单价',tick_symbol['price'],
        #             '金额',tick_symbol['amount']*tick_symbol['price'])
        tick_symbol_swap = i['detail']['supply_token_list'][1]
        # print('tick --交换币种',tick_symbol_swap['symbol'],'数量',tick_symbol_swap['amount'],'单价',tick_symbol_swap['price'],
        #             '金额',tick_symbol_swap['amount']*tick_symbol_swap['price'])
        wallet_dict = {'asset':tick_asset,
                        'tick_symbol':{'symbol':tick_symbol['symbol'],
                                        'amount':tick_symbol['amount'],
                                        'price':tick_symbol['price'],
                                        'asset':tick_symbol['amount']*tick_symbol['price']},
                        'tick_symbol_swap':{'symbol':tick_symbol_swap['symbol'],
                                            'amount':tick_symbol_swap['amount'],
                                            'price':tick_symbol_swap['price'],
                                            'asset':tick_symbol_swap['amount']*tick_symbol_swap['price']},
                        }
        wallets.append(wallet_dict)
    return wallets

def send_msg(message):
    print(message)
    access_token = 'a90e59df9171db94c8416423b648840929ffcc95b418ca0a2bfbdd398ecc5de3'
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s'%access_token
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8"
    }
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [
                #如果需要@某人，这里写他的手机号
                "13603053095"                                    
            ],
             #如果需要@所有人，这些写1
            "isAtAll": 1                                        #如果需要@所有人，这些写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)

def get_balances():
    res = ''
    msg = ''
    time_now = get_time_now()
    msg = msg + format_msg(['当前时间',time_now])
    print('当前时间',time_now)

    wallets = get_wallet_balance()
    
    for wallet_dict in wallets:
        msg = msg + format_msg(['钱包币种',wallet_dict['symbol'],'价格',wallet_dict['price'],'数量',
                    wallet_dict['amount'],'金额',wallet_dict['asset']])

    wallet_asset = sum([i['asset'] for i in wallets])
    msg = msg + format_msg(['钱包资产',wallet_asset])
    print('钱包资产',wallet_asset)

    v3_wallets = get_v3_balance()
    for i in v3_wallets:
        # print(i)
        tick_symbol = i['tick_symbol']
        tick_symbol_swap = i['tick_symbol_swap']
        tick_asset = i['asset']
        msg = msg + format_msg(['tick --币种',tick_symbol['symbol'],'数量',tick_symbol['amount'],'单价',tick_symbol['price'],
                    '金额',tick_symbol['amount']*tick_symbol['price']])
        msg = msg + format_msg(['tick --交换币种',tick_symbol_swap['symbol'],'数量',tick_symbol_swap['amount'],'单价',tick_symbol_swap['price'],
                    '金额',tick_symbol_swap['amount']*tick_symbol_swap['price']])

    v3_asset = sum([i['asset'] for i in v3_wallets])
    msg = msg + format_msg(['v3资产',v3_asset])
    print('v3资产',v3_asset)

    total_asset = wallet_asset + v3_asset
    msg = msg + format_msg(['总资产',total_asset])
    print('总资产',total_asset)

    print(msg)
    send_msg(msg)

    return res


if __name__ == '__main__':
    get_balances()
    # scheduler = TwistedScheduler()
    # # scheduler.add_job(main, 'interval', seconds=20, max_instances=1, kwargs={})
    # # scheduler.add_job(get_balances, 'cron', minute = '*/1')
    # scheduler.add_job(get_balances, 'cron', hour = '*/1')
    # scheduler.start()
    # reactor.run()
