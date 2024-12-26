from datetime import datetime

from models.dto.order_response_dto import OrderResponseDto


class OrderData:
    def __init__(
            self,
            order_id: int = None,
            order_uuid: str = None,
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
        self.order_id = order_id
        self.order_uuid = order_uuid
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
    def create_by_order_response_dto(order_response_dto: OrderResponseDto):
        return OrderData(
            order_uuid=order_response_dto.uuid,
            side=order_response_dto.side,
            ord_type=order_response_dto.ord_type,
            price=order_response_dto.price,
            volume=order_response_dto.volume,
            state=order_response_dto.state,
            market=order_response_dto.market,
            created_at=order_response_dto.created_at,
            reserved_fee=order_response_dto.reserved_fee,
            remaining_fee=order_response_dto.remaining_fee,
            remaining_volume=order_response_dto.remaining_volume,
            paid_fee=order_response_dto.paid_fee,
            locked=order_response_dto.locked,
            executed_volume=order_response_dto.executed_volume,
            trades_count=order_response_dto.trades_count,
        )