from math import floor
from time import time
from datetime import datetime


def current_millis() -> int:
    return floor(time() * 1000.0)


def millis_to_datetime(millis: int) -> datetime:
    return datetime.fromtimestamp(millis / 1000.0)


def datetime_to_millis(dt: datetime) -> int:
    return floor(dt.timestamp() * 1000.0)
