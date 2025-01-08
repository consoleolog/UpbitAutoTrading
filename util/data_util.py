from pandas import DataFrame
from scipy.stats import linregress

from models.type.ema import EMA
from models.type.stage_type import StageType


def get_stage_from_ema(data: DataFrame):
    ema_short = data.iloc[-1][EMA.SHORT]
    ema_middle = data.iloc[-1][EMA.MIDDLE]
    ema_long = data.iloc[-1][EMA.LONG]
    if ema_short > ema_middle > ema_long:
        return StageType.STABLE_INCREASE
    elif ema_middle > ema_short > ema_long:
        return StageType.END_OF_INCREASE
    elif ema_middle > ema_long > ema_short:
        return StageType.START_OF_DECREASE
    elif ema_long > ema_middle > ema_short:
        return StageType.STABLE_DECREASE
    elif ema_long > ema_short > ema_middle:
        return StageType.END_OF_DECREASE
    elif ema_short > ema_long > ema_middle:
        return StageType.START_OF_INCREASE

def is_downward_trend(data):
    if len(data) < 2:
        raise ValueError("List's length is must be over 2")

    x = list(range(len(data)))
    slope, _, _, _, _ = linregress(x, data)

    return slope < 0

def is_upward_trend(data):
    if len(data) < 2:
        raise ValueError("List's length is must be over 2")

    x = list(range(len(data)))
    slope, _, _, _, _ = linregress(x, data)

    return slope > 0