from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


PRICE_ALERT_TYPES = (
    "TARGET_PRICE_ABOVE",
    "TARGET_PRICE_BELOW",
    "DROP_FROM_HIGH",
    "RISE_FROM_LOW",
)


class PriceAlertBase(BaseModel):
    stock_id: int
    alert_type: str = Field(min_length=1, max_length=50)
    target_price: Decimal | None = Field(default=None, ge=0)
    threshold_percent: Decimal | None = Field(default=None, ge=0)
    is_enabled: bool = True
    memo: str | None = None


class PriceAlertCreate(PriceAlertBase):
    pass


class PriceAlertUpdate(BaseModel):
    stock_id: int | None = None
    alert_type: str | None = Field(default=None, min_length=1, max_length=50)
    target_price: Decimal | None = Field(default=None, ge=0)
    threshold_percent: Decimal | None = Field(default=None, ge=0)
    is_enabled: bool | None = None
    memo: str | None = None


class PriceAlertRead(BaseModel):
    id: int
    stock_id: int
    stock_code: str
    stock_name: str
    current_price: Decimal | None = None
    alert_type: str
    target_price: Decimal | None = None
    threshold_percent: Decimal | None = None
    lookback_days: int
    is_enabled: bool
    triggered: bool
    triggered_at: datetime | None = None
    memo: str | None = None
    created_at: datetime
    updated_at: datetime


class PriceAlertEvaluationRequest(BaseModel):
    alert_ids: list[int] | None = None
    limit: int = Field(default=20, ge=1, le=100)
    force: bool = False


class PriceAlertEvaluationItem(BaseModel):
    price_alert_id: int
    stock_id: int
    stock_code: str
    stock_name: str
    alert_type: str
    current_price: Decimal | None = None
    target_price: Decimal | None = None
    threshold_percent: Decimal | None = None
    lookback_days: int
    recent_high: Decimal | None = None
    recent_low: Decimal | None = None
    trigger_price: Decimal | None = None
    latest_price_date: datetime | None = None
    matched: bool
    status: str
    skip_reason: str | None = None
    recipient_email: str | None = None
    subject: str | None = None
    reason: str | None = None


class PriceAlertEvaluationResult(BaseModel):
    evaluated_count: int
    matched_count: int
    sendable_count: int
    sent_count: int = 0
    failed_count: int = 0
    skipped_count: int
    skipped_reasons: dict[str, int]
    daily_sent_count: int
    hourly_sent_count: int
    items: list[PriceAlertEvaluationItem]


class PriceAlertSummary(BaseModel):
    total_count: int
    enabled_count: int
    disabled_count: int
    triggered_count: int
    sent_count: int
    failed_count: int
    skipped_count: int
    today_sent_count: int
    hourly_sent_count: int


class AlertHistoryRead(BaseModel):
    id: int
    news_id: int | None = None
    stock_id: int | None = None
    price_alert_id: int | None = None
    alert_type: str
    recipient_email: str | None = None
    title: str
    message: str | None = None
    link_url: str | None = None
    status: str
    sent_at: datetime | None = None
    error_message: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
