from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TradeCreate(BaseModel):
    fund_pool_id: int
    stock_id: int
    trade_type: str = Field(min_length=1, max_length=20)
    trade_date: date
    quantity: int = Field(ge=1)
    price: Decimal = Field(gt=0)
    fee: Decimal = Field(default=0)
    tax: Decimal = Field(default=0)
    reason: str | None = None
    memo: str | None = None


class TradeUpdate(BaseModel):
    fund_pool_id: int | None = None
    stock_id: int | None = None
    trade_type: str | None = Field(default=None, min_length=1, max_length=20)
    trade_date: date | None = None
    quantity: int | None = Field(default=None, ge=1)
    price: Decimal | None = Field(default=None, gt=0)
    fee: Decimal | None = None
    tax: Decimal | None = None
    reason: str | None = None
    memo: str | None = None


class TradeRead(BaseModel):
    id: int
    fund_pool_id: int
    fund_pool_name: str
    stock_id: int
    stock_code: str
    stock_name: str
    trade_type: str
    trade_date: date
    quantity: int
    price: Decimal
    amount: Decimal
    fee: Decimal
    tax: Decimal
    total_amount: Decimal
    average_price_at_trade: Decimal | None = None
    realized_profit_loss: Decimal | None = None
    realized_profit_loss_rate: Decimal | None = None
    reason: str | None = None
    memo: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
