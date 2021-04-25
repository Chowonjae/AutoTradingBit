# -*- encoding: utf-8 -*-

# 이동평균선으로 현재의 장 흐름세를 파악 (상승장, 하락장)
import pyupbit as pu

def StateMarket(ticker):
    ct = pu.get_ohlcv(ticker)
    close = ct['close']

    ma5 = close.rolling(5).mean()
    last_ma5 = ma5[-2]

    price = pu.get_current_price(ticker)

    if price > last_ma5:
        return True
    else:
        return False

# tickers = ['KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-ADA', 'KRW-ZIL']
# for ticker in tickers:
#     is_bull = StateMarket(ticker)
#     if is_bull:
#         print(ticker, "상승장")
#     else:
#         print(ticker, "하락장")

# def buy_currency(ticker):
#     krw = upbit.get_balance("KRW")
#     orderbook = pu.get_orderbook(coin)
#     sell_price = orderbook['orderbook_units'][0]['bid_price']
#     unit = krw / float(sell_price)
#     upbit.buy_limit_order(coin, sell_price, unit)