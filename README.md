# Cryptocurrency Trading
> Table of Contents
1. About main.py  
 * Strategy  
 * 손실률을 최소화 하는 방법
 * How it works
2. About Slack Bot  
 * In main.py
 * Commander Bot
3. About Working environment
 * AWS
 * Docker

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
  -거래를 하면서 발생하는 모든 Log들을 Slack API를 사용하여 Slack으로 받아 볼 수 있도록 했다.  
  -slackBot.py  
 * Commander Bot  
  -slackToUser.py에서 Flask를 사용하여 챗봇(Rest API POST, GET를 사용하여) 형태로 사용자가 Slack에서 값들을 입력(POST)하면 find_info.py에서 해당 값을 찾아서 반환하도록 했다.  
  
-구현부
```
@app.route("/slack", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200,
                             {"content_type": "application/json"})
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        event_command = slack_event["event"]["text"]
        command = command_list(event_command)
        return event_handler(event_type, slack_event, command)
    return make_response("슬랙 요청에 이벤트가 없습니다.", 404,
                         {"X-Slack_No_Retry": 1})
```
  -거래중인 화폐 보기  
```
def get_balances():
    text = ''
    data = upbit.get_balances()
    for i in data:
        text += i['currency'] + ' : ' + str(format(float(i['balance']), ',')) + '\n'
    return text
```
  -손익 확인하기 (%)  
```
def profit_and_loss():
    text = ''
    current_price = {}
    data = upbit.get_balances()
    for i in data:
        if i['currency'] == 'KRW':
            pass
        else:
            current_price[i['currency']] = round(
                ((pu.get_current_price() - float(i['avg_buy_price'])) / float(i['avg_buy_price'])) * 100, 2)
    for i in current_price:
        text += i + ' : ' + str(current_price[i]) + ' %' + '\n'
    return text
```
*** 
                                               우분투 조작
***
  -프로그램 작동 여부  
```
def state():
    pids = str(sp.check_output("ps -ef | grep main.py | awk '{print $2}'", shell=True))
    pid = pids.replace('b', '').replace("'", "").split('\\n')[0]
    if pid == 0 or pid is None:
        return '실행중이 아닙니다.'
    else:
        return '실행중 입니다.'
```
  -도커에 들어가서 따로 실행하지 않고 Slack으로 동작 정지를 할 수 있게 만들었다.  
  -프로그램 시작  
```
def start():
    os.chdir(path_ubuntu)
    os.system('nohup python3 main.py 1>output.log 2>error.log &')
    return 'main.py를 실행'
```
  -프로그램 정지  
```
def stop():
    pids = str(sp.check_output("ps -ef | grep main.py | awk '{print $2}'", shell=True))
    pid = pids.replace('b', '').replace("'", "").split('\\n')[0]
    os.system('kill -9 ' + pid)
    return pid + ' 정지 완료'
```
> 3. About Working environment
  * AWS  
   -AWS EC2 Ubuntu 20.04 환경에서 nohup으로 백그라운드에서 실행 시켰다.  
  * Docker  
   -Docker Ubuntu 20.04 환경으로 이식 완료  
   -main.py를 nohup으로 백그라운드 실행 후 별도로 slackToUser.py를 실행시켜 API로 명령어를 주고 받음
   -터널링을 통하여 통신
