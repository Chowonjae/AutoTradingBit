# -*- encoding: utf-8 -*-

# 이동평균선으로 현재의 장 흐름세를 파악 (상승장, 하락장)
import time

import pyupbit as pu


def StateMarket(ticker):
    ct5 = pu.get_ohlcv(ticker, interval="day", count=5)
    ct20 = pu.get_ohlcv(ticker, interval="day", count=20)
    ma5 = ct5['close'].rolling(5).mean().iloc[-1]
    ma20 = ct20['close'].rolling(20).mean().iloc[-1]

    price = pu.get_current_price(ticker)
    time.sleep(0.1)

    if price > ma5:
        return True
    else:
        return False

# coin_list = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-ADA", "KRW-LTC", "KRW-XEM", "KRW-ZIL", "KRW-SC"]
#
# for i in coin_list:
#     print(i, StateMarket(i))