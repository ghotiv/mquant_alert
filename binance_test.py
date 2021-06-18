from pandas.core.frame import DataFrame
from my_ccxt import MyCcxt
from my_conf import *

import arrow,datetime
from matplotlib.pyplot import ylabel
import mplfinance as mpf
import pandas as pd

TZ = 'Asia/Shanghai'

exchange = MyCcxt('','','huobipro')
symbol = 'eth/usdt'
res = exchange.fetch_ohlcv(symbol)
# print(res)

res_list = [{'candle_begin_time':arrow.get(i[0]).to(TZ).datetime,'open':i[1],
            'high':i[2],'low':i[3],'close':i[4],
            'volume':i[5]} for i in res]

df = pd.DataFrame(res_list)

#filter to excel
# df = df[df['volume']>6000]
df_e = df[df['volume']>6000]
df_e['percent'] = (df_e['high']-df_e['low'])/df_e['low']*100
df_e['candle_begin_time'] = df_e['candle_begin_time'].apply(lambda x: str(x))
df_e.to_excel('eth_usdt.xlsx', sheet_name='sheet1', index=True)

#draw k line
df.set_index(['candle_begin_time'],inplace=True)
title = 'tile_k'
my_color = mpf.make_marketcolors(up='red',down='green',edge='inherit')
my_style = mpf.make_mpf_style(marketcolors=my_color)
# add_plot = [mpf.make_addplot(df[['ma10','ma50']])]
mpf.plot(df, type='candle', volume=True, title=title, ylabel="price(usdt)", style=my_style,
            ylabel_lower="volume")
