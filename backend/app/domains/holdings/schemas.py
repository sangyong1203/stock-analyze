from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class HoldingRead(BaseModel):
    id: int
    fund_pool_id: int
    fund_pool_name: str
    stock_id: int
    stock_code: str
    stock_name: str
    quantity: int
    average_price: Decimal
    total_buy_amount: Decimal
    current_price: Decimal | None = None
    market_value: Decimal | None = None
    unrealized_profit_loss: Decimal | None = None
    unrealized_profit_loss_rate: Decimal | None = None
    realized_profit_loss: Decimal
    first_buy_date: date | None = None
    last_trade_date: date | None = None
    is_closed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HoldingSummary(BaseModel):
    holding_count: int
    closed_holding_count: int
    total_market_value: Decimal
    total_unrealized_profit_loss: Decimal
    total_realized_profit_loss: Decimal


class HoldingRecalculateResult(BaseModel):
    fund_pool_ids: list[int]
    processed_trade_count: int
    holding_count: int
