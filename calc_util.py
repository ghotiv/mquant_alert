from math import floor, sqrt
import math
import time
from decimal import Decimal

MIN_TICK = -887272
MAX_TICK = -MIN_TICK

MIN_SQRT_RATIO = 4295128739
MAX_SQRT_RATIO = 1461446703485210103287273052203988822378723970342

# Q96 = 0x1000000000000000000000000
Q96 = Decimal('79228162514264337593543950336')
# Q128 = 0x100000000000000000000000000000000
Q128 = Decimal('340282366920938463463374607431768211456')

#validate
def get_sqrtPriceX96_by_tick(tick):
    # -200880
    absTick = abs(tick)
    # absTick = tick < 0 ? uint256(-int256(tick)) : uint256(int256(tick))
    # ratio = absTick & 0x1 != 0 ? 0xfffcb933bd6fad37aa2d162d1a594001 : 0x100000000000000000000000000000000
    ratio = 0xfffcb933bd6fad37aa2d162d1a594001 if absTick & 0x1 != 0 else 0x100000000000000000000000000000000
    if (absTick & 0x2 != 0):
        ratio = (ratio * 0xfff97272373d413259a46990580e213a) >> 128
    if (absTick & 0x4 != 0):
        ratio = (ratio * 0xfff2e50f5f656932ef12357cf3c7fdcc) >> 128
    if (absTick & 0x8 != 0):
        ratio = (ratio * 0xffe5caca7e10e4e61c3624eaa0941cd0) >> 128
    if (absTick & 0x10 != 0):
        ratio = (ratio * 0xffcb9843d60f6159c9db58835c926644) >> 128
    if (absTick & 0x20 != 0):
        ratio = (ratio * 0xff973b41fa98c081472e6896dfb254c0) >> 128
    if (absTick & 0x40 != 0): 
        ratio = (ratio * 0xff2ea16466c96a3843ec78b326b52861) >> 128
    if (absTick & 0x80 != 0): 
        ratio = (ratio * 0xfe5dee046a99a2a811c461f1969c3053) >> 128
    if (absTick & 0x100 != 0): 
        ratio = (ratio * 0xfcbe86c7900a88aedcffc83b479aa3a4) >> 128
    if (absTick & 0x200 != 0): 
        ratio = (ratio * 0xf987a7253ac413176f2b074cf7815e54) >> 128
    if (absTick & 0x400 != 0): 
        ratio = (ratio * 0xf3392b0822b70005940c7a398e4b70f3) >> 128
    if (absTick & 0x800 != 0): 
        ratio = (ratio * 0xe7159475a2c29b7443b29c7fa6e889d9) >> 128
    if (absTick & 0x1000 != 0): 
        ratio = (ratio * 0xd097f3bdfd2022b8845ad8f792aa5825) >> 128
    if (absTick & 0x2000 != 0): 
        ratio = (ratio * 0xa9f746462d870fdf8a65dc1f90e061e5) >> 128
    if (absTick & 0x4000 != 0): 
        ratio = (ratio * 0x70d869a156d2a1b890bb3df62baf32f7) >> 128
    if (absTick & 0x8000 != 0): 
        ratio = (ratio * 0x31be135f97d08fd981231505542fcfa6) >> 128
    if (absTick & 0x10000 != 0): 
        ratio = (ratio * 0x9aa508b5b7a84e1c677de54f3e99bc9) >> 128
    if (absTick & 0x20000 != 0): 
        ratio = (ratio * 0x5d6af8dedb81196699c329225ee604) >> 128
    if (absTick & 0x40000 != 0): 
        ratio = (ratio * 0x2216e584f5fa1ea926041bedfe98) >> 128
    if (absTick & 0x80000 != 0): 
        ratio = (ratio * 0x48a170391f7dc42444e8fa2) >> 128
    if (tick > 0):
        ratio = (2**256 - 1) / ratio
    sqrtPriceX96 = (ratio >> 32) + (0 if ratio % (1 << 32) == 0 else 1)
    return sqrtPriceX96

def getPrice(pool):
    sqrtPrice = pool.slot0()[0] / (1 << 96)
    return sqrtPrice ** 2

def get_sqrtPriceX96(price, decimal0=1e18, decimal1=1e6):
    price = Decimal(str(price))*Decimal(str(decimal1))/Decimal(str(decimal0))
    res = price.sqrt() * Decimal(str((1 << 96)))
    res = str(res).split('.')[0]
    return res

def get_price_by_x96(sqrtPriceX96, decimal0=1e18, decimal1=1e6):
    return floor(((sqrtPriceX96/(1 << 96))**2)/(decimal0/decimal1))

# def get_price_by_x96(sqrtPriceX96, decimal0=1e18, decimal1=1e6):
#     sqrtPrice = sqrtPriceX96 / (1 << 96)
#     return sqrtPrice**2*(decimal0/decimal1)

# def get_tick_by_price(price, decimal0=1e18, decimal1=1e6, base_price=1.0001):
#     price = price*decimal1/decimal0
#     tick = math.log(price, base_price)
#     # tick = math.ceil(tick/tick_spacing)*tick_spacing
#     return tick

