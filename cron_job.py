import arrow
import time
import requests
TZ = 'Asia/Shanghai'

# while 1:
#     time.sleep(3)
time_now = arrow.utcnow().to(TZ).format('YYYY-MM-DD HH:mm:ss ZZ')

url = 'http://8.211.165.131:8008/get_twap_gap?twap_duration=60'
r = requests.get(url)
print(time_now,r.json())



