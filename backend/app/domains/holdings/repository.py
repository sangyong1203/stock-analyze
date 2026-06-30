from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import FundPool, Holding, Stock, Trade


def list_holdings(db: Session) -> list[tuple[Holding, str, str, str, str]]:
    return (
        db.query(Holding, FundPool.name, Stock.code, Stock.name, Stock.market)
        .join(FundPool, FundPool.id == Holding.fund_pool_id)
        .join(Stock, Stock.id == Holding.stock_id)
        .order_by(Holding.is_closed.asc(), Holding.market_value.desc().nullslast(), Stock.code)
        .all()
    )


def get_holding_summary_values(db: Session) -> tuple[int, int, Decimal, Decimal, Decimal]:
    holding_count = db.query(func.count(Holding.id)).filter(Holding.is_closed.is_(False), Holding.quantity > 0).scalar() or 0
    closed_holding_count = db.query(func.count(Holding.id)).filter(Holding.is_closed.is_(True)).scalar() or 0
    total_market_value = db.query(func.coalesce(func.sum(Holding.market_value), 0)).filter(Holding.is_closed.is_(False)).scalar() or Decimal("0")
    total_unrealized_profit_loss = (
        db.query(func.coalesce(func.sum(Holding.unrealized_profit_loss), 0)).filter(Holding.is_closed.is_(False)).scalar() or Decimal("0")
    )
    total_realized_profit_loss = db.query(func.coalesce(func.sum(Holding.realized_profit_loss), 0)).scalar() or Decimal("0")
    return holding_count, closed_holding_count, total_market_value, total_unrealized_profit_loss, total_realized_profit_loss


def list_target_pool_ids(db: Session, fund_pool_id: int | None = None) -> list[int]:
    if fund_pool_id is not None:
        return [fund_pool_id]
    rows = db.query(Trade.fund_pool_id).distinct().order_by(Trade.fund_pool_id).all()
    return [row[0] for row in rows]
