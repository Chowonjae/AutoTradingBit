# -*- encoding: utf-8 -*-

import time
import pyupbit as pu


# 변동성 돌파 전략 목표가 갱신
def get_target_price(ticker):
    df = pu.get_ohlcv(ticker, interval="day", count=2)
    k = k_range(ticker)
    target = df.iloc[1]['open'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target


# def get_target_price_12(ticker):
#     df = pu.get_daily_ohlcv_from_base(ticker, base=12)
#     target = df.iloc[-1]['open'] + (df.iloc[-2]['high'] - df.iloc[-2]['low']) * 0.5
#     return target
#
#
# def get_target_price_15(ticker):
#     df = pu.get_daily_ohlcv_from_base(ticker, base=15)
#     target = df.iloc[-1]['open'] + (df.iloc[-2]['high'] - df.iloc[-2]['low']) * 0.5
#     return target
#
#
# def get_target_price_18(ticker):
#     df = pu.get_daily_ohlcv_from_base(ticker, base=18)
#     target = df.iloc[-1]['open'] + (df.iloc[-2]['high'] - df.iloc[-2]['low']) * 0.5
#     return target


def k_range(ticker):
    # noise = 1 - abs(open - end) / (high - low)
    while True:
        df = pu.get_ohlcv(ticker, interval="day", count=21)
        time.sleep(0.1)
        if df is not None:
            break
    noise_total = 0
    for i in range(len(df)-1):
        noise_total += 1 - abs(df.iloc[i]['open'] - df.iloc[i]['close']) / (df.iloc[i]['high'] - df.iloc[i]['low'])
    noise = noise_total / 20
    return truncate(noise, 2)


def truncate(num, n):
    temp = str(num)
    for x in range(len(temp)):
        if temp[x] == '.':
            try:
                return float(temp[:x+n+1])
            except:
                return float(temp)
    return float(temp)


if __name__ == '__main__':
    coin_list = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-ADA", "KRW-LTC"]
    for i in coin_list:
        print(k_range(i))