def get_tick_by_price(price, decimal0=1e18, decimal1=1e6, base_price=Decimal('1.0001')):
    price = Decimal(str(price))*Decimal(str(decimal1))/Decimal(str(decimal0))
    tick = round(math.log(price, base_price))
    # tick = math.ceil(tick/tick_spacing)*tick_spacing
    return tick

# def get_tick_by_price(price, tick_spacing=60, decimal0=1e18, decimal1=1e6, base_price=1.0001):
#     price = price*decimal1/decimal0
#     tick = math.log(price, base_price)
#     tick = math.ceil(tick/tick_spacing)*tick_spacing
#     return tick

# def get_tick_by_x96(sqrtPriceX96, decimal0=1e18, decimal1=1e6):
#     price = get_price_by_x96(sqrtPriceX96, decimal0=decimal0, decimal1=decimal1)
#     tick = get_tick_by_price(price, decimal0=decimal0, decimal1=decimal1)
#     print(price,tick)
#     return tick

def get_price_by_tick(tick, decimal0=1e18, decimal1=1e6, base_price=1.0001):
    return base_price**tick*decimal0/decimal1

def mul_div(a,b,denominator):
    res = Decimal(str(a))*Decimal(str(b))/Decimal(str(denominator))
    # print('res00',res)
    # res = str(res).split('.')[0]
    return res

def get_min_max(ax,bx):
    return (min(ax,bx),max(ax,bx))

def get_l_by_amount0(ax,bx,amount0):
    ax,bx = get_min_max(ax,bx)
    im = Decimal(mul_div(ax,bx,Q96))
    l = mul_div(amount0,im,bx-ax)
    return l

def get_l_by_amount1(ax,bx,amount1):
    ax,bx = get_min_max(ax,bx)
    l = mul_div(amount1,Q96,bx-ax)
    return l

def get_l_by_amount01(x,ax,bx,amount0,amount1):
    ax,bx = get_min_max(ax,bx)
    if x<=ax:
        l = get_l_by_amount0(ax,bx,amount0)
    if ax<x<bx:
        l0 = get_l_by_amount0(x,bx,amount0)
        l1 = get_l_by_amount1(ax,x,amount1)
        l = min(l0,l1)
    if x>=bx:
        l = get_l_by_amount0(ax,bx,amount1)
    return l

def get_amount0_by_l(ax,bx,l):
    ax,bx = get_min_max(ax,bx)
    amount0 = Decimal(mul_div(Decimal(str(l*Decimal(str(2**96)))),bx-ax,bx))/ax
    return amount0

def get_amount1_by_l(ax,bx,l):
    ax,bx = get_min_max(ax,bx)
    amount1 = Decimal(mul_div(l,bx-ax,Q96))
    return amount1

def get_amount01_by_l(x,ax,bx,l,decimal0=1e18, decimal1=1e6):
    amount0 = 0
    amount1 = 1
    ax,bx = get_min_max(ax,bx)
    if x<=ax:
        amount0 = get_amount0_by_l(ax,bx,l)
    if ax<x<=bx:
        amount0 = get_amount0_by_l(x,bx,l)
        amount1 = get_amount1_by_l(ax,x,l)
    if x>bx:
        amount1 = get_amount1_by_l(ax,bx,l)
    return amount0/Decimal(str(decimal0)),amount1/Decimal(str(decimal1))

def get_av_args(bt,lt,amount0,amount1,tick=None,decimal0=1e18,decimal1=1e6):
    t_l = tick-bt
    t_u = tick+bt
    ax = Decimal(get_sqrtPriceX96_by_tick(t_l))
    bx = Decimal(get_sqrtPriceX96_by_tick(t_u))
    x = Decimal(get_sqrtPriceX96_by_tick(tick))
    amount0 = Decimal(str(amount0))
    amount1 = Decimal(str(amount1))
    amount0_wei = amount0*Decimal(str(decimal0))
    amount1_wei = amount1*Decimal(str(decimal1))
    price = get_price_by_tick(tick)
    price0 = get_price_by_tick(t_l)
    price1 = get_price_by_tick(t_u)
    l = get_l_by_amount01(x,ax,bx,amount0_wei,amount1_wei)
    amount0_use,amount1_use = get_amount01_by_l(x,ax,bx,l)
    res_dict = {'base_amount0':amount0_use,'base_amount1':amount1_use,
            'base_price_l':price0,'base_price_u':price1}    
    amount0_left = amount0-amount0_use
    amount1_left = amount1-amount1_use
    if amount0_left*Decimal(str(price))>amount1_left:
        res_dict.update({'limit_amount0':amount0_left,'limit_amount1':0,
            'limit_price_l':get_price_by_tick(tick),'limit_price_u':get_price_by_tick(tick+lt)})
    else:
        res_dict.update({'limit_amount0':0,'limit_amount1':amount1_left,
            'limit_price_l':get_price_by_tick(tick-lt),'limit_price_u':get_price_by_tick(tick)})
    return res_dict