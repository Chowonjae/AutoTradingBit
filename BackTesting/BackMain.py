import time
import pandas as pd
import pyupbit as pu
import numpy as np

# def get_ror(k=0.5):
#     date = None
#     dfs = []
#
#     for i in range(5):
#         df = pu.get_ohlcv("KRW-BTC", to=date)
#         dfs.append(df)
#
#         date = df.index[0]
#         time.sleep(0.1)
#
#     df = pd.concat(dfs).sort_index()
#     print(len(df))
#     df['ma5'] = df['close'].rolling(5).mean().shift(1)
#     df['range'] = (df['high'] - df['low']) * k
#     df['target'] = df['open'] + df['range'].shift(1)
#     df['bull'] = df['open'] > df['ma5']
#
#     fee = 0.0012
#     df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1)
#
#     df['total'] = df['ror'].cumprod()[-2]
#
#     df['hpr'] = df['ror'].cumprod()
#     df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
#     print("MDD: ", df['dd'].max())
#     print("HPR: ", df['hpr'][-2])
#     # df.to_excel("larry_ma.xlsx")
#
#     # df.to_excel("BackTesting.xlsx")
#
#     ror = df['ror'].cumprod()[-2]
#     return ror
#
# for k in np.arange(0.1, 1.0, 0.1):
#     ror = get_ror(k)
#     print("%.1f %f" % (k, ror))

date = None
dfs = []

for i in range(5):
    df = pu.get_ohlcv("KRW-BTC", to=date)
    dfs.append(df)

    date = df.index[0]
    time.sleep(0.1)

df = pd.concat(dfs).sort_index()
print(len(df))
df['ma5'] = df['close'].rolling(5).mean().shift(1)
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)
df['bull'] = df['open'] > df['ma5']

fee = 0.0032
df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1)

df['total'] = df['ror'].cumprod()[-2]

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD: ", df['dd'].max())
print("HPR: ", df['hpr'][-2])
df.to_excel("larry_ma.xlsx")

# df.to_excel("BackTesting.xlsx")

ror = df['ror'].cumprod()[-2]
print(ror)