from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import FundPool, FundTransaction
from app.domains.funds import repository
from app.domains.funds.schemas import (
    FundPoolCreate,
    FundPoolRead,
    FundsSummary,
    FundTransactionCreate,
    FundTransactionRead,
)

ALLOWED_MANUAL_TRANSACTION_TYPES = {"deposit", "withdraw", "dividend", "fee", "tax", "adjustment"}
POSITIVE_TRANSACTION_TYPES = {"deposit", "dividend", "sell"}
NEGATIVE_TRANSACTION_TYPES = {"withdraw", "buy", "fee", "tax"}


def _to_decimal(value: Decimal | int | float | str) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))


def _cash_delta(transaction_type: str, amount: Decimal) -> Decimal:
    normalized = transaction_type.lower()
    decimal_amount = _to_decimal(amount)
    if normalized in POSITIVE_TRANSACTION_TYPES:
        return decimal_amount
    if normalized in NEGATIVE_TRANSACTION_TYPES:
        return -decimal_amount
    if normalized == "adjustment":
        return decimal_amount
    raise HTTPException(status_code=400, detail="unsupported fund transaction type")


def _serialize_transaction(item: FundTransaction, fund_pool_name: str) -> FundTransactionRead:
    return FundTransactionRead(
        id=item.id,
        fund_pool_id=item.fund_pool_id,
        fund_pool_name=fund_pool_name,
        transaction_type=item.transaction_type,
        amount=item.amount,
        currency=item.currency,
        related_trade_id=item.related_trade_id,
        memo=item.memo,
        transaction_date=item.transaction_date,
        created_at=item.created_at,
    )


def list_pools(db: Session) -> list[FundPoolRead]:
    return [FundPoolRead.model_validate(row) for row in repository.list_fund_pools(db)]


def create_pool(db: Session, payload: FundPoolCreate) -> FundPoolRead:
    item = FundPool(name=payload.name, currency=payload.currency, description=payload.description, is_active=payload.is_active)
    db.add(item)
    db.commit()
    db.refresh(item)
    return FundPoolRead.model_validate(item)


def list_transactions(db: Session, fund_pool_id: int | None = None) -> list[FundTransactionRead]:
    return [_serialize_transaction(item, fund_pool_name) for item, fund_pool_name in repository.list_fund_transactions(db, fund_pool_id)]


def create_transaction(db: Session, payload: FundTransactionCreate) -> FundTransactionRead:
    normalized = payload.transaction_type.lower()
    if normalized not in ALLOWED_MANUAL_TRANSACTION_TYPES:
        raise HTTPException(status_code=400, detail="manual fund transactions support deposit/withdraw/dividend/fee/tax/adjustment only")
    fund_pool = repository.get_fund_pool(db, payload.fund_pool_id)
    if fund_pool is None:
        raise HTTPException(status_code=404, detail="fund pool not found")
    delta = _cash_delta(normalized, payload.amount)
    if fund_pool.cash_balance + delta < Decimal("0"):
        raise HTTPException(status_code=400, detail="insufficient cash balance")

    item = FundTransaction(
        fund_pool_id=payload.fund_pool_id,
        transaction_type=normalized,
        amount=payload.amount,
        currency=payload.currency,
        memo=payload.memo,
        transaction_date=payload.transaction_date,
    )
    db.add(item)
    fund_pool.cash_balance += delta
    db.commit()
    db.refresh(item)
    return _serialize_transaction(item, fund_pool.name)


def get_summary(db: Session) -> FundsSummary:
    active_pool_count, total_cash, total_deposit_amount, total_withdraw_amount, transaction_count = repository.get_summary_values(db)
    return FundsSummary(
        active_pool_count=active_pool_count,
        total_cash=total_cash,
        total_deposit_amount=total_deposit_amount,
        total_withdraw_amount=total_withdraw_amount,
        transaction_count=transaction_count,
    )
