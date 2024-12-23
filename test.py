
from components.strategy_component import StrategyComponent
from components.upbit_component import UpbitComponent
from config.app_properties import AppProperties
from models.candles_dto import RequestCandlesDto
from models.ma_dto import EmaDto, MacdDto
from models.order_dto import RequestOrderDto, ResponseOrderDto

tickers = [
    "KRW-BTC",
    "KRW-ETH"
]

ticker = "KRW-BTC"

upbit_component = UpbitComponent(
    app_properties=AppProperties()
)

strategy_component = StrategyComponent(
    ema_dto=EmaDto(
        short=10,
        middle=20,
        long=60
    ),
    macd_dto=MacdDto(),
)

my_krw = upbit_component.get_balance("KRW")

PRICE = my_krw / len(tickers)


request_candles_dto = (
    RequestCandlesDto()
    .set_ticker(ticker)
    .set_count(200)
    .set_interval(RequestCandlesDto.Interval.MINUTE)
    .set_unit(RequestCandlesDto.Unit.MINUTE)
    .build())

df = strategy_component.get_macd(
    df=strategy_component.get_ema(
        df=upbit_component.get_candles(request_candles_dto),
    )
)

ord_type = strategy_component.before_order(df)

my_balance = upbit_component.get_balance(ticker)

# res = upbit_component.create_buy_order(ticker, 6000)

# result = ResponseOrderDto.create_by_dict(res)
# print(res)
# print(result)
#
# # if ord_type.mode == RequestOrderDto.OrdType.BUY and my_balance == 0:
# #     res = upbit_component.create_buy_order(
# #         ticker=ticker,
# #         price=PRICE
# #     )
# #     result = ResponseOrderDto.create_by_dict(res)
# #
# # elif ord_type.mode == RequestOrderDto.OrdType.SELL and my_balance != 0:
# #     res = upbit_component.create_sell_order(
# #         ticker=ticker,
# #         volume=my_balance,
# #     )
# #     result = ResponseOrderDto.create_by_dict(res)
# # else:
# #     pass
# res = upbit_component.create_buy_order(ticker, 6000)
res = upbit_component.create_sell_order(ticker, my_balance)
print(res)

# result = ResponseOrderDto.created_by_buy_res(res)
result = ResponseOrderDto.created_by_sell_res(res)

print(result)



