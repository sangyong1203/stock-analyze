from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.responses import ok
from app.db.session import get_db
from app.domains.stocks.schemas import FavoriteUpdate, StockCreate, StockRead, StockUpdate
from app.domains.stocks.service import (
    create_stock,
    deactivate_stock,
    get_stock_detail,
    get_stock_list,
    set_favorite,
    update_stock,
)

router = APIRouter()


@router.get("", response_model=list[StockRead])
def list_items(
    search: str | None = None,
    market: str | None = None,
    is_favorite: bool | None = None,
    is_active: bool | None = True,
    is_holding: bool | None = None,
    db: Session = Depends(get_db),
):
    return get_stock_list(
        db=db,
        search=search,
        market=market,
        is_favorite=is_favorite,
        is_active=is_active,
        is_holding=is_holding,
    )


@router.get("/search", response_model=list[StockRead])
def search_items(
    q: str = Query(min_length=1),
    market: str | None = None,
    db: Session = Depends(get_db),
):
    return get_stock_list(db=db, search=q, market=market)


@router.post("", response_model=StockRead, status_code=201)
def create_item(payload: StockCreate, db: Session = Depends(get_db)):
    return create_stock(db, payload)


@router.get("/summary")
def summary():
    return ok({"menu": "stocks", "description": "종목 기본정보 조회 및 별칭 보정"})


@router.get("/{stock_id}", response_model=StockRead)
def detail_item(stock_id: int, db: Session = Depends(get_db)):
    return get_stock_detail(db, stock_id)


@router.put("/{stock_id}", response_model=StockRead)
def update_item(stock_id: int, payload: StockUpdate, db: Session = Depends(get_db)):
    return update_stock(db, stock_id, payload)


@router.delete("/{stock_id}", response_model=StockRead)
def deactivate_item(stock_id: int, db: Session = Depends(get_db)):
    return deactivate_stock(db, stock_id)


@router.patch("/{stock_id}/favorite", response_model=StockRead)
def favorite_item(stock_id: int, payload: FavoriteUpdate, db: Session = Depends(get_db)):
    return set_favorite(db, stock_id, payload)
