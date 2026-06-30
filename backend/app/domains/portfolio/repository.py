from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import FundPool, Holding


def get_portfolio_summary_values(db: Session) -> tuple[Decimal, Decimal, Decimal, Decimal, Decimal, int]:
    total_cash = db.query(func.coalesce(func.sum(FundPool.cash_balance), 0)).filter(FundPool.is_active.is_(True)).scalar() or Decimal("0")
    total_invested_amount = (
        db.query(func.coalesce(func.sum(Holding.total_buy_amount), 0)).filter(Holding.is_closed.is_(False), Holding.quantity > 0).scalar() or Decimal("0")
    )
    total_market_value = (
        db.query(func.coalesce(func.sum(Holding.market_value), 0)).filter(Holding.is_closed.is_(False), Holding.quantity > 0).scalar() or Decimal("0")
    )
    total_unrealized_profit_loss = (
        db.query(func.coalesce(func.sum(Holding.unrealized_profit_loss), 0)).filter(Holding.is_closed.is_(False), Holding.quantity > 0).scalar() or Decimal("0")
    )
    realized_profit_loss = db.query(func.coalesce(func.sum(Holding.realized_profit_loss), 0)).scalar() or Decimal("0")
    holding_count = db.query(func.count(Holding.id)).filter(Holding.is_closed.is_(False), Holding.quantity > 0).scalar() or 0
    return total_cash, total_invested_amount, total_market_value, total_unrealized_profit_loss, realized_profit_loss, holding_count
