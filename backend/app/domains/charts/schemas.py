from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class ChartSummary(BaseModel):
    timeframe: str = "daily"


class OhlcvPoint(BaseModel):
    date: date
    open: Decimal | None
    high: Decimal | None
    low: Decimal | None
    close: Decimal | None
    volume: int | None
    change_rate: Decimal | None


class OhlcvResponse(BaseModel):
    stock_id: int
    timeframe: str
    items: list[OhlcvPoint]
