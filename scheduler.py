from apscheduler.schedulers.background import BackgroundScheduler

from components import UpbitComponent, StrategyComponent
from config import AppProperties
from database import connection
from logger import Logger
from mappers import CandleMapper, OrderMapper
from models import RequestCandlesDto, EmaDto, MacdDto, ResponseCandlesDto, RequestOrderDto, ResponseOrderDto
from services import CandleService, OrderService

logger = Logger().get_logger(__name__)

tickers = [
    "KRW-BTC",
    "KRW-ETH"
]

upbit_component = UpbitComponent(
    app_properties=AppProperties()
)

my_krw = upbit_component.get_balance("KRW")

PRICE = my_krw / len(tickers)

candle_service = CandleService(
    connection=connection,
    candle_mapper=CandleMapper(),
)
order_service = OrderService(
    connection=connection,
    order_mapper=OrderMapper(),
)

def init():
    logger.info("""
    =======================
    
        TABLE INITIALIZE
    
    =======================
    """)
    candle_service.init()
    order_service.init()


def run(
        request_candles_dto: RequestCandlesDto,
        ema_dto: EmaDto,
        macd_dto: MacdDto,
):
    def create_candle_data(df):
        last_df = df.iloc[-1]

        ema_short = last_df[ema_dto.SHORT.name]
        ema_middle = last_df[ema_dto.MIDDLE.name]
        ema_long = last_df[ema_dto.LONG.name]

        candle_data = {
            "ticker": ticker,
            "close": last_df[ResponseCandlesDto.Df.CLOSE],
            "ema_short": ema_short,
            "ema_middle": ema_middle,
            "ema_long": ema_long,
            "macd_upper": last_df[macd_dto.UPPER.name],
            "macd_middle": last_df[macd_dto.MIDDLE.name],
            "macd_lower": last_df[macd_dto.LOWER.name],
            "interval": interval,
        }

        if ema_short > ema_middle > ema_long:
            candle_data['stage'] = 1
        elif ema_middle > ema_short > ema_long:
            candle_data['stage'] = 2
        elif ema_middle > ema_long > ema_short:
            candle_data['stage'] = 3
        elif ema_long > ema_middle > ema_short:
            candle_data['stage'] = 4
        elif ema_long > ema_short > ema_middle:
            candle_data['stage'] = 5
        elif ema_short > ema_long > ema_middle:
            candle_data['stage'] = 6

        return candle_data

    interval = request_candles_dto.interval
    unit = request_candles_dto.unit
    if request_candles_dto.interval == RequestCandlesDto.Interval.MINUTE and unit:
        interval = f"{interval}{unit}"

    logger.info(f"""
    =======================
            JOB START

      Interval : {interval}  
 
    =======================
    """)
    ticker = request_candles_dto.ticker

    strategy_component = StrategyComponent(
        ema_dto=ema_dto,
        macd_dto=macd_dto,
    )

    df = strategy_component.get_macd(
        df=strategy_component.get_ema(
            df=upbit_component.get_candles(request_candles_dto),
        )
    )

    candle_data = create_candle_data(df)

    candle_service.add_one(candle_data)

    ord_type = strategy_component.before_order(df)

    my_balance = upbit_component.get_balance(ticker)

    if ord_type.mode == RequestOrderDto.OrdType.BUY and my_balance == 0:
        res = upbit_component.create_buy_order(
            ticker=ticker,
            price=PRICE
        )
        result = ResponseOrderDto.created_by_buy_res(res)
        logger.info(result)
        order_service.add_one(result)

    elif ord_type.mode == RequestOrderDto.OrdType.SELL and my_balance != 0:
        res = upbit_component.create_sell_order(
            ticker=ticker,
            volume=my_balance,
        )
        result = ResponseOrderDto.created_by_sell_res(res)
        logger.info(result)
        order_service.add_one(result)
    else:
        pass

scheduler = BackgroundScheduler()

scheduler.add_job(run, "interval", minutes=RequestCandlesDto.Unit.MINUTE_5, kwargs={
    "request_candles_dto": (RequestCandlesDto().
                            set_ticker("KRW-BTC")
                            .set_count(200)
                            .set_interval(RequestCandlesDto.Interval.MINUTE)
                            .set_unit(RequestCandlesDto.Unit.MINUTE_5)
                            .build()),
    "ema_dto": EmaDto(
        short=14,
        middle=28,
        long=60
    ),
    "macd_dto": MacdDto()
})
scheduler.add_job(run, "interval", minutes=RequestCandlesDto.Unit.MINUTE_10, kwargs={
    "request_candles_dto": (RequestCandlesDto().
                            set_ticker("KRW-BTC")
                            .set_count(200)
                            .set_interval(RequestCandlesDto.Interval.MINUTE)
                            .set_unit(RequestCandlesDto.Unit.MINUTE_10)
                            .build()),
    "ema_dto": EmaDto(
        short=14,
        middle=28,
        long=56
    ),
    "macd_dto": MacdDto(),
})
scheduler.add_job(run, "interval", minutes=RequestCandlesDto.Unit.MINUTE_15, kwargs={
    "request_candles_dto": (RequestCandlesDto()
                            .set_ticker("KRW-BTC")
                            .set_count(200)
                            .set_interval(RequestCandlesDto.Interval.MINUTE)
                            .set_unit(RequestCandlesDto.Unit.MINUTE_15)
                            .build()),
    "ema_dto": EmaDto(
        short=14,
        middle=28,
        long=60
    ),
    "macd_dto": MacdDto()
})
scheduler.add_job(run, "interval", minutes=RequestCandlesDto.Unit.HALF_HOUR, kwargs={
    "request_candles_dto": (RequestCandlesDto()
                            .set_ticker("KRW-BTC")
                            .set_count(200)
                            .set_interval(RequestCandlesDto.Interval.MINUTE)
                            .set_unit(RequestCandlesDto.Unit.HALF_HOUR)
                            .build()),
    "ema_dto": EmaDto(
        short=14,
        middle=28,
        long=60
    ),
    "macd_dto": MacdDto(),
})
scheduler.add_job(run, "interval", minutes=RequestCandlesDto.Unit.HOUR, kwargs={
    "request_candles_dto": (RequestCandlesDto()
                            .set_ticker("KRW-BTC")
                            .set_count(200)
                            .set_interval(RequestCandlesDto.Interval.MINUTE)
                            .set_unit(RequestCandlesDto.Unit.HOUR)
                            .build()),
    "ema_dto": EmaDto(
        short=14,
        middle=28,
        long=60
    ),
    "macd_dto": MacdDto()
})
scheduler.add_job(run, "interval", minutes=RequestCandlesDto.Unit.HOUR_4, kwargs={
    "request_candles_dto": (RequestCandlesDto()
                            .set_ticker("KRW-BTC")
                            .set_count(200)
                            .set_interval(RequestCandlesDto.Interval.MINUTE)
                            .set_unit(RequestCandlesDto.Unit.HOUR_4)
                            .build()),
    "ema_dto": EmaDto(
        short=14,
        middle=28,
        long=60
    ),
    "macd_dto": MacdDto()
})
scheduler.add_job(run, "interval", days=1, kwargs={
    "request_candles_dto": (RequestCandlesDto()
                            .set_ticker("KRW-BTC")
                            .set_count(200)
                            .set_interval(RequestCandlesDto.Interval.DAY)
                            .build()),
    "ema_dto": EmaDto(
        short=14,
        middle=28,
        long=60
    ),
    "macd_dto": MacdDto()
})

