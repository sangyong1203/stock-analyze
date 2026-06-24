from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class StockBase(BaseModel):
    code: str = Field(min_length=1, max_length=20)
    name: str = Field(min_length=1, max_length=100)
    market: str | None = None
    sector: str | None = None
    industry: str | None = None
    market_cap: Decimal | None = None
    current_price: Decimal | None = None
    change_rate: Decimal | None = None
    aliases_json: list[str] | None = None
    is_favorite: bool = False
    is_active: bool = True


class StockCreate(StockBase):
    pass


class StockUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=20)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    market: str | None = None
    sector: str | None = None
    industry: str | None = None
    market_cap: Decimal | None = None
    current_price: Decimal | None = None
    change_rate: Decimal | None = None
    aliases_json: list[str] | None = None
    is_favorite: bool | None = None
    is_active: bool | None = None


class FavoriteUpdate(BaseModel):
    is_favorite: bool


class StockRead(StockBase):
    id: int
    is_holding: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
