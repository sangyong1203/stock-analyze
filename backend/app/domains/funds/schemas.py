from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FundPoolCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    currency: str = Field(default="KRW", min_length=1, max_length=10)
    description: str | None = None
    is_active: bool = True


class FundPoolRead(BaseModel):
    id: int
    name: str
    currency: str
    cash_balance: Decimal
    description: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FundTransactionCreate(BaseModel):
    fund_pool_id: int
    transaction_type: str = Field(min_length=1, max_length=30)
    amount: Decimal
    currency: str = Field(default="KRW", min_length=1, max_length=10)
    memo: str | None = None
    transaction_date: date


class FundTransactionRead(BaseModel):
    id: int
    fund_pool_id: int
    fund_pool_name: str
    transaction_type: str
    amount: Decimal
    currency: str
    related_trade_id: int | None = None
    memo: str | None = None
    transaction_date: date
    created_at: datetime


class FundsSummary(BaseModel):
    active_pool_count: int
    total_cash: Decimal
    total_deposit_amount: Decimal
    total_withdraw_amount: Decimal
    transaction_count: int
