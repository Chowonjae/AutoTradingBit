# -*- encoding: utf-8 -*-

import pyupbit as pu

def api_key():
    with open("../upbit.txt") as f:
        lines = f.readlines()
        access = lines[0].strip()
        secret = lines[1].strip()
        upbit = pu.Upbit(access, secret)

        return upbit


# with open("upbit.txt") as f:
#     lines = f.readlines()
#     access = lines[0].strip()
#     print(access)
#     secret = lines[1].strip()
#     print(secret)
#     upbit = pu.Upbit(access, secret)