from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class KrxDailyCollectRequest(BaseModel):
    bas_date: str = Field(pattern=r"^\d{8}$")
    markets: list[str] = Field(default_factory=lambda: ["KOSPI", "KOSDAQ"])
    dry_run: bool = False


class KrxDailyCollectResult(BaseModel):
    bas_date: str
    markets: list[str]
    fetched_count: int = 0
    inserted_count: int = 0
    updated_count: int = 0
    stock_created_count: int = 0
    error_count: int = 0
    errors: list[str] = Field(default_factory=list)


class KrxRangeCollectRequest(BaseModel):
    date_from: str = Field(pattern=r"^\d{8}$")
    date_to: str = Field(pattern=r"^\d{8}$")
    markets: list[str] = Field(default_factory=lambda: ["KOSPI", "KOSDAQ"])
    dry_run: bool = False
    skip_empty: bool = True


class KrxRangeDateResult(BaseModel):
    bas_date: str
    fetched_count: int = 0
    inserted_count: int = 0
    updated_count: int = 0
    stock_created_count: int = 0
    skipped_empty: bool = False
    error_count: int = 0
    errors: list[str] = Field(default_factory=list)


class KrxRangeCollectResult(BaseModel):
    date_from: str
    date_to: str
    markets: list[str]
    requested_date_count: int
    fetched_count: int = 0
    inserted_count: int = 0
    updated_count: int = 0
    stock_created_count: int = 0
    skipped_empty_dates: int = 0
    error_count: int = 0
    errors: list[str] = Field(default_factory=list)
    dates: list[KrxRangeDateResult] = Field(default_factory=list)


class PriceSummary(BaseModel):
    total_price_rows: int
    latest_price_date: date | None
    kospi_price_count: int
    kosdaq_price_count: int
    latest_updated_stocks_count: int


class StockPriceRead(BaseModel):
    id: int
    stock_id: int
    market: str | None
    date: date
    timeframe: str
    open: Decimal | None
    high: Decimal | None
    low: Decimal | None
    close: Decimal | None
    volume: int | None
    trade_value: Decimal | None
    market_cap: Decimal | None
    listed_shares: int | None
    change_price: Decimal | None
    change_rate: Decimal | None
    source: str

    model_config = ConfigDict(from_attributes=True)
