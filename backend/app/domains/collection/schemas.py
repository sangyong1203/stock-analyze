from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict


class IndexConstituentImportRequest(BaseModel):
    file_path: str
    index_code: str
    index_name: str
    tracking_index: str | None = None
    effective_date: date
    source: str = "manual"


class IndexConstituentRead(BaseModel):
    id: int
    index_code: str
    index_name: str
    tracking_index: str | None = None
    stock_id: int | None = None
    stock_code: str
    stock_name: str
    market: str | None = None
    effective_date: date
    is_active: bool
    source: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IndexConstituentSummary(BaseModel):
    total_count: int
    active_count: int
    kodex_200_count: int
    kodex_kosdaq150_count: int


class CollectionRuleBase(BaseModel):
    name: str
    rule_type: str
    enabled: bool = True
    condition_json: dict[str, Any] | None = None
    priority: int = 100


class CollectionRuleCreate(CollectionRuleBase):
    pass


class CollectionRuleUpdate(BaseModel):
    name: str | None = None
    rule_type: str | None = None
    enabled: bool | None = None
    condition_json: dict[str, Any] | None = None
    priority: int | None = None


class CollectionRuleRead(CollectionRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CollectionStockUpdate(BaseModel):
    collect_enabled: bool | None = None
    collect_news: bool | None = None
    collect_price_snapshot: bool | None = None
    collect_alert_enabled: bool | None = None
    priority: str | None = None
    collect_reason: str | None = None
    manual_override: bool | None = None
    manual_include: bool | None = None
    manual_exclude: bool | None = None


class CollectionStockRead(BaseModel):
    stock_id: int
    stock_code: str
    stock_name: str
    market: str | None = None
    sector: str | None = None
    market_cap: Decimal | None = None
    current_price: Decimal | None = None
    is_favorite: bool
    is_holding_calculated: bool
    collect_enabled: bool
    collect_news: bool
    collect_price_snapshot: bool
    collect_alert_enabled: bool
    priority: str
    collect_reason: str | None = None
    manual_override: bool
    manual_include: bool
    manual_exclude: bool
    last_collected_at: datetime | None = None


class CollectionStockSummary(BaseModel):
    total_candidate_count: int
    collect_enabled_count: int
    collect_news_count: int
    collect_alert_enabled_count: int
    manual_include_count: int
    manual_exclude_count: int


class CollectionStockListResponse(BaseModel):
    items: list[CollectionStockRead]
    total_count: int
    page: int
    page_size: int


class RecalculateResult(BaseModel):
    processed_count: int
    collect_enabled_count: int
    manual_exclude_count: int


class ImportResult(BaseModel):
    imported_count: int
    created_stock_count: int
    updated_existing_count: int
    deactivated_previous_count: int
