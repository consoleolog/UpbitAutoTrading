import hashlib
import json
import os
import pprint
from urllib.parse import urlencode

import jwt
import uuid
import time
import requests
from dotenv import load_dotenv

from logger import Logger
from provider import Provider

load_dotenv()

accessKey = os.environ["BITHUMB_OPEN_API_ACCESS_KEY"]
secretKey = os.environ["BITHUMB_OPEN_API_SECRET_KEY"]
apiUrl = 'https://api.bithumb.com'


class BithumbProvider(Provider):
    def __init__(self):
        self.logger = Logger.get_logger(__class__.__name__)

    def _print_result(self, result):
        self.logger.debug("============")
        self.logger.debug("\n"+pprint.pformat(result))
        self.logger.debug("=============")

    def get_currencies(self):
        payload = {
            'access_key': accessKey,
            'nonce': str(uuid.uuid4()),
            'timestamp': round(time.time()*1000),
        }
        jwt_token = jwt.encode(payload, secretKey)
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {'Authorization': authorization_token}

        try:
            response = requests.get(apiUrl + '/v1/accounts', headers=headers)
            result = response.json()
            self._print_result(result)
            return result
        except Exception as err:
            self.logger.error(err)

    def get_price(self, interval, params):
        url = f"https://api.bithumb.com/v1/candles/{interval}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        self._print_result(result)
        return result

    def get_candles(self, interval: str, ticker: str, count: int) -> list[dict]:
        params = {
            'market': ticker,
            'count': count,
        }
        headers = {"accept": "application/json"}
        response = requests.get(apiUrl + '/v1/candles', headers=headers, params=params)
        result = response.json()
        self._print_result(result)
        return result

    def create_order(self, param):

        query = urlencode(param).encode()
        m = hashlib.sha512()
        m.update(query)
        query_hash = m.hexdigest()
        payload = {
            'access_token': accessKey,
            'nonce': str(uuid.uuid4()),
            'timestamp': round(time.time() * 1000),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = jwt.encode(payload, secretKey)
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {
            'Authorization': authorization_token,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(apiUrl + '/orders', headers=headers, data=json.dumps(param))
            result =  response.json()
            self._print_result(result)
            return result
        except Exception as err:
            self.logger.error(err)

    def deposit_krw(self, amount):
        requestBody = dict(
            amount=amount,
            two_factor_type='kakao'
        )
        query = urlencode(requestBody).encode()
        h = hashlib.sha512()
        h.update(query)
        query_hash = h.hexdigest()
        payload = {
            'access_token': accessKey,
            'nonce': str(uuid.uuid4()),
            'timestamp': round(time.time() * 1000),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = jwt.encode(payload, secretKey)
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {
            'Authorization': authorization_token,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(apiUrl + '/v1/deposits/krw', data=json.dumps(requestBody), headers=headers)
            result = response.json()
            self._print_result(result)
            return result
        except Exception as err:
            self.logger.error(err)

    def withdrawal_krw(self, amount):
        requestBody = dict(
            amount=amount,
            two_factor_type='kakao'
        )

        query = urlencode(requestBody).encode()
        h = hashlib.sha512()
        h.update(query)
        query_hash = h.hexdigest()
        payload = {
            'access_token': accessKey,
            'nonce': str(uuid.uuid4()),
            'timestamp': round(time.time() * 1000),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = jwt.encode(payload, secretKey)
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {
            'Authorization': authorization_token,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(apiUrl + '/v1/withdraws/krw', data=json.dumps(requestBody), headers=headers)
            result = response.json()
            self._print_result(result)
            return result
        except Exception as err:
            self.logger.error(err)


bithumb_provider = BithumbProvider()

bithumb_provider.get_price("minutes/3", {
            'market': "KRW-BTC",
            'count': 200
})