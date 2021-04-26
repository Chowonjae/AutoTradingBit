# -*- encoding: utf-8 -*-

import pyupbit as pu


# 변동성 돌파 전략 목표가 갱신
def get_target_price(ticker):
    df = pu.get_ohlcv(ticker)
    yesterday = df.iloc[-2]
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target
