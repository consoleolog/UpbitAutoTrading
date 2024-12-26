from models.type.unit_type import UnitType


class IntervalType:
    SECOND = "seconds"
    DAY = "days"
    MONTH = "months"
    YEAR = "years"
    def __init__(self, unit: UnitType):
        self.MINUTE = f"minutes{unit}"