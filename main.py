import time
import datetime
import pyupbit as pu
import strategy as st
import StateMarket as state
import Trading as trading
import API_KEY as key

upbit = key.api_key()

coin = "KRW-XRP"

isBull = state.StateMarket(coin)

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
open = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(0.375)
target_price = st.get_target_price(coin) # 거래 시작 목표가
print("거래 시작 목표가 : ", target_price)

while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.delta(seconds=10):
            target_price = st.get_target_price(coin)  # 목표가 갱신 (자정)
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            print("다음 자정은 : ", mid)
        current_price = pu.get_current_price(coin)  # 현재가
        if current_price > target_price and isBull:    # 현재가가 목표가이상으로 가면 매수
            krw = upbit.get_balance("KRW")
            if krw >= 5000:
                trading.buy_crypto_currency(coin)
                print("구매완료")
            else:
                print("최소 주문금액 미달 혹은 하락장. 으로 거래할 수 없습니다.")
        if open < now < open + datetime.timedelta(seconds=10):  # 장 시작(9시)에 전량 매도
            trading.sell_crypto_currency(coin)
            print("판매완료")

    except:
        print("에러 발생")

    time.sleep(1)