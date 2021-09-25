# -*- encoding: utf-8 -*-

import pyupbit as pu


# 변동성 돌파 전략 목표가 갱신
def get_target_price(ticker):
    df = pu.get_ohlcv(ticker, interval="day", count=2)
    target = df.iloc[1]['open'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * 0.5
    return target


def get_target_price_12(ticker):
    df = pu.get_daily_ohlcv_from_base(ticker, base=12)
    target = df.iloc[-1]['open'] + (df.iloc[-2]['high'] - df.iloc[-2]['low']) * 0.5
    return target


def get_target_price_15(ticker):
    df = pu.get_daily_ohlcv_from_base(ticker, base=15)
    target = df.iloc[-1]['open'] + (df.iloc[-2]['high'] - df.iloc[-2]['low']) * 0.5
    return target


def get_target_price_18(ticker):
    df = pu.get_daily_ohlcv_from_base(ticker, base=18)
    target = df.iloc[-1]['open'] + (df.iloc[-2]['high'] - df.iloc[-2]['low']) * 0.5
    return target
