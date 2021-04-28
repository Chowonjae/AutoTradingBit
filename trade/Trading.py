# -*- encoding: utf-8 -*-

from api import API_KEY as key
from bot import slackBot as bot
import datetime
import pyupbit as pu

upbit = key.api_key()
now = str(datetime.datetime.now())
new_now = now[0:10]

# 매수
def buy_crypto_currency(ticker, unit):
    orderbook = pu.get_orderbook(ticker)
    sell_price = orderbook[0]['orderbook_units'][0]['bid_price']
    a = (unit / sell_price) - 0.00000001
    volume = '%.8f' % a
    buy = upbit.buy_limit_order(ticker, sell_price, volume)
    # print('매수 ', ticker)
    return buy


# 매도
def sell_crypto_currency(ticker):
    coin = upbit.get_balance(ticker)
    orderbook = pu.get_orderbook(ticker)
    buy_price = orderbook[0]['orderbook_units'][0]['ask_price']
    upbit.sell_limit_order(ticker, buy_price, coin)


# 취소
def bought_crypto_cancel(uuid):
    upbit.cancel_order(uuid)


# 미체결 주문
def order_state(coin):
    state_wait = upbit.get_order(coin)  # 미체결

    if len(state_wait) > 0:
        for i in range(len(state_wait)):
            orderId = state_wait[i]['uuid']
            bought_crypto_cancel(orderId)  # 미체결 주문 취소
            bot.cancel_bot(coin)

# 주문 이력 비교
def order_history1(coin):
    if len(upbit.get_order(coin, state='done')) > 0:
        state_done = upbit.get_order(coin, state='done')
        for i in range(1):
            order_date = state_done[i]['created_at'][0:10]
        if order_date == new_now:
            return True  # 거래한 내역이 있다
def order_history2(coin):
    if len(upbit.get_order(coin)) > 0:
        his_coin = upbit.get_order(coin)[0]['market']
        if his_coin == coin:
            return True

# stop-loss
# def stop_loss(coin):
#     state_done = upbit.get_order(coin, state="done")
#     current_price = pu.get_current_price(coin)
#     if len(state_done) > 0:
#         for i in range(len(state_done)):
#             if state_done[i]['ord_type'] in "limit":
#                 current_price < float(state_done[i]['price'] * 0.1)
#                 return True
