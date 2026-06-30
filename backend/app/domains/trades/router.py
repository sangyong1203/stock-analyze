from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domains.trades.schemas import NewsTradeRead, TradeCreate, TradeNewsLinkCreate, TradeNewsRead, TradeRead, TradeUpdate
from app.domains.trades.service import (
    create_trade,
    delete_trade,
    get_news_related_trades,
    get_trade_detail,
    get_trade_list,
    get_trade_related_news,
    link_trade_news,
    unlink_trade_news,
    update_trade,
)

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


@router.get("/{trade_id}/news", response_model=list[TradeNewsRead])
def trade_news_items(trade_id: int, db: Session = Depends(get_db)):
    return get_trade_related_news(db, trade_id)


@router.post("/{trade_id}/news", response_model=TradeNewsRead, status_code=201)
def create_trade_news_item(trade_id: int, payload: TradeNewsLinkCreate, db: Session = Depends(get_db)):
    return link_trade_news(db, trade_id, payload)


@router.delete("/{trade_id}/news/{news_id}")
def delete_trade_news_item(trade_id: int, news_id: int, db: Session = Depends(get_db)):
    return unlink_trade_news(db, trade_id, news_id)


@router.get("/news/{news_id}", response_model=list[NewsTradeRead])
def news_trade_items(news_id: int, db: Session = Depends(get_db)):
    return get_news_related_trades(db, news_id)
