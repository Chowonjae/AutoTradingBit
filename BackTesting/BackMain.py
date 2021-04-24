# -*- encoding: utf-8 -*-

import time
import pandas as pd
import pyupbit as pu
import numpy as np
import matplotlib.pyplot as plt

def get_ror(coin, k):
    date = None
    dfs = []
    # 1000일간 데이터 수집
    for i in range(5):
        df = pu.get_ohlcv(coin, to=date)
        dfs.append(df)

        date = df.index[0]
        time.sleep(0.1)

    df = pd.concat(dfs).sort_index()

    df['ma5'] = df['close'].rolling(5).mean().shift(1)
    df['bull'] = df['open'] > df['ma5']
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    df['current_price'] <= df['target'] + df['target'] * 0.
    krw = 1000000
    if df['high'] > df['target']:


    df['total'] = df['ror'].cumprod()

    df['hpr'] = df['ror'].cumprod()
    df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
    print("MDD: ", df['dd'].max())
    print("HPR: ", df['hpr'][-2])
    df.to_excel("larry_ma.xlsx")

    plt.plot(df['total'])
    plt.show()
    # df.to_excel("BackTesting.xlsx")

    ror = df['ror'].cumprod()[-2]
    return ror

# 상승장일 경우 0.7 아닐경우 0.5

print(get_ror("KRW-BTC", 0.5))
# for k in np.arange(0.1, 1.0, 0.1):
#     ror = get_ror(k)
#     print("%.1f %f" % (k, ror))

# def get_ror(k):
#     date = None
#     dfs = []
#     # 1000일간 데이터 수집
#     for i in range(5):
#         df = pu.get_ohlcv("KRW-BTC", to=date)
#         dfs.append(df)
#
#         date = df.index[0]
#         time.sleep(0.1)
#
#     df = pd.concat(dfs).sort_index()
#
#     df['ma5'] = df['close'].rolling(5).mean().shift(1)
#     df['range'] = (df['high'] - df['low']) * k
#     df['target'] = df['open'] + df['range'].shift(1)
#     df['bull'] = df['open'] > df['ma5']
#
#     fee = 0.0012
#     df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1) # 매수하면 나오는 수익률
#
#     df['total'] = df['ror'].cumprod()
#
#     df['hpr'] = df['ror'].cumprod()
#     df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
#     print("MDD: ", df['dd'].max())
#     print("HPR: ", df['hpr'][-2])
#     df.to_excel("larry_ma.xlsx")
#
#     plt.plot(df['total'])
#     plt.show()
#     # df.to_excel("BackTesting.xlsx")
#
#     ror = df['ror'].cumprod()[-2]
#     return ror