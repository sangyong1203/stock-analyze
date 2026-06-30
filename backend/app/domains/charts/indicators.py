from decimal import Decimal, ROUND_HALF_UP


def _round(value: Decimal | None) -> Decimal | None:
    if value is None:
        return None
    return value.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def _average(values: list[Decimal]) -> Decimal:
    return sum(values, Decimal("0")) / Decimal(len(values))


def calculate_sma(values: list[Decimal | None], period: int) -> list[Decimal | None]:
    result: list[Decimal | None] = []
    for index in range(len(values)):
        window = values[index - period + 1 : index + 1]
        if len(window) < period or any(value is None for value in window):
            result.append(None)
            continue
        result.append(_round(_average([value for value in window if value is not None])))
    return result


def calculate_rsi(values: list[Decimal | None], period: int = 14) -> list[Decimal | None]:
    result: list[Decimal | None] = [None] * len(values)
    if len(values) <= period:
        return result

    for index in range(period, len(values)):
        gains: list[Decimal] = []
        losses: list[Decimal] = []
        valid = True
        for cursor in range(index - period + 1, index + 1):
            current = values[cursor]
            previous = values[cursor - 1]
            if current is None or previous is None:
                valid = False
                break
            change = current - previous
            gains.append(max(change, Decimal("0")))
            losses.append(abs(min(change, Decimal("0"))))
        if not valid:
            continue
        avg_gain = _average(gains)
        avg_loss = _average(losses)
        if avg_loss == 0:
            result[index] = Decimal("100") if avg_gain > 0 else Decimal("0")
            continue
        rs = avg_gain / avg_loss
        result[index] = _round(Decimal("100") - (Decimal("100") / (Decimal("1") + rs)))
    return result


def calculate_ema(values: list[Decimal | None], period: int) -> list[Decimal | None]:
    result: list[Decimal | None] = [None] * len(values)
    multiplier = Decimal("2") / Decimal(period + 1)
    ema: Decimal | None = None

    for index, value in enumerate(values):
        if value is None:
            continue
        if index < period - 1:
            continue
        if ema is None:
            seed_window = values[index - period + 1 : index + 1]
            if len(seed_window) < period or any(item is None for item in seed_window):
                continue
            ema = _average([item for item in seed_window if item is not None])
        else:
            ema = (value - ema) * multiplier + ema
        result[index] = _round(ema)
    return result


def calculate_macd(values: list[Decimal | None], fast: int = 12, slow: int = 26, signal: int = 9) -> tuple[list[Decimal | None], list[Decimal | None], list[Decimal | None]]:
    ema_fast = calculate_ema(values, fast)
    ema_slow = calculate_ema(values, slow)
    macd: list[Decimal | None] = []
    for fast_value, slow_value in zip(ema_fast, ema_slow):
        if fast_value is None or slow_value is None:
            macd.append(None)
        else:
            macd.append(_round(fast_value - slow_value))

    signal_line = calculate_ema(macd, signal)
    histogram: list[Decimal | None] = []
    for macd_value, signal_value in zip(macd, signal_line):
        if macd_value is None or signal_value is None:
            histogram.append(None)
        else:
            histogram.append(_round(macd_value - signal_value))
    return macd, signal_line, histogram


def calculate_indicators(closes: list[Decimal | None]) -> dict[str, list[Decimal | None]]:
    macd, macd_signal, macd_histogram = calculate_macd(closes)
    return {
        "ma20": calculate_sma(closes, 20),
        "ma60": calculate_sma(closes, 60),
        "ma120": calculate_sma(closes, 120),
        "rsi14": calculate_rsi(closes, 14),
        "macd": macd,
        "macd_signal": macd_signal,
        "macd_histogram": macd_histogram,
    }
