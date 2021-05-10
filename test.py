import time
import datetime
import pyupbit as pu
from strategy import strategy as st
from strategy import StateMarket as state
from trade import Trading as trading
from api import API_KEY as key
from bot import slackBot as bot

upbit = key.api_key()
coin_list = ["KRW-TRX"]
target_price = {}
current_price = {}
isBull = {}

# for coin in coin_list:vi


# def order_history1(coin):
#     return True
#
# print(order_history1("KRW-BTC"))

# print(upbit.get_balances())

# now = datetime.datetime.now()
# open_time = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(0.375)
# print(open_time - datetime.timedelta(minutes=2))