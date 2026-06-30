from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domains.trades.schemas import TradeCreate, TradeRead, TradeUpdate
from app.domains.trades.service import create_trade, delete_trade, get_trade_detail, get_trade_list, update_trade

router = APIRouter()


@router.get("", response_model=list[TradeRead])
def list_items(db: Session = Depends(get_db)):
    return get_trade_list(db)


@router.post("", response_model=TradeRead, status_code=201)
def create_item(payload: TradeCreate, db: Session = Depends(get_db)):
    return create_trade(db, payload)


@router.get("/{trade_id}", response_model=TradeRead)
def detail_item(trade_id: int, db: Session = Depends(get_db)):
    return get_trade_detail(db, trade_id)


@router.patch("/{trade_id}", response_model=TradeRead)
def patch_item(trade_id: int, payload: TradeUpdate, db: Session = Depends(get_db)):
    return update_trade(db, trade_id, payload)


@router.delete("/{trade_id}")
def delete_item(trade_id: int, db: Session = Depends(get_db)):
    return delete_trade(db, trade_id)
