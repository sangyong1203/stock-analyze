from sqlalchemy.orm import Session

from app.db.models import FundPool, FundTransaction, Stock, Trade


def list_trades(db: Session):
    return (
        db.query(Trade, FundPool.name, Stock.code, Stock.name)
        .join(FundPool, FundPool.id == Trade.fund_pool_id)
        .join(Stock, Stock.id == Trade.stock_id)
        .order_by(Trade.trade_date.desc(), Trade.id.desc())
        .limit(300)
        .all()
    )


def get_trade_detail_row(db: Session, trade_id: int):
    return (
        db.query(Trade, FundPool.name, Stock.code, Stock.name)
        .join(FundPool, FundPool.id == Trade.fund_pool_id)
        .join(Stock, Stock.id == Trade.stock_id)
        .filter(Trade.id == trade_id)
        .first()
    )


def get_trade(db: Session, trade_id: int) -> Trade | None:
    return db.get(Trade, trade_id)


def get_trade_fund_transaction(db: Session, trade_id: int) -> FundTransaction | None:
    return db.query(FundTransaction).filter(FundTransaction.related_trade_id == trade_id).first()
