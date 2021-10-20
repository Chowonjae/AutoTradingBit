# Cryptocurrency Trading
> Table of Contents
1. About main.py  
 * Strategy  
 * 손실률을 최소화 하는 방법
 * How it works
2. About Slack Bot  
 * In main.py
 * Commander Bot
4. About Working environment

> 1. About main.py 
 * Strategy
 -레리 윌리엄스의 변동성 돌파 전략을 사용 (전일의 변동폭을 사용하여 오늘의 거래신호를 계산함)  
 -전날, 당일의 거래 데이터를 가져와 (전날 고점 - 전날 저점) * k(노이즈 비율)와 당일 시가에 더한 값을 거래 신호로 받아서 거래를 한다.
  ```
  def get_target_price(ticker):
    df = pu.get_ohlcv(ticker, interval="day", count=2)
    k = k_range(ticker)
    target = df.iloc[1]['open'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target
  ```
  -이동평균선을 이용한 상승장 파악  
  -5일 평균선이 현재가 보다 눂으며 상승장이라 판단하여 변동성 돌파 전략을 사용하여 거래 반대면 거래 정지
  ```
  def StateMarket(ticker):
    ct5 = pu.get_ohlcv(ticker, interval="day", count=5)
    ma5 = ct5['close'].rolling(5).mean().iloc[-1]

    price = pu.get_current_price(ticker)
    time.sleep(0.1)

    if price > ma5:
        return True
    else:
        return False
 ```
 * 손실률을 최소화 하는 방법  
  -시드의 20%씩 분산하여 투자  
  -수익이 난 금액은 시드에 포함하지 않는다.  
  ```
  holding_cash = 0,000,000
  buy_percent = 0.2
  buy_amount = holding_cash * buy_percent
  
  trading.buy_crypto_currency(coin, buy_amount)
  ```
  -노이즈 값을 고정 값으로 두는 것이 아닌 20일 노이즈 비율의 평균을 노이즈 값으로 쓰면서 좀 더 시장의 변화에 대응할 수 있도록 한다.  
  -식 : noise = 1 - abs(open - end) / (high - low)
  ```
  def k_range(ticker):
    df = pu.get_ohlcv(ticker, interval="day", count=21)
    noise_total = 0
    for i in range(len(df)-1):
        noise_total += 1 - abs(df.iloc[i]['open'] - df.iloc[i]['close']) / (df.iloc[i]['high'] - df.iloc[i]['low'])
    noise = noise_total / 20
    return truncate(noise, 2)
  ```
* How it works  
  -main.py에 각각의 모듈들을 import 하고 모든 동작은 main.py에서 시작 되게 했다.
```
  import time
  import datetime
  import pyupbit as pu
  from strategy import strategy as st
  from strategy import StateMarket as state
  from trade import Trading as trading
  from api import API_KEY as key
  from bot import slackBot as bot
```
> 2. About Slack Bot  
 * In main.py
  -거래를 하면서 
