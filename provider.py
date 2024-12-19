from abc import ABCMeta
from typing import Any


class Provider(metaclass=ABCMeta):

    def _print_result(self, result):
        """
        결과 예쁘게 출력
        """

    def get_currencies(self)-> list[dict[str, Any]]:
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

    def create_order(self, params):
        """
        ** 시장가 주문 **
        =======================================
        주문 설정 방식   |   시장가 주문
        =======================================
        매수            ord_type : price
                       side     : bid
                       volume   : null 또는 생략
                       price    : 필수 입력
        =======================================
        매도            ord_type : market
                       side     : ask
                       volume   : 필수 입력
                       price    : null 또는 생략
        =======================================

        ** 지원되는 주문 타입 및 조건 **
        ============================================================
        주문 설정 방식   | 지정가 주문 (limit)     | 최유리 주문 (best)
        ============================================================
        일반            ord_type : limit          X
                       side     : bid 또는 ask
                       volume   : 필수 입력
                       price    : 필수 입력
        ============================================================
        IOC (즉시 체결 또는 취소)
                       ord_type : limit           ord_type : best
                       side     : bid 또는 ask     time_in_force : ioc (매수)
                       volume   : 필수 입력        volume : null 또는 생략
                       price    : 필수 입력        price : 필수 입력 (매도)
                       time_in_force : ioc        side : ask
                                                  volume : 필수 입력
                                                  price : null 또는 생략
        ============================================================
        FOK (전량 체결 또는 취소)
                       ord_type : limit           ord_type : best
                       side     : bid 또는 ask     time_in_force : fok (매수)
                       volume   : 필수 입력        side : bid
                       price    : 필수 입력        volume : null 또는 생략
                       time_in_force : fok        price : 필수 입력 (매도)
                                                  volume : 필수 입력
                                                  price : null 또는 생략
        ============================================================
        Args:
            market: 마켓 ID (필수)
            side : 주문 종류 (필수)

                    - bid : 매수

                    - ask : 매도

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

    def create_order_v2(
            self,
            market: str,
            side: str,
            volume: float,
            price: float,
            ord_type: str,
            identifier: str,
            time_in_force: str,
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

    def get_candles(self, interval: str, ticker: str, count: int) -> list[dict]:
        """
        Args:
            interval (str): 시간 간격.

                - seconds: 초

                - minutes/{unit}: 분 (e.g., "minutes/1", "minutes/5")

                - days: 일

                - weeks: 주

                - months: 달

            ticker (str): 마켓 코드 (e.g., "KRW-BTC").
            count (int): 캔들 개수 (최대 200개 까지 요청 가능).

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

                ** bithumb 에만 있는 항목 **

                - prev_closing_price (float): 전일 종가 (UTC 0시 기준)

                - change_price (float): 전일 종가 대비 변화 금액

                - change_rate (float): 전일 종가 대비 변화량

                - converted_trade_price (float) 종가 환산 화폐 단위로 환산된 가격 (요청에 convertingPriceUnit 파라미터가 없는 경우 해당 필드는 반환되지 않음)
        """


    def deposit_krw(self, amount: int) -> dict:
        """
        원화 입금 요청

        Args:
            amount: 출금액

        Returns:
            dict:

                - type (str): 입출금 종류

                - uuid (str): 출금의 고유 아이디

                - currency (str): 화폐를 의미하는 영문 대문자 코드

                - txid (str): 출금의 트랜잭션 아이디

                - state (str): 출금 상태

                - created_at (str): 출금 생성 시간

                - done_at (str): 출금 완료 시간

                - amount (int): 출금 금액 / 수량

                - fee (int): 출금 수수료

                - transaction_type (str): 출금 유형 ( default: 일반출금, internal: 바로출금 )
        """

    def withdrawal_krw(self, amount: int) -> dict:
        """
        원화 출금 요청

        Args:
            amount: 입금액

        Returns:
            dict:
                - type (str): 입출금 종류

                - uuid (str): 입금의 고유 아이디

                - currency (str): 화폐를 의미하는 영문 대문자 코드

                - txid (str): 입금의 트랜잭션 아이디

                - state (str): 입금 상태

                - created_at (str): 입금 생성 시간

                - done_at (str): 입금 완료 시간

                - amount (int): 입금 금액 / 수량

                - fee (int): 입금 수수료

                - transaction_type (str): 출금 유형 ( default: 일반출금, internal: 바로출금 )
        """
