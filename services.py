from dotenv import load_dotenv

from logger import Logger
from mappers import CandleMapper, OrderMapper


class CandleService:
    def __init__(
            self,
            candle_mapper: CandleMapper,
            connection
    ):
        self.candle_mapper = candle_mapper
        self.connection = connection
        self.logger = Logger().get_logger(__class__.__name__)

    def init(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.candle_mapper.init().template)
            self.connection.commit()

    def add_one(self, data):
        mapper = self.candle_mapper.insert_one(data)
        with self.connection.cursor() as cursor:
            cursor.execute(
                mapper.template,
                mapper.data
            )
            self.connection.commit()


class OrderService:
    def __init__(
            self,
            order_mapper: OrderMapper,
            connection
    ):
        self.order_mapper = order_mapper
        self.connection = connection
        self.logger = Logger().get_logger(__class__.__name__)

    def init(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.order_mapper.init().template)
            self.connection.commit()

    def add_one(self, data):
        mapper = self.order_mapper.insert_one(data)
        with self.connection.cursor() as cursor:
            cursor.execute(
                mapper.template,
                mapper.data
            )
            self.connection.commit()

load_dotenv()

# def send_mail():
