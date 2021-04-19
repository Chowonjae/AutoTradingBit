import API_KEY as key
import pyupbit as pu

upbit = key.api_key()

# 매수
def buy_crypto_currency(ticker):
    krw = upbit.get_balance("KRW")
    orderbook = pu.get_orderbook(ticker)
    sell_price = orderbook[0]['orderbook_units'][0]['bid_price']
    unit = krw / float(sell_price)
    upbit.buy_limit_order(ticker, sell_price, unit)
    # a = upbit.buy_limit_order(ticker, 5000, 20)
    # return a
# 매도
def sell_crypto_currency(ticker):
    coin = upbit.get_balance(ticker)
    orderbook = pu.get_orderbook(ticker)
    buy_price = orderbook[0]['orderbook_units'][0]['ask_price']
    upbit.sell_limit_order(ticker, buy_price, coin)