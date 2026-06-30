from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import FundPool, FundTransaction


def list_fund_pools(db: Session) -> list[FundPool]:
    return db.query(FundPool).order_by(FundPool.id).all()


def get_fund_pool(db: Session, fund_pool_id: int) -> FundPool | None:
    return db.get(FundPool, fund_pool_id)


def list_fund_transactions(db: Session, fund_pool_id: int | None = None) -> list[tuple[FundTransaction, str]]:
    query = db.query(FundTransaction, FundPool.name).join(FundPool, FundPool.id == FundTransaction.fund_pool_id)
    if fund_pool_id is not None:
        query = query.filter(FundTransaction.fund_pool_id == fund_pool_id)
    return query.order_by(FundTransaction.transaction_date.desc(), FundTransaction.id.desc()).limit(300).all()


def get_summary_values(db: Session) -> tuple[int, Decimal, Decimal, Decimal, int]:
    active_pool_count = db.query(func.count(FundPool.id)).filter(FundPool.is_active.is_(True)).scalar() or 0
    total_cash = db.query(func.coalesce(func.sum(FundPool.cash_balance), 0)).filter(FundPool.is_active.is_(True)).scalar() or Decimal("0")
    total_deposit_amount = (
        db.query(func.coalesce(func.sum(FundTransaction.amount), 0))
        .filter(FundTransaction.transaction_type == "deposit")
        .scalar()
        or Decimal("0")
    )
    total_withdraw_amount = (
        db.query(func.coalesce(func.sum(FundTransaction.amount), 0))
        .filter(FundTransaction.transaction_type == "withdraw")
        .scalar()
        or Decimal("0")
    )
    transaction_count = db.query(func.count(FundTransaction.id)).scalar() or 0
    return active_pool_count, total_cash, total_deposit_amount, total_withdraw_amount, transaction_count
