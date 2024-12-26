from datetime import datetime

class OrderResponseDto:
    def __init__(
            self,
            uuid: str = None,
            side: str = None,
            ord_type:str = None,
            price: float = None,
            volume: float = None,
            state: str = None,
            market: str = None,
            created_at: datetime = None,
            reserved_fee: float = None,
            remaining_fee: float = None,
            remaining_volume: float = None,
            paid_fee: float = None,
            locked: float = None,
            executed_volume: float = None,
            trades_count: int = None,
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

    def __str__(self):
        return f"""OrderResponseDto(
            uuid: {self.uuid},
            side: {self.side},
            ord_type: {self.ord_type},
            price: {self.price},
            volume: {self.volume},
            state: {self.state},
            market: {self.market},
            created_at: {self.created_at},
            reserved_fee: {self.reserved_fee},
            remaining_fee: {self.remaining_fee},
            remaining_volume: {self.remaining_volume},
            paid_fee: {self.paid_fee},
            locked: {self.locked},
            executed_volume: {self.executed_volume},
            trades_count: {self.trades_count}
        )"""