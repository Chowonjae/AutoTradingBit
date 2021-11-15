import sys
import os
import pyupbit as pu
import subprocess as sp
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api import API_KEY as key

upbit = key.api_key_slack()

path_ubuntu = '/Ubuntu/AutoTradingBit'
path_mac = '/Volumes/home/Drive/AutoTradingBit'


def get_balances():
    text = ''
    data = upbit.get_balances()
    for i in data:
        text += i['currency'] + ' : ' + str(format(float(i['balance']), ',')) + '\n'
    return text


def get_balance(ticker):
    text = upbit.get_balance(ticker)
    return text


def stop():
    pids = str(sp.check_output("ps -ef | grep main.py | awk '{print $2}'", shell=True))
    pid = pids.replace('b', '').replace("'", "").split('\\n')[0]
    os.system('kill -9 ' + pid)
    return pid + ' 정지 완료'


def start():
    os.chdir(path_ubuntu)
    os.system('nohup python3 main.py 1>output.log 2>error.log &')
    return 'main.py를 실행'


def command(text):
    return os.system(text)


def state():
    pids = str(sp.check_output("ps -ef | grep main.py | awk '{print $2}'", shell=True))
    pid = pids.replace('b', '').replace("'", "").split('\\n')[0]
    if pid == 0 or pid is None:
        return '실행중이 아닙니다.'
    else:
        return '실행중 입니다.'


def profit_and_loss():
    text = ''
    current_price = {}
    data = upbit.get_balances()
    print(data)
    for i in data:
        if i['currency'] == 'KRW':
            pass
        elif i['avg_buy_price'] == '0':
            pass
        else:
            ticker = 'KRW-' + i['currency']
            current_price[i['currency']] = round(
                ((pu.get_current_price(ticker) - float(i['avg_buy_price'])) / float(i['avg_buy_price'])) * 100, 2)
    for i in current_price:
        text += i + ' : ' + str(current_price[i]) + ' %' + '\n'
    text += 'Total' + ' : ' + str(round(sum(current_price.values()) / len(current_price), 2)) + ' %' + '\n'
    return text


if __name__ == '__main__':
    print(profit_and_loss())

    # ps -ef | grep main.py | awk '{print $2}'  PID 불러오기