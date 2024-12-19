import json
from typing import Optional

import websocket

from logger import Logger
import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote
import pprint

from dotenv import load_dotenv

from upbit_document import UpbitDocument

load_dotenv()

access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']


class UpbitProviderV2(UpbitDocument):
    def __init__(self):
        self.logger = Logger().get_logger(__class__.__name__)

    def _print_result(self, result):
        self.logger.debug("============")
        self.logger.debug("\n" + pprint.pformat(result))
        self.logger.debug("=============")

    def get_currencies(self) -> list[dict]:

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorization = 'Bearer {}'.format(jwt_token)
        headers = {
            'Authorization': authorization,
        }

        res = requests.get(server_url + '/v1/accounts', headers=headers)
        result = res.json()
        self._print_result(result)
        return result

    def get_currency(self, ticker) -> int:
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorization = 'Bearer {}'.format(jwt_token)
        headers = {'Authorization': authorization}
        res = requests.get(server_url + '/v1/accounts', headers=headers)
        balances = res.json()

        for b in balances:
            if b['currency'] == ticker:
                self._print_result(b['balance'])
                return int(b['balance'])
            else:
                return 0

    def get_second_candles(self, market: str, to: Optional[str], count: int):
        url = "https://api.upbit.com/v1/candles/seconds"
        params = {
            'market': market,
            'count': count
        }
        if to is not None:
            params['to'] = to
        headers = {"accept": "application/json"}
        try:
            response = requests.get(url, params=params, headers=headers)
            result = response.json()
            self._print_result(result)
            return result
        except Exception as err:
            self.logger.error(err)

    def get_minute_candles(self, market: str, to: Optional[str], count: int, unit: int):
        url = "https://api.upbit.com/v1/candles/minutes/{}".format(unit)
        params = {
            'market': market,
            'count': count,
        }
        if to is not None:
            params['to'] = to
        headers = {"accept": "application/json"}
        try:
            response = requests.get(url, params=params, headers=headers)
            result = response.json()
            self._print_result(result)
            return result
        except Exception as err:
            self.logger.error(err)

    def get_day_candles(self, market: str, to: Optional[str], count: int, converting_price_unit: Optional[str]):
        url = "https://api.upbit.com/v1/candles/days"
        params = {
            'market': market,
            'count': count
        }
        if to is not None:
            params['to'] = to
        if converting_price_unit is not None:
            params['converting_price_unit'] = converting_price_unit
        headers = {"accept": "application/json"}
        try:
            response = requests.get(url, params=params, headers=headers)
            result = response.json()
            self._print_result(result)
            return result
        except Exception as err:
            self.logger.error(err)

    def get_week_candles(self, market: str, to: Optional[str], count: int):
        url = "https://api.upbit.com/v1/candles/weeks"
        params = {
            'market': market,
            'count': count
        }
        if to is not None:
            params['to'] = to
        headers = {"accept": "application/json"}
        try:
            response = requests.get(url, params=params, headers=headers)
            result = response.json()
            self._print_result(result)
            return result
        except Exception as err:
            self.logger.error(err)

    def get_month_candles(self, market: str, to: Optional[str], count: int):
        url = "https://api.upbit.com/v1/candles/months"
        params = {
            'market': market,
            'count': count
        }
        if to is not None:
            params['to'] = to
        headers = {"accept": "application/json"}
        try:
            response = requests.get(url, params=params, headers=headers)
            result = response.json()
            self._print_result(result)
            return result
        except Exception as err:
            self.logger.error(err)

    def get_year_candles(self, market: str, to: Optional[str], count: int):

        url = "https://api.upbit.com/v1/candles/years"
        params = {
            'market': market,
            'count': count
        }
        if to is not None:
            params['to'] = to
        headers = {"accept": "application/json"}
        try:
            response = requests.get(url, params=params, headers=headers)
            result = response.json()
            self._print_result(result)
            return result
        except Exception as err:
            self.logger.error(err)

    def deposit_krw(self, amount):
        params = {
            'amount': amount,
            'two_factor_type': 'kakao',
        }
        query_string = unquote(urlencode(params, doseq=True)).encode('utf-8')
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }
        jwt_token = jwt.encode(payload, secret_key)
        authorization = 'Bearer {}'.format(jwt_token)
        headers = {'Authorization': authorization}
        res = requests.post(server_url + '/v1/deposits/krw', json=params, headers=headers)
        result = res.json()
        self._print_result(result)
        return result

    def withdrawal_krw(self, amount):
        params = {
            'amount': amount,
            'two_factor_type': 'kakao',
        }

        query_string = unquote(urlencode(params, doseq=True)).encode('utf-8')
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorization = 'Bearer {}'.format(jwt_token)
        headers = {'Authorization': authorization}

        res = requests.post(server_url + '/v1/withdraws/krw', json=params, headers=headers)
        result = res.json()
        self._print_result(result)
        return result

    def create_order_v2(
            self,
            market: str,
            side: str,
            volume: Optional[float],
            price: Optional[float],
            ord_type: str,
            identifier: Optional[str],
            time_in_force: Optional[str],
    ):
        params = {
            "market": market,
            "side": side,
            "ord_type": ord_type,
        }

        if side == "bid":
            params["price"] = price
        elif side == "ask":
            params["volume"] = volume
        if ord_type == "limit" or ord_type == "best":
            params["time_in_force"] = time_in_force
        if identifier is not None:
            params["identifier"] = identifier

        query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorization = 'Bearer {}'.format(jwt_token)
        headers = {
            'Authorization': authorization,
        }

        try:
            res = requests.post(server_url + '/v1/orders', json=params, headers=headers)
            result = res.json()
            self._print_result(result)
            return result
        except Exception as err:
            self.logger.error(err)

    def create_socket(self, url):
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4())
        }
        jwt_token = jwt.encode(payload, secret_key)
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {'Authorization': authorization_token}
        ws_app = websocket.WebSocketApp(
            url=url,
            header=headers,
            on_message=self._on_message,
            on_open=self._on_connect,
            on_error=self._on_error,
            on_close=self._on_close
        )
        ws_app.run_forever()

    def _on_message(self, ws, message):
        data = message.decode("utf-8")
        self._print_result(json.loads(data))

    def _on_connect(self, ws):
        self.logger.info("========================")
        self.logger.info("WebSocket Connected!!")
        self.logger.info("========================")
        request_param = [
            {
                "ticket": str(uuid.uuid4())
            },
            {
                "type": "ticker",
                "codes": [
                    "KRW-BTC"
                ],
                "is_only_realtime": True
            },
            {
                "format": "SIMPLE"
            }
        ]
        ws.send(json.dumps(request_param))

    def _on_error(self, ws, error):
        self._print_result(error)

    def _on_close(self, ws, status_code, msg):
        self._print_result("status code : {}".format(status_code))
        self._print_result("msg : {}".format(msg))
