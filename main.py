# -*- encoding: utf-8 -*-

import os, sys, ctypes
import time, calendar
import datetime
import pyupbit as pu
import strategy as st
import StateMarket as state
import Trading as trading
import API_KEY as key
import bot.slackBot as bot


if __name__ == '__main__':
    # try:
        upbit = key.api_key()
        coin_list = ['KRW-ADA']
        bought_list = []
        target_buy_count = 2                    # 주문예정 암호화폐 개수
        buy_percent = 0.40                      # 화폐별 구매 비율
        holding_cash = upbit.get_balance("KRW") # 보유한 현금
        bring_balances = upbit.get_balances()   # 보유한 암호화폐 조회
        buy_amount = holding_cash * buy_percent # 화폐당 주문 가능 금액
        holding_cash_message = '주문 가능 금액 ' + str(holding_cash) + '\n'
        buy_percent_message = '암호화폐별 주문 비율 : ' + str(buy_percent) + '\n'
        buy_amount_message = '암호화폐별 주문 금액 : ' + str(buy_amount) + '\n'
        start_time_message = '시작 시간 :: ' + str(datetime.datetime.now().strftime('%m/%d %H:%M:%S')) + '\n'
        start_message = holding_cash_message + buy_percent_message + buy_amount_message + start_time_message
        bot.start_bot(start_message)
        soldout = False

        target_price = []
        current_price = []

        now = datetime.datetime.now()
        for coin in coin_list:
            target_price = st.get_target_price(coin)  # 거래 시작 목표가
            message = coin + ":" + str(target_price)
            bot.slack_message("거래 시작 목표가", message)

        while True:
            now = datetime.datetime.now()
            open = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(0.375)

            for coin in coin_list:
                if open < now < open + datetime.timedelta(seconds=10):
                    target_price = st.get_target_price(coin)  # 목표가 갱신
                current_price = pu.get_current_price(coin)  # 현재가

            for coin in coin_list:
                isBull = state.StateMarket(coin)
                if current_price > target_price and isBull:  # 현재가가 목표가이상으로 가면 매수
                    trading.buy_crypto_currency(coin, buy_amount)
                    # trading.buy_crypto_currency(coin)
                    if not upbit.get_order(coin):
                        bot.buy_bot(coin)

            # 주문 취소
            if open + datetime.timedelta(minutes=20) < now:  # 10분이 지난 후 미체결 주문 취소
                trading.order_state(coin)
                bot.cancel_bot(coin)
                time.sleep(1)

            if trading.stop_loss(coin) is True:
                trading.sell_crypto_currency(coin)
                bot.stop_loss_bot(coin)
                time.sleep(1)

            if open - datetime.timedelta(seconds=10) < now < open - datetime.timedelta(seconds=1):  # 9시에 전량 매도
                trading.sell_crypto_currency(coin)
                bot.sell_bot(coin)

            time.sleep(1)
    # except Exception as e:
    #     bot.error_bot(e)