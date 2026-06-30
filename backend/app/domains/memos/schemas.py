from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


MEMO_TYPES = ("stock", "trade", "news", "general")


class MemoCreate(BaseModel):
    memo_type: str = Field(min_length=1, max_length=30)
    title: str | None = Field(default=None, max_length=255)
    content: str = Field(min_length=1)
    stock_id: int | None = None
    trade_id: int | None = None
    news_id: int | None = None
    memo_date: date | None = None
    context_json: dict[str, Any] | None = None


class MemoUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    content: str | None = None
    memo_date: date | None = None
    context_json: dict[str, Any] | None = None


class MemoRead(BaseModel):
    id: int
    memo_type: str
    title: str | None = None
    content: str
    stock_id: int | None = None
    trade_id: int | None = None
    news_id: int | None = None
    price_snapshot_id: int | None = None
    memo_date: date | None = None
    context_json: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
