from functools import wraps


def round0(func):
    """Round to whole."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> int:
        return round(func(*args, **kwargs))

    return wrapper


def round01(func):
    """Round to tenths place"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> int:
        return round(func(*args, **kwargs), 1)

    return wrapper


def round02(func):
    """Rounding to 0, 0.2, 0.4, 0.6, 0,8."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> float:
        return round(func(*args, **kwargs) * 5) / 5

    return wrapper
