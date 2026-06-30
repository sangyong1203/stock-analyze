from decimal import Decimal

from pydantic import BaseModel


class PortfolioSummary(BaseModel):
    total_cash: Decimal
    total_invested_amount: Decimal
    total_market_value: Decimal
    total_unrealized_profit_loss: Decimal
    total_unrealized_profit_loss_rate: Decimal | None = None
    realized_profit_loss: Decimal
    total_asset_value: Decimal
    holding_count: int
    today_change_amount: Decimal
    today_change_rate: Decimal | None = None
