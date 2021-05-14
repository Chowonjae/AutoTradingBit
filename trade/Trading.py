# -*- encoding: utf-8 -*-

from api import API_KEY as key
from bot import slackBot as bot
import datetime
import pyupbit as pu

upbit = key.api_key()


# 매수
def buy_crypto_currency(ticker, unit):
    orderbook = pu.get_orderbook(ticker)
    sell_price = orderbook[0]['orderbook_units'][0]['bid_price']
    a = (unit / sell_price) - 0.00000001
    volume = '%.8f' % a
    buy = upbit.buy_limit_order(ticker, sell_price, volume)
    bot.buy_bot(buy)


# 매도
def sell_crypto_currency(ticker):
    coin = upbit.get_balance(ticker)
    # orderbook = pu.get_orderbook(ticker)
    # buy_price = orderbook[0]['orderbook_units'][0]['ask_price']
    upbit.sell_market_order(ticker, coin)


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


# 주문 이력 비교 (거래 완료)
def order_history1(coin):
    coin_name = coin[4:]
    for i in range(len(upbit.get_balances())):
        if upbit.get_balances()[i]['currency'] == coin_name:
            return True

    # now = str(datetime.datetime.now())
    # new_now = now[0:10]
    # global order_date
    # if len(upbit.get_order(coin, state='done')) > 0:
    #     state_done = upbit.get_order(coin, state='done')
    #     if state_done[0]['side'] == 'bid':  # 매수
    #         order_date = state_done[0]['created_at'][0:10]
    #         if order_date == new_now:
    #             return True  # 거래한 내역이 있다
    #         else:
    #             pass
    #     elif state_done[0]['side'] == 'ask':  # 매도
    #         pass


# 주문 이력 비교 (미체결 주문)
def order_history2(coin):
    if len(upbit.get_order(coin)) > 0:
        his_coin = upbit.get_order(coin)[0]['market']
        if his_coin == coin:
            return True
        else:
            pass

# stop-loss
# def stop_loss(coin):
#     state_done = upbit.get_order(coin, state="done")
#     current_price = pu.get_current_price(coin)
#     if len(state_done) > 0:
#         for i in range(len(state_done)):
#             if state_done[i]['ord_type'] in "limit":
#                 current_price < float(state_done[i]['price'] * 0.1)
#                 return True

# print(order_history1("KRW-TRX"))
