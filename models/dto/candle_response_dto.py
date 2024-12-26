from datetime import datetime


class CandleResponseDto:
    DATE = datetime.now()
    OPEN = 'open'
    HIGH = 'high'
    LOW = 'low'
    CLOSE = 'close'
    VOLUME = 'volume'
    VALUE = 'value'

