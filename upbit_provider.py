import json
from typing import Optional, Union

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

from provider import Provider

load_dotenv()

access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

class UpbitProvider:
    def __init__(self):
        self.logger = Logger().get_logger(__class__.__name__)

    def _print_result(self, result):
        self.logger.debug("============")
        self.logger.debug("\n"+pprint.pformat(result))
        self.logger.debug("=============")

    def get_currencies(self)-> list[dict]:
        """
        전체 계좌 조회
        Returns:
            dict:
                - currency (str): 화폐를 의미하는 영문 대문자 코드

                - balance (int): 주문 가능 금액 / 수량

                - locked (float): 주문 중 묶여있는 금액 / 수량

                - avg_buy_price (float) : 매수 평균가

                - avg_buy_price_modified (bool): 매수 평균가 수정 여부

                - unit_currency (str): 평단가 기준 화폐
        """
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

    def get_currency(self, ticker)-> Union[str, int]:
        """
        Returns:
            dict:
                - currency (str): 화폐를 의미하는 영문 대문자 코드

                - balance (int): 주문 가능 금액 / 수량

                - locked (float): 주문 중 묶여있는 금액 / 수량

                - avg_buy_price (float) : 매수 평균가

                - avg_buy_price_modified (bool): 매수 평균가 수정 여부

                - unit_currency (str): 평단가 기준 화폐
        """
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorization = 'Bearer {}'.format(jwt_token)
        headers = { 'Authorization': authorization }
        res = requests.get(server_url + '/v1/accounts', headers=headers)
        balances = res.json()

        for b in balances:
            if b['currency'] == ticker:
                self._print_result(b['balance'])
                return str(b['balance'])
            else:
                return 0

    def get_order_chance(self, market: str):
        """
        주문 가능 정보
        Args:
            market: 마켓 ID
        Returns:
            dict:
                - bid_fee (NumberString): 매수 수수료 비율

                - ask_fee (NumberString): 매도 수수료 비율

                - market (Object): 마켓에 대한 정보

                - market.id (String): 마켓의 유일 키

                - market.name (String) : 마켓 이름

                - market.order_types  (Array[String]) 지원 주문 방식ㅅ

        """

    def get_second_candles(self, market: str, to: Optional[str], count: int):
        """
        Args:
            market : 마켓 코드 (ex. KRW-BTC)
            to : 마지막 캔들 시각 (exclusive). ISO8061 포맷 (yyyy-MM-dd'T'HH:mm:ss'Z' or yyyy-MM-dd HH:mm:ss). 기본적으로 UTC 기준 시간이며 2023-01-01T00:00:00+09:00 과 같이 KST 시간으로 요청 가능. 비워서 요청시 가장 최근 캔들
            count : 캔들 개수 (최대 200개 까지 요청 가능)
        Returns:
            dict:

                - market (str): 종목 코드

                - candle_date_time_utc (str): 캔들 기준 시각 (UTC 기준) 포맷 yyyy-MM-dd 'T' HH:mm:ss

                - candle_date_time_kst (str): 캔들 기준 시각 (KST 기준) 포맷 yyyy-MM-dd 'T' HH:mm:ss

                - opening_price (float): 시가

                - high_price (float): 고가

                - low_price (float): 저가

                - trade_price (float): 종가

                - timestamp (int): 마지막 틱이 저장된 시각

                - candle_acc_trade_price (float): 누적 거래 금액

                - candle_acc_trade_volume (float): 누적 거래량
        """
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
        """
        Args:
            market : 마켓 코드 (ex. KRW-BTC)
            to : 마지막 캔들 시각 (exclusive). ISO8061 포맷 (yyyy-MM-dd'T'HH:mm:ss'Z' or yyyy-MM-dd HH:mm:ss). 기본적으로 UTC 기준 시간이며 2023-01-01T00:00:00+09:00 과 같이 KST 시간으로 요청 가능. 비워서 요청시 가장 최근 캔들
            count : 캔들 개수 (최대 200개 까지 요청 가능)
            unit : 분 단위. 가능한 값 : 1, 3, 5, 15, 10, 30, 60, 240
        Returns:
            dict:

                - market (str): 종목 코드

                - candle_date_time_utc (str): 캔들 기준 시각 (UTC 기준) 포맷 yyyy-MM-dd 'T' HH:mm:ss

                - candle_date_time_kst (str): 캔들 기준 시각 (KST 기준) 포맷 yyyy-MM-dd 'T' HH:mm:ss

                - opening_price (float): 시가

                - high_price (float): 고가

                - low_price (float): 저가

                - trade_price (float): 종가

                - timestamp (int): 마지막 틱이 저장된 시각

                - candle_acc_trade_price (float): 누적 거래 금액

                - candle_acc_trade_volume (float): 누적 거래량
        """
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
        """
        Args:
            market : 마켓 코드 (ex. KRW-BTC)
            to : 마지막 캔들 시각 (exclusive). ISO8061 포맷 (yyyy-MM-dd'T'HH:mm:ss'Z' or yyyy-MM-dd HH:mm:ss). 기본적으로 UTC 기준 시간이며 2023-01-01T00:00:00+09:00 과 같이 KST 시간으로 요청 가능. 비워서 요청시 가장 최근 캔들
            count : 캔들 개수 (최대 200개 까지 요청 가능)
            converting_price_unit: 종가 환산 화폐 단위 (생략 가능, KRW로 명시할 시 원화 환산 가격을 반환.)
        Returns:
            dict:

                - market (str): 종목 코드

                - candle_date_time_utc (str): 캔들 기준 시각 (UTC 기준) 포맷 yyyy-MM-dd 'T' HH:mm:ss

                - candle_date_time_kst (str): 캔들 기준 시각 (KST 기준) 포맷 yyyy-MM-dd 'T' HH:mm:ss

                - opening_price (float): 시가

                - high_price (float): 고가

                - low_price (float): 저가

                - trade_price (float): 종가

                - timestamp (int): 마지막 틱이 저장된 시각

                - candle_acc_trade_price (float): 누적 거래 금액

                - candle_acc_trade_volume (float): 누적 거래량

        """
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

    def get_week_candles(self, market:str, to:Optional[str], count: int):
        """
        Args:
            market : 마켓 코드 (ex. KRW-BTC)
            to : 마지막 캔들 시각 (exclusive). ISO8061 포맷 (yyyy-MM-dd'T'HH:mm:ss'Z' or yyyy-MM-dd HH:mm:ss). 기본적으로 UTC 기준 시간이며 2023-01-01T00:00:00+09:00 과 같이 KST 시간으로 요청 가능. 비워서 요청시 가장 최근 캔들
            count : 캔들 개수 (최대 200개 까지 요청 가능)
        Returns:
            dict:

                - market (str): 종목 코드

                - candle_date_time_utc (str): 캔들 기준 시각 (UTC 기준) 포맷 yyyy-MM-dd 'T' HH:mm:ss

                - candle_date_time_kst (str): 캔들 기준 시각 (KST 기준) 포맷 yyyy-MM-dd 'T' HH:mm:ss

                - opening_price (float): 시가

                - high_price (float): 고가

                - low_price (float): 저가

                - trade_price (float): 종가

                - timestamp (int): 마지막 틱이 저장된 시각

                - candle_acc_trade_price (float): 누적 거래 금액

                - candle_acc_trade_volume (float): 누적 거래량
        """
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
        """
        Args:
            market : 마켓 코드 (ex. KRW-BTC)
            to : 마지막 캔들 시각 (exclusive). ISO8061 포맷 (yyyy-MM-dd'T'HH:mm:ss'Z' or yyyy-MM-dd HH:mm:ss). 기본적으로 UTC 기준 시간이며 2023-01-01T00:00:00+09:00 과 같이 KST 시간으로 요청 가능. 비워서 요청시 가장 최근 캔들
            count : 캔들 개수 (최대 200개 까지 요청 가능)
        Returns:
            dict:

                - market (str): 종목 코드

                - candle_date_time_utc (str): 캔들 기준 시각 (UTC 기준) 포맷 yyyy-MM-dd 'T' HH:mm:ss

                - candle_date_time_kst (str): 캔들 기준 시각 (KST 기준) 포맷 yyyy-MM-dd 'T' HH:mm:ss

                - opening_price (float): 시가

                - high_price (float): 고가

                - low_price (float): 저가

                - trade_price (float): 종가

                - timestamp (int): 마지막 틱이 저장된 시각

                - candle_acc_trade_price (float): 누적 거래 금액

                - candle_acc_trade_volume (float): 누적 거래량
        """
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
        """
        Args:
            market : 마켓 코드 (ex. KRW-BTC)
            to : 마지막 캔들 시각 (exclusive). ISO8061 포맷 (yyyy-MM-dd'T'HH:mm:ss'Z' or yyyy-MM-dd HH:mm:ss). 기본적으로 UTC 기준 시간이며 2023-01-01T00:00:00+09:00 과 같이 KST 시간으로 요청 가능. 비워서 요청시 가장 최근 캔들
            count : 캔들 개수 (최대 200개 까지 요청 가능)
        Returns:
            dict:

                - market (str): 종목 코드

                - candle_date_time_utc (str): 캔들 기준 시각 (UTC 기준) 포맷 yyyy-MM-dd 'T' HH:mm:ss

                - candle_date_time_kst (str): 캔들 기준 시각 (KST 기준) 포맷 yyyy-MM-dd 'T' HH:mm:ss

                - opening_price (float): 시가

                - high_price (float): 고가

                - low_price (float): 저가

                - trade_price (float): 종가

                - timestamp (int): 마지막 틱이 저장된 시각

                - candle_acc_trade_price (float): 누적 거래 금액

                - candle_acc_trade_volume (float): 누적 거래량
        """
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





    def create_order(self, params):
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
        headers = {'Authorization': authorization}

        res = requests.post(server_url + '/v1/orders', json=params, headers=headers)
        result = res.json()
        self._print_result(result)
        return result

    def get_candles(self, interval: str, ticker: str, count: int) -> list[dict]:
        params = {
            'market': ticker,
            'count': count
        }
        url = f"https://api.upbit.com/v1/candles/{interval}"
        headers = {"accept": "application/json"}
        response = requests.get(url, params=params, headers=headers)
        result = response.json()
        self._print_result(result)
        return result


    def get_price(self, interval, ticker, count):
        params = {
            'market': ticker,
            'count': count,
        }
        url = f"https://api.upbit.com/v1/candles/{interval}"
        headers = {"accept": "application/json"}
        response = requests.get(url, params=params, headers=headers)

        self._print_result(response.json())
        return response.json()

    def deposit_krw(self, amount):
        params = {
            'amount' : amount,
            'two_factor_type' : 'kakao',
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
        res = requests.post(server_url+'/v1/deposits/krw', json=params, headers=headers)
        result = res.json()
        self._print_result(result)
        return result

    def withdrawal_krw(self, amount):
        params = {
            'amount' : amount,
            'two_factor_type' : 'kakao',
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

        res = requests.post(server_url+'/v1/withdraws/krw', json=params, headers=headers)
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
        """
        Args:
            market: 마켓 ID (필수)
            side: 주문 종류 (필수)

                  - bid : 매수
                  - ask : 매도
            volume: 주문량 (지정가, 시장가 매도 시 필수)
            price: 주문 가격 (지정가, 시장가 매수 시 필수)

                      - ex) KRW-BTC 마켓에서 1BTC당 1,000 KRW로 거래할 경우, 값은 1000 이 된다.

                      - ex) KRW-BTC 마켓에서 1BTC당 매도 1호가가 500 KRW 인 경우, 시장가 매수 시 값을 1000으로 세팅하면 2BTC가 매수된다. (수수료가 존재하거나 매도 1호가의 수량에 따라 상이할 수 있음)
            ord_type: 주문 타입 (필수)

                      - limit : 지정가 주문
                      - price : 시장가 주문 (매수)
                      - market : 시장가 주문 (매도)
                      - best : 최유리 주문 (time_in_force 설정 필수)
            identifier : 조회용 사용자 지정값 (선택)
            time_in_force : IOC, FOK 주문 설정

                      - ioc : Immediate of Cancel
                      - fok : Fill or Kill
                       ** ord_type 이 best 혹인 limit 일 때만 지원됨 **



        Returns:
            dict:
                - uuid (str): 주문의 고유 아이디

                - side (str): 주문 종류

                - ord_type (str): 주문 방식

                - price (float): 주문 당시 화폐 가격

                - state (str): 주문 상태

                - market (str): 마켓의 유일키

                - created_at (str): 주문 생성 시간

                - volume (float) : 사용자가 입력한 주문 양

                - remaining_volume (float): 체결 후 남은 주문 양

                - reserved_fee (int) : 수수료로 예약된 비용

                - remaining_fee (int): 남은 수수료

                - paid_fee (int): 사용된 수수료

                - locked (int): 거래에 사용중인 비용

                - executed_volume (float) : 체결된 양

                - trades_count (int) : 해당 주문에 걸린 체결 수

                - time_int_force (str) : IOC, FOK 설정

                - identifier (str) : 조회용 사용자 지정값
        """

        params = {
            "market": market,
            "side": side,
            "ord_type": ord_type,
        }

        if side == "bid":
            params["price"] = price
        elif side == "ask":
            params["volume"] = volume

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

        try :
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
