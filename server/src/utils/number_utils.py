def float_or_none(value: str) -> float | None:
    try:
        result = float(value)
        return result
    except ValueError:
        return None


def int_or_none(value: str) -> int | None:
    try:
        result = int(value)
        return result
    except ValueError:
        return None
