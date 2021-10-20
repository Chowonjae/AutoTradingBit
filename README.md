# Cryptocurrency Trading
> Table of Contents
1. About main.py  
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
 * How it works
2. About Slack Bot  
> 가나다
* 리스트1
* 리스트2
1. 순서
2. 순서  
*가나다*
**가나다**
