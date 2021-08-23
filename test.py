import time
import datetime
import pyupbit as pu
from strategy import strategy as st
from strategy import StateMarket as state
from trade import Trading as trading
from api import API_KEY as key
from bot import slackBot as bot

upbit = key.api_key()
coin_list = ["KRW-EOS"]
target_price = {}
current_price = {}
isBull = {}

# for coin in coin_list:vi


# def order_history1(coin):
#     return True
#
# print(order_history1("KRW-BTC"))

# print(upbit.get_balances())
# for i in range(len(upbit.get_balances())):
#     if upbit.get_balances()[i]['currency']==coin_list[0][4:]:
#         print(upbit.get_balances()[i]['currency'])
# print(coin_list[0][4:])

# now = datetime.datetime.now()
# open_time = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(0.375)
# print(open_time + datetime.timedelta(minutes=5, seconds=5))
# print(open_time - datetime.timedelta(seconds=11))
print(st.get_target_price("KRW-XRP"))