
class RequestOrderDto:
    class OrdType:
        BUY = 'BUY'
        SELL = 'SELL'

    def __init__(
            self,
            mode=None,
            price=None,
            volume=None,
    ):
        self.mode = mode
        self.price = price
        self.volume = volume

    def set_mode(self, mode):
        self.mode = mode
        return self
    def set_price(self, price):
        self.price = price
        return self
    def set_volume(self, volume):
        self.volume = volume
        return self
    def build(self):
        if not self.mode:
            raise ValueError("Mode is required")
        return self

    def __str__(self): return f"""RequestOrderDto(
        mode={self.mode},
        price={self.price},
        volume={self.volume}
    )"""

class ResponseOrderDto:
    def __init__(
            self,
            uuid=None,
            side=None,
            ord_type=None,
            price=None,
            volume=None,
            state=None,
            market=None,
            created_at=None,
            reserved_fee=None,
            remaining_fee=None,
            remaining_volume=None,
            paid_fee=None,
            locked=None,
            executed_volume=None,
            trades_count=None
    ):
        self.uuid = uuid
        self.side = side
        self.ord_type = ord_type
        self.price = price
        self.volume = volume
        self.state = state
        self.market = market
        self.created_at = created_at
        self.reserved_fee = reserved_fee
        self.remaining_fee = remaining_fee
        self.remaining_volume = remaining_volume
        self.paid_fee = paid_fee
        self.locked = locked
        self.executed_volume = executed_volume
        self.trades_count = trades_count

    @staticmethod
    def created_by_buy_res(dicts):
        return ResponseOrderDto(
            uuid=dicts['uuid'],
            side=dicts['side'],
            ord_type=dicts['ord_type'],
            price=dicts['price'],
            state=dicts['state'],
            market=dicts['market'],
            created_at=dicts['created_at'],
            reserved_fee=dicts['reserved_fee'],
            remaining_fee=dicts['remaining_fee'],
            paid_fee=dicts['paid_fee'],
            locked=dicts['locked'],
            executed_volume=dicts['executed_volume'],
            trades_count=dicts['trades_count']
        )

    @staticmethod
    def created_by_sell_res(dicts):
        return ResponseOrderDto(
            uuid=dicts['uuid'],
            side=dicts['side'],
            ord_type=dicts['ord_type'],
            market=dicts['market'],
            state=dicts['state'],
            created_at=dicts['created_at'],
            volume=dicts['volume'],
            remaining_volume=dicts['remaining_volume'],
            reserved_fee=dicts['reserved_fee'],
            remaining_fee=dicts['remaining_fee'],
            paid_fee=dicts['paid_fee'],
            locked=dicts['locked'],
            executed_volume=dicts['executed_volume'],
            trades_count=dicts['trades_count']
        )

    def __str__(self):
        return f"""
        ResponseOrderDto(
            uuid={self.uuid},
            side={self.side},
            ord_type={self.ord_type},
            price={self.price},
            volume={self.volume},
            state={self.state},
            market={self.market},
            created_at={self.created_at},
            reserved_fee={self.reserved_fee},
            remaining_fee={self.remaining_fee},
            remaining_volume={self.remaining_volume},
            paid_fee={self.paid_fee},
            locked={self.locked},
            executed_volume={self.executed_volume},
            trades_count={self.trades_count}
        )
        """