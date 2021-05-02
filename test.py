import time
import datetime
import pyupbit as pu
from strategy import strategy as st
from strategy import StateMarket as state
from trade import Trading as trading
from api import API_KEY as key
from bot import slackBot as bot

upbit = key.api_key()
coin_list = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-ADA", "KRW-LTC", "KRW-xEM", "KRW-ZIL", "KRW-SC"]
target_price = {}
current_price = {}
isBull = {}

# for coin in coin_list:
#     target_price[coin] = st.get_target_price(coin)
# while True:
#     for coin in coin_list:
#         current_price[coin] = pu.get_current_price(coin)  # 현재가
#         isBull[coin] = state.StateMarket(coin)
#         if current_price[coin] > target_price[coin] and isBull[coin]:  # 현재가가 목표가이상으로 가면 매수 상승장
#             if False:
#                 print(coin)
#             else:
#                 print("a")


# def order_history1(coin):
#     return True
#
# print(order_history1("KRW-BTC"))

# print(upbit.get_balances())

# now = datetime.datetime.now()
# open_time = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(0.375)
# print(open_time - datetime.timedelta(minutes=2))