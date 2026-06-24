from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Stock
from app.domains.stocks import repository
from app.domains.stocks.schemas import FavoriteUpdate, StockCreate, StockRead, StockUpdate


def _serialize_stock(stock: Stock, is_holding: bool = False) -> StockRead:
    return StockRead.model_validate(stock).model_copy(update={"is_holding": bool(is_holding)})


def _apply_updates(instance: Stock, payload: StockUpdate) -> None:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(instance, key, value)


def get_stock_list(
    db: Session,
    search: str | None = None,
    market: str | None = None,
    is_favorite: bool | None = None,
    is_active: bool | None = True,
    is_holding: bool | None = None,
):
    rows = repository.list_stocks(
        db=db,
        search=search,
        market=market,
        is_favorite=is_favorite,
        is_active=is_active,
        is_holding=is_holding,
    )
    return [_serialize_stock(stock, is_holding) for stock, is_holding in rows]


def get_stock_detail(db: Session, stock_id: int):
    row = repository.get_stock_with_holding(db, stock_id)
    if not row:
        raise HTTPException(status_code=404, detail="stock not found")
    stock, is_holding = row
    return _serialize_stock(stock, is_holding)


def create_stock(db: Session, payload: StockCreate):
    if repository.get_stock_by_code(db, payload.code):
        raise HTTPException(status_code=409, detail="stock code already exists")
    item = Stock(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return get_stock_detail(db, item.id)


def update_stock(db: Session, stock_id: int, payload: StockUpdate):
    item = repository.get_stock(db, stock_id)
    if not item:
        raise HTTPException(status_code=404, detail="stock not found")
    if payload.code and payload.code != item.code and repository.get_stock_by_code(db, payload.code):
        raise HTTPException(status_code=409, detail="stock code already exists")
    _apply_updates(item, payload)
    db.commit()
    db.refresh(item)
    return get_stock_detail(db, item.id)


def deactivate_stock(db: Session, stock_id: int):
    item = repository.get_stock(db, stock_id)
    if not item:
        raise HTTPException(status_code=404, detail="stock not found")
    item.is_active = False
    db.commit()
    db.refresh(item)
    return get_stock_detail(db, item.id)


def set_favorite(db: Session, stock_id: int, payload: FavoriteUpdate):
    item = repository.get_stock(db, stock_id)
    if not item:
        raise HTTPException(status_code=404, detail="stock not found")
    item.is_favorite = payload.is_favorite
    db.commit()
    db.refresh(item)
    return get_stock_detail(db, item.id)
