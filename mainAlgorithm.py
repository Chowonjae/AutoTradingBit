# -*- encoding: utf-8 -*-

import datetime
import pyupbit as pu
from strategy import strategy as st
from strategy import StateMarket as state
from trade import Trading as trading
from api import API_KEY as key
from bot import slackBot as bot
from database import database_hendler as dh


def refresh_time():
    return datetime.datetime.now()


def open_time():
    currentTime = refresh_time()
    return datetime.datetime(currentTime.year, currentTime.month, currentTime.day) + datetime.timedelta(0.375)


class mainTrading:
    def __init__(self):
        self.upbit = key.api_key()
        # self.db = dh.MariaDBHandler()
        self.coin_list = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-ADA", "KRW-LTC"]
        self.bought_list = []
        self.target_buy_count = 5  # 주문예정 암호화폐 개수
        self.buy_percent = 0.2  # 화폐별 구매 비율
        self.holding_cash = 200000  # 보유한 현금
        self.bring_balances = self.upbit.get_balances()  # 보유한 암호화폐 조회
        self.buy_amount = self.holding_cash * self.buy_percent  # 화폐당 주문 가능 금액
        self.target_price = {}
        self.current_price = {}
        self.isBull = {}
        self.k_range = {}
        self.purchase_history = {}
        for ticker in self.coin_list:
            if trading.order_history1(ticker) or trading.order_history2(ticker):
                self.purchase_history[ticker] = True
            else:
                self.purchase_history[ticker] = False

    def start_messages(self):
        holding_cash_message = '주문 가능 금액 ' + str(int(self.holding_cash)) + '원 \n'
        buy_percent_message = '암호화폐별 주문 비율 : ' + str(self.buy_percent) + '배 \n'
        buy_amount_message = '암호화폐별 주문 금액 : ' + str(int(self.buy_amount)) + '원 \n'
        start_time_message = '시작 시간 :: ' + str(datetime.datetime.now().strftime('%m/%d %H:%M:%S')) + '\n'
        start_message = '------------------------ \n' + \
                        holding_cash_message + \
                        buy_percent_message + \
                        buy_amount_message + \
                        start_time_message + \
                        '------------------------ \n'
        self.target_price_define()
        bot.start_bot(start_message)

    def target_price_define(self):
        message = ''
        for ticker in self.coin_list:
            self.target_price[ticker] = st.get_target_price(ticker)
            self.k_range[ticker] = st.k_range(ticker)
        for i in self.target_price:
            message += i + ' : ' + str(self.target_price[i]) + ' K : ' + str(self.k_range[i]) + '\n'
        bot.slack_message("거래 시작 목표가 \n", message)

    def buy(self):
        for ticker in self.coin_list:
            self.current_price[ticker] = pu.get_current_price(ticker)
            self.isBull[ticker] = state.StateMarket(ticker)
            if self.current_price[ticker] > self.target_price[ticker] and self.isBull[ticker]:
                if not self.purchase_history and self.upbit.get_balance('KRW') > 5000:
                    trading.buy_crypto_currency(ticker, self.buy_amount)
                    self.purchase_history[ticker] = True

    def sell(self):
        for ticker in self.coin_list:
            if self.upbit.get_balance(ticker):
                trading.sell_crypto_currency(ticker)
                self.purchase_history[ticker] = False
            if self.upbit.get_order(ticker):
                trading.order_state(ticker)
                self.purchase_history[ticker] = False

    def bid_get_order_main(self):
        data_list = []
        for ticker in self.coin_list:
            order = self.upbit.get_order(ticker, state="done")[0]
            now = refresh_time()
            data = {
                'order_time': now,
                'market': 'btc',
                'side': '매수',
                'price': '23000',
                'volume': '2',
                'fee': '18'
            }
            data_list.append(data)
            self.db.bid_side_insert(data)
            if order['side'] == 'bid':
                if order['created_at'][0:10] == str(refresh_time())[0:10]:
                    pass
                    # data = {'side': '매수',
                    #         'price': order['price'],
                    #         'market': order['market'],
                    #         'volume': order['volume'],
                    #         'fee': order['paid_fee'],
                    #         'order_time': order['created_at'][0:19]
                    #         }
        print(data_list)

    def ask_get_order_main(self):
        data_list = []
        for ticker in self.coin_list:
            order = self.upbit.get_order(ticker, state="done")[0]
            print(order)
            if order['side'] == 'ask':
                if order['created_at'][0:10] == str(refresh_time())[0:10]:
                    data = {'side': '매도',
                            'price': order['price'],
                            'market': order['market'],
                            'volume': order['volume'],
                            'fee': order['paid_fee'],
                            'order_time': order['created_at'][0:19]
                            }
                    # order_DB['ratio'] = round(((float(order['price']) * float(order['volume'])) - self.buy_amount) / self.buy_amount * 100, 2)
                    data_list.append(data)
        return data_list


if __name__ == '__main__':
    d = mainTrading()
    d.bid_get_order_main()
