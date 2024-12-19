class OrderParams:
    def __init__(
            self,
            market=None,
            side=None,
            volume=None,
            price=None,
            ord_type=None,
            identifier=None,
            time_in_force=None,
    ):
        self.market = market
        self.side = side
        self.volume = volume
        self.price = price
        self.ord_type = ord_type
        self.identifier = identifier
        self.time_in_force = time_in_force

    def set_market(self, market):
        self.market = market
        return self

    def set_side(self, side):
        """
        주문 종류
        bid : 매수
        ask : 매도
        """
        self.side = side
        return self

    def set_volume(self, volume):
        """
        주문량 ( 지정가, 시장가 매도 시 필수 )
        """
        self.volume = volume
        return self

    def set_price(self, price):
        """
        주문 가격 ( 지정가, 시장가 매수 시 필수 )
        """
        self.price = price
        return self

    def set_ord_type(self, ord_type):
        """
        limit  : 지정가 주문
        price  : 시장가 주문 ( 매수 )
        market : 시장가 주문 ( 매도 )
        best   : 최유리 주문 ( time_in_force 설정 필수 )
        """
        self.ord_type = ord_type
        return self

    def set_identifier(self, identifier):
        """
        조회용 사용자 지정값 ( 선택 )
        """
        self.identifier = identifier
        return self

    def set_time_in_force(self, time_in_force):
        """
        IOC, FOK 주문 설정
        ioc : Immediate or Cancel
        fok : Fill or Kill
        * ord_type 이 best 혹은 limit 일때만 지원됩니다.
        """

class PriceParams:
    def __init__(
            self,
            interval=None,
            ticker=None,
            count=None,
    ):
        self.interval = interval
        self.ticker = ticker
        self.count = count