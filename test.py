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

# while True:
#     for coin in coin_list:
#         target_price[coin] = st.get_target_price(coin)
#     message = str(target_price)
#     print("거래 시작 목표가 : ", message)
#
#     for coin in coin_list:
#         current_price[coin] = pu.get_current_price(coin)
#         isBull[coin] = state.StateMarket(coin)
#     print("현재가 : ", current_price)
#     print(isBull["KRW-BTC"])
#
#     time.sleep(1)
# now = datetime.datetime.now()
# print(upbit.get_order("KRW-BTC", state='done')[0]['created_at'])

