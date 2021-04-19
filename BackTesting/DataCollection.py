# 변동성 돌파전략 백테스팅
import pyupbit as pu

# 비트코인
df = pu.get_ohlcv("KRW-BTC")
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)
df.to_excel("btc.xlsx")

# 리플
df = pu.get_ohlcv("KRW-XRP")
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)
df.to_excel("xrp.xlsx")
