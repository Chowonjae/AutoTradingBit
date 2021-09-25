import time
import datetime
import pyupbit as pu
from strategy import strategy as st
from strategy import StateMarket as state
from trade import Trading as trading
from api import API_KEY as key
from bot import slackBot as bot

upbit = key.api_key()
coin_list = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-ADA", "KRW-SNT", "KRW-ZIL", "KRW-LTC", "KRW-EOS"]
target_price = {}
target_price_12 = {}
target_price_15 = {}
target_price_18 = {}
current_price = {}
isBull = {}


def get_target_price(ticker):
    df = pu.get_ohlcv(ticker, interval="day", count=2)
    print(df)
    target = df.iloc[1]['open'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * 0.5
    return target


def get_target_price_9(ticker):
    df = pu.get_daily_ohlcv_from_base(ticker, base=9)
    print(df)
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


for ticker in coin_list:
    target_price[ticker] = get_target_price(ticker)
    target_price_12[ticker] = get_target_price_9(ticker)
    # target_price_15[ticker] = get_target_price_15(ticker)
    # target_price_18[ticker] = get_target_price_18(ticker)
    time.sleep(1)

print(target_price)
print(target_price_12)
# print(target_price_15)
# print(target_price_18)