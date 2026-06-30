from decimal import Decimal

from sqlalchemy.orm import Session

from app.db.models import Holding, Stock
from app.domains.portfolio.repository import get_portfolio_summary_values
from app.domains.portfolio.schemas import PortfolioSummary


def get_portfolio_summary(db: Session) -> PortfolioSummary:
    total_cash, total_invested_amount, total_market_value, total_unrealized_profit_loss, realized_profit_loss, holding_count = get_portfolio_summary_values(db)
    total_unrealized_profit_loss_rate = (total_unrealized_profit_loss / total_invested_amount) if total_invested_amount > 0 else None

    today_change_amount = Decimal("0")
    rows = (
        db.query(Holding, Stock)
        .join(Stock, Stock.id == Holding.stock_id)
        .filter(Holding.is_closed.is_(False), Holding.quantity > 0)
        .all()
    )
    for holding, stock in rows:
        current_price = Decimal(str(stock.current_price)) if stock.current_price is not None else None
        change_rate = Decimal(str(stock.change_rate)) if stock.change_rate is not None else None
        if current_price is None or change_rate is None or current_price == 0:
            continue
        previous_close = current_price / (Decimal("1") + (change_rate / Decimal("100")))
        today_change_amount += (current_price - previous_close) * Decimal(holding.quantity)
    today_change_rate = (today_change_amount / total_market_value) if total_market_value > 0 else None

    return PortfolioSummary(
        total_cash=total_cash,
        total_invested_amount=total_invested_amount,
        total_market_value=total_market_value,
        total_unrealized_profit_loss=total_unrealized_profit_loss,
        total_unrealized_profit_loss_rate=total_unrealized_profit_loss_rate,
        realized_profit_loss=realized_profit_loss,
        total_asset_value=total_cash + total_market_value,
        holding_count=holding_count,
        today_change_amount=today_change_amount,
        today_change_rate=today_change_rate,
    )
