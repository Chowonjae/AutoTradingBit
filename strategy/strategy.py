# -*- encoding: utf-8 -*-

import time
import pyupbit as pu
import bot.slackBot as bot

# 잔고조회
def balance_now():
    for bal in upbit.get_balances():
        bal = bal['currency']
        if (bal == "KRW"):
            balance = upbit.get_balance(bal)
            print(bal, " : ", balance)
            time.sleep(0.1)
        else:
            for ticker in pu.get_tickers("KRW-" + bal):
                balance = upbit.get_balance(ticker)
                print(ticker, " : ", balance)
                time.sleep(0.1)

# 현재가 조회
# while True:
#     price = pu.get_current_price("KRW-BTC")
#     print(price)
#     bot.post_message(price)
#     time.sleep(0.2)

# 변동성 돌파 전략 목표가 갱신
def get_target_price(ticker):
    df = pu.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target