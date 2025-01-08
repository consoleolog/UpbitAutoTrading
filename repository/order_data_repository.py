from logger import Logger
from models.entity.order_data import OrderData


class OrderDataRepository:
    def __init__(self, connection):
        self.connection = connection
        self.logger = Logger().get_logger(__class__.__name__)

    def init(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS ORDER_DATA (
                    ORDER_ID SERIAL PRIMARY KEY,
                    ORDER_UUID VARCHAR(255),
                    SIDE VARCHAR(20),
                    ORD_TYPE VARCHAR(20),
                    PRICE FLOAT,
                    VOLUME FLOAT,
                    STATE VARCHAR(20),
                    MARKET VARCHAR(20),
                    CREATED_AT TIMESTAMP,
                    RESERVED_FEE FLOAT,
                    REMAINING_FEE FLOAT,
                    REMAINING_VOLUME FLOAT,
                    PAID_FEE FLOAT,
                    LOCKED FLOAT,
                    EXECUTED_VOLUME FLOAT,
                    TRADES_COUNT INTEGER
                );
                """)
                self.connection.commit()
        except Exception as e:
            self.logger.warn(e)

    def save(self, order_data: OrderData):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO ORDER_DATA(
                    ORDER_UUID,
                    SIDE,
                    ORD_TYPE,
                    PRICE,
                    VOLUME,
                    STATE,
                    MARKET,
                    CREATED_AT,
                    RESERVED_FEE,
                    REMAINING_FEE,
                    REMAINING_VOLUME,
                    PAID_FEE,
                    LOCKED,
                    EXECUTED_VOLUME,
                    TRADES_COUNT 
                ) VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s 
                )
                """, (
                    order_data.order_uuid,
                    order_data.side,
                    order_data.ord_type,
                    order_data.price,
                    order_data.volume,
                    order_data.state,
                    order_data.market,
                    order_data.created_at,
                    order_data.reserved_fee,
                    order_data.remaining_fee,
                    order_data.remaining_volume,
                    order_data.paid_fee,
                    order_data.locked,
                    order_data.executed_volume,
                    order_data.trades_count
                )
                               )
                self.connection.commit()
        except Exception as e:
            self.logger.warn(e)