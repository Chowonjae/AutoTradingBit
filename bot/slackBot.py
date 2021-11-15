# -*- encoding: utf-8 -*-

import requests
from datetime import datetime
from api import API_KEY as key

upbit = key.api_key()

def post_message(text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+'aa'},
        data={"channel": '#bit', "text": text}
    )

def slack_message(title, message):
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + str(title) + str(message)
    post_message(strbuf)

def buy_bot(information):
    message = information['market'][4:8] + "을 " + information['price'] + "가격으로" + information['volume'] + "개 매수했습니다."
    slack_message("구매", message)

def sell_bot(coin):
    slack_message('매도 완료', coin)

def cancel_bot(coin):
    slack_message(coin, '현재가가 매수가를 넘어 매수 주문을 취소합니다.')

def stop_loss_bot(coin):
    slack_message(coin, '10% 이상 손실로 스탑로스 실행')

def error_bot(e):
    slack_message('exception ERROR', e)

def start_bot(message):
    post_message(message)

def exit_bot(message):
    post_message(message)
