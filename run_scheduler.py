from multiprocessing.dummy import Pool as ThreadPool
from apscheduler.schedulers.background import BackgroundScheduler
from scipy.constants import minute

from components.strategy_component import StrategyComponent
from components.upbit_component import UpbitComponent
from config.app_properties import AppProperties
from logger import Logger
from models.candles_dto import RequestCandlesDto
from models.ma_dto import EmaDto, MacdDto
from models.order_dto import RequestOrderDto, ResponseOrderDto


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

def run(
        request_candles_dto: RequestCandlesDto,
        ema_dto: EmaDto,
        macd_dto: MacdDto,
):
    logger.info("=======================")
    logger.info("       JOB START       ")
    logger.info(f"  Interval : {request_candles_dto.interval}  ")
    logger.info(f"  Unit : {request_candles_dto.unit}    ")
    logger.info("=======================")
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

    ord_type = strategy_component.before_order(df)

    my_balance = upbit_component.get_balance(ticker)

    # if ord_type.mode == RequestOrderDto.OrdType.BUY and my_balance == 0:
    #     res = upbit_component.create_buy_order(
    #         ticker=ticker,
    #         price=PRICE
    #     )
    #     result = ResponseOrderDto.created_by_buy_res(res)
    #     logger.info(result)
    #
    # elif ord_type.mode == RequestOrderDto.OrdType.SELL and my_balance != 0:
    #     res = upbit_component.create_sell_order(
    #         ticker=ticker,
    #         volume=my_balance,
    #     )
    #     result = ResponseOrderDto.created_by_sell_res(res)
    #     logger.info(result)
    #
    # else:
    #     pass

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

