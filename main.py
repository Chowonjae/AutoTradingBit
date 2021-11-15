# -*- encoding: utf-8 -*-
import mainAlgorithm
import datetime
import time
from bot import slackBot as bot

if __name__ == '__main__':
    d = mainAlgorithm.mainTrading()
    currentTime = mainAlgorithm.refresh_time()
    open_time = mainAlgorithm.open_time()
    d.start_messages()
    while True:
        print(d.target_price)
        print(d.purchase_history)
        try:
            if open_time + datetime.timedelta(minutes=5) < currentTime < open_time + datetime.timedelta(minutes=5,
                                                                                                        seconds=2):
                d.start_messages()

            if open_time + datetime.timedelta(minutes=5,
                                              seconds=3) < currentTime or currentTime < open_time - datetime.timedelta(
                    seconds=11):
                d.buy()

            if open_time - datetime.timedelta(seconds=10) < currentTime < open_time - datetime.timedelta(seconds=1):
                d.sell()

            time.sleep(1)

        except Exception as e:
            bot.error_bot(e)
            bot.error_bot('에러로 인해 재실행 합니다.')
            time.sleep(1)