# -*- encoding: utf-8 -*-

import API_KEY as key
import pyupbit as pu
import bot.slackBot as bot

upbit = key.api_key()

# 매수
def buy_crypto_currency(ticker):
    orderbook = pu.get_orderbook(ticker)
    sell_price = orderbook[0]['orderbook_units'][0]['bid_price']
    a = (unit / sell_price) - 0.00000001
    volume = '%.8f' % a
    upbit.buy_limit_order(ticker, sell_price, volume)

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
            bought_crypto_cancel(orderId)   # 미체결 주문 취소
            print("주문 ", state_wait[i]['market'], "이 ", state_wait[i]['volume'], "개 취소 되었습니다.")

# stop-loss
def stop_loss(coin):
    state_done = upbit.get_order(coin, state="done")
    current_price = pu.get_current_price(coin)
    if len(state_done) > 0:
        for i in range(len(state_done)):
            if state_done[i]['ord_type'] in "limit":
                current_price < state_done[i]['price'] * 0.1

                return True