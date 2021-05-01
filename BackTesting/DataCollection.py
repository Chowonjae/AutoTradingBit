# -*- encoding: utf-8 -*-

# 변동성 돌파전략 백테스팅
import pyupbit as pu
import time
import pandas as pd
import pyupbit as pu
import numpy as np
import matplotlib.pyplot as plt

# 비트코인
date = None
dfs = []
# 1000일간 데이터 수집
for i in range(5):
    df = pu.get_ohlcv("KRW-BTC", to=date)
    dfs.append(df)

    date = df.index[0]
    time.sleep(0.1)

df = pd.concat(dfs).sort_index()

df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)
df.to_excel("btc.xlsx")

# 리플
df = pu.get_ohlcv("KRW-XRP")
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)
df.to_excel("xrp.xlsx")
