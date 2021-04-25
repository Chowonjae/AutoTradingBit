# -*- encoding: utf-8 -*-

import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = 'rqunJ24JBI6zllhMVbmN5MfxxIYFqmuoUPs5LxkW'
secret_key = 'SkyNQLhqE9kT7Iec4Qe0n7sVM1Epo2QryBzN0lex'
server_url = 'https://api.upbit.com'

def buy_order(ticker, price, volume):
    query = {
        'market' : ticker,
        'side' : 'bid',
        'volume' : volume,
        'price' : price,
        'ord_type' : 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key' : access_key,
        'nonce' : str(uuid.uuid4()),
        'query_hash' : query_hash,
        'query_hash_alg' : 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)