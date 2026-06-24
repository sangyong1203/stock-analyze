from sqlalchemy import exists, or_
from sqlalchemy.orm import Session

from app.db.models import Holding, Stock


def holding_exists_expression():
    return exists().where(
        Holding.stock_id == Stock.id,
        Holding.is_closed.is_(False),
        Holding.quantity > 0,
    )


def list_stocks(
    db: Session,
    search: str | None = None,
    market: str | None = None,
    is_favorite: bool | None = None,
    is_active: bool | None = True,
    is_holding: bool | None = None,
):
    holding_exists = holding_exists_expression()
    query = db.query(Stock, holding_exists.label("is_holding"))

    if search:
        keyword = f"%{search.strip()}%"
        query = query.filter(or_(Stock.code.like(keyword), Stock.name.like(keyword)))
    if market:
        query = query.filter(Stock.market == market)
    if is_favorite is not None:
        query = query.filter(Stock.is_favorite.is_(is_favorite))
    if is_active is not None:
        query = query.filter(Stock.is_active.is_(is_active))
    if is_holding is True:
        query = query.filter(holding_exists)
    elif is_holding is False:
        query = query.filter(~holding_exists)

    return query.order_by(Stock.code).limit(500).all()


def get_stock_with_holding(db: Session, stock_id: int):
    holding_exists = holding_exists_expression()
    return db.query(Stock, holding_exists.label("is_holding")).filter(Stock.id == stock_id).first()


def get_stock_by_code(db: Session, code: str):
    return db.query(Stock).filter(Stock.code == code).first()


def get_stock(db: Session, stock_id: int):
    return db.get(Stock, stock_id)
