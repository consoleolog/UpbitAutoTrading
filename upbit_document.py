from typing import Optional


class UpbitDocument:

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

    def get_balance(self, ticker: str)-> int :
        """
        :param ticker: 종목 코드
        :return: int
        """

    def get_currency(self, ticker: str)-> dict:
        """
        계좌 조회
        Returns:
            dict:
                - currency (str): 화폐를 의미하는 영문 대문자 코드

                - balance (int): 주문 가능 금액 / 수량

                - locked (float): 주문 중 묶여있는 금액 / 수량

                - avg_buy_price (float) : 매수 평균가

                - avg_buy_price_modified (bool): 매수 평균가 수정 여부

                - unit_currency (str): 평단가 기준 화폐
        """

    def get_second_candles(self, market: str, to: Optional[str], count: int)-> list[dict]:
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

    def get_minute_candles(self, market: str, to: Optional[str], count: int, unit: int)-> list[dict]:
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

    def get_day_candles(self, market: str, to: Optional[str], count: int, converting_price_unit: Optional[str])->list[dict]:
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

    def get_week_candles(self,  market: str, to: Optional[str], count: int) -> list[dict]:
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

    def get_month_candles(self, market: str, to: Optional[str], count: int)-> list[dict]:
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

    def create_order_v2(
            self,
            market: str,
            side: str,
            volume: Optional[float],
            price: Optional[float],
            ord_type: str,
            identifier: Optional[str],
            time_in_force: Optional[str],
    )-> dict:
        """
        ** 시장가 주문 **

        =======================================
        주문 설정 방식   |   시장가 주문
        =======================================
        매수
            - ord_type : price
            - side     : bid
            - volume   : null 또는 제외
            - price    : 필수 입력
        =======================================

        매도
            - ord_type : market
            - side     : ask
            - volume   : 필수 입력
            - price    : null 또는 제외
        =======================================

         ** 지원 되는 주문 타입 및 조건 **

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

        ============================================================

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
