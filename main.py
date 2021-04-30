# -*- encoding: utf-8 -*-

import time
import datetime
import pyupbit as pu
from strategy import strategy as st
from strategy import StateMarket as state
from trade import Trading as trading
from api import API_KEY as key
from bot import slackBot as bot

if __name__ == '__main__':
    try:
        upbit = key.api_key()
        coin_list = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-ADA", "KRW-LTC", "KRW-XEM", "KRW-ZIL", "KRW-SC"]
        bought_list = []
        target_buy_count = 8  # 주문예정 암호화폐 개수
        buy_percent = 0.125  # 화폐별 구매 비율
        holding_cash = upbit.get_balance("KRW")  # 보유한 현금
        bring_balances = upbit.get_balances()  # 보유한 암호화폐 조회
        buy_amount = holding_cash * buy_percent  # 화폐당 주문 가능 금액
        holding_cash_message = '주문 가능 금액 ' + str(int(holding_cash)) + '원 \n'
        buy_percent_message = '암호화폐별 주문 비율 : ' + str(buy_percent) + '배 \n'
        buy_amount_message = '암호화폐별 주문 금액 : ' + str(int(buy_amount)) + '원 \n'
        start_time_message = '시작 시간 :: ' + str(datetime.datetime.now().strftime('%m/%d %H:%M:%S')) + '\n'
        start_message = '------------------------ \n' + \
                        holding_cash_message + \
                        buy_percent_message + \
                        buy_amount_message + \
                        start_time_message + \
                        '------------------------ \n'
        bot.start_bot(start_message)
        # print(start_message)

        target_price = {}
        current_price = {}
        isBull = {}

        now = datetime.datetime.now()
        for coin in coin_list:
            target_price[coin] = st.get_target_price(coin)  # 거래 시작 목표가
        message = str(target_price)
        bot.slack_message("거래 시작 목표가", message)
        # print("거래 시작 목표가 ", message)

        while True:
            now = datetime.datetime.now()
            open_time = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(0.375)

            # 장 시작시간 이후 설정 값 초기화
            if open_time < now < open_time + datetime.timedelta(seconds=5):
                for coin in coin_list:
                    target_price[coin] = st.get_target_price(coin)  # 목표가 갱신
                holding_cash = upbit.get_balance("KRW")  # 보유한 현금
                bring_balances = upbit.get_balances()  # 보유한 암호화폐 조회
                buy_amount = holding_cash * buy_percent  # 화폐당 주문 가능 금액
                message = str(target_price) + '보유한 현금 = ' + str(int(holding_cash)) + '암호화폐별 주문 금액 = ' + str(
                    int(buy_amount))
                bot.slack_message("거래 시작 목표가 갱신", message)
            
            # 지정가 이후 매수
            for coin in coin_list:
                current_price[coin] = pu.get_current_price(coin)  # 현재가
                isBull[coin] = state.StateMarket(coin)
                if current_price[coin] > target_price[coin] and isBull[coin]:  # 현재가가 목표가이상으로 가면 매수 상승장
                    if trading.order_history1(coin):
                        pass
                    else:
                        trading.buy_crypto_currency(coin, buy_amount)
                        bot.buy_bot(coin)

                time.sleep(0.2)
            # 9시에 전량 매도
            if open_time - datetime.timedelta(seconds=11) < now < open_time - datetime.timedelta(seconds=1):
                for coin in coin_list:
                    if upbit.get_balance(coin):
                        trading.sell_crypto_currency(coin)
                        bot.sell_bot(coin)

            # 주문 취소
            # if open + datetime.timedelta(minutes=20) < now:  # 10분이 지난 후 미체결 주문 취소
            #     for coin in coin_list:
            #         trading.order_state(coin)

            # if trading.stop_loss(coin) is True:
            #     trading.sell_crypto_currency(coin)
            #     bot.stop_loss_bot(coin)
            #     time.sleep(1)
            print("~ing...")
            time.sleep(1)

    except Exception as e:
        bot.error_bot(e)
