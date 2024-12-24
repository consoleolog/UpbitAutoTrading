class Mapper:
    def __init__(
            self,
            template,
            data=None
    ):
        self.template = template
        self.data = data

class CandleMapper:
    def __init__(self):
        self.mapper = Mapper

    def init(self):
        return self.mapper(
            template="""
            CREATE TABLE IF NOT EXISTS CANDLE_DATA(
                CANDLE_ID SERIAL PRIMARY KEY,
                DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                TICKER VARCHAR(20),
                CLOSE FLOAT,
                EMA_SHORT FLOAT,
                EMA_MIDDLE FLOAT,
                EMA_LONG FLOAT,
                STAGE INTEGER,
                MACD_UPPER FLOAT,
                MACD_MIDDLE FLOAT,
                MACD_LOWER FLOAT,
                INTERVAL VARCHAR(20)
            );
            """
        )
    def insert_one(self,candle_data):
        return self.mapper(
            template="""
            INSERT INTO CANDLE_DATA(
                TICKER,
                CLOSE,
                EMA_SHORT,
                EMA_MIDDLE,
                EMA_LONG,
                STAGE,
                MACD_UPPER,
                MACD_MIDDLE,
                MACD_LOWER,
                INTERVAL 
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
                %s
            )
            """,
            data=(
                candle_data['ticker'],
                candle_data['close'],
                candle_data['ema_short'],
                candle_data['ema_middle'],
                candle_data['ema_long'],
                candle_data['stage'],
                candle_data['macd_upper'],
                candle_data['macd_middle'],
                candle_data['macd_lower'],
                candle_data['interval']
            )
        )

class OrderMapper:

    def __init__(self):
        self.mapper = Mapper

    def init(self):
        return self.mapper(
            template="""
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
            )
            """,
        )

    def insert_one(self, order_data):
        return self.mapper(
            template="""
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
            """,
            data=(
                order_data['uuid'],
                order_data['side'],
                order_data['ord_type'],
                order_data['price'],
                order_data['volume'],
                order_data['state'],
                order_data['market'],
                order_data['created_at'],
                order_data['reserve_fee'],
                order_data['remaining_fee'],
                order_data['remaining_volume'],
                order_data['paid_fee'],
                order_data['locked'],
                order_data['executed_volume'],
                order_data['trades_count'],
            )
        )