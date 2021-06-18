import arrow
import time
import requests
from log_util import logger
TZ = 'Asia/Shanghai'

def cron_get_twap_gap():
    time_now = arrow.utcnow().to(TZ).format('YYYY-MM-DD_HH:mm:ss')
    url = 'http://8.211.165.131:8008/get_twap_gap?twap_duration=60'
    r = requests.get(url)
    logger.info(r.json())

while 1:
    time.sleep(5)
    try:
        cron_get_twap_gap()
    except as e:
        print(e)



