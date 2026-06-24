from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class KrxDailyPrice:
    date: date
    code: str
    name: str
    market: str
    open: Decimal | None
    high: Decimal | None
    low: Decimal | None
    close: Decimal | None
    change_price: Decimal | None
    change_rate: Decimal | None
    volume: int | None
    trade_value: Decimal | None
    market_cap: Decimal | None
    listed_shares: int | None
