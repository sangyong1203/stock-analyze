from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Memo, News, Stock, Trade
from app.domains.memos import repository
from app.domains.memos.schemas import MEMO_TYPES, MemoCreate, MemoRead, MemoUpdate


def _normalize_memo_type(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in MEMO_TYPES:
        raise HTTPException(status_code=400, detail=f"memo_type must be one of: {', '.join(MEMO_TYPES)}")
    return normalized


def _validate_targets(db: Session, payload: MemoCreate) -> None:
    if payload.stock_id is not None and db.get(Stock, payload.stock_id) is None:
        raise HTTPException(status_code=404, detail="stock not found")
    if payload.trade_id is not None and db.get(Trade, payload.trade_id) is None:
        raise HTTPException(status_code=404, detail="trade not found")
    if payload.news_id is not None and db.get(News, payload.news_id) is None:
        raise HTTPException(status_code=404, detail="news not found")

    if payload.memo_type == "stock" and payload.stock_id is None:
        raise HTTPException(status_code=400, detail="stock memo requires stock_id")
    if payload.memo_type == "trade" and payload.trade_id is None:
        raise HTTPException(status_code=400, detail="trade memo requires trade_id")
    if payload.memo_type == "news" and payload.news_id is None:
        raise HTTPException(status_code=400, detail="news memo requires news_id")
    if payload.memo_type == "general" and any(value is not None for value in (payload.stock_id, payload.trade_id, payload.news_id)):
        raise HTTPException(status_code=400, detail="general memo cannot target stock, trade, or news")


def list_memos(
    db: Session,
    memo_type: str | None = None,
    stock_id: int | None = None,
    trade_id: int | None = None,
    news_id: int | None = None,
):
    normalized_memo_type = _normalize_memo_type(memo_type) if memo_type else None
    return [
        MemoRead.model_validate(row)
        for row in repository.list_memos(
            db,
            memo_type=normalized_memo_type,
            stock_id=stock_id,
            trade_id=trade_id,
            news_id=news_id,
        )
    ]


def get_memo_detail(db: Session, memo_id: int) -> MemoRead:
    row = repository.get_memo(db, memo_id)
    if row is None:
        raise HTTPException(status_code=404, detail="memo not found")
    return MemoRead.model_validate(row)


def create_memo(db: Session, payload: MemoCreate) -> MemoRead:
    memo_type = _normalize_memo_type(payload.memo_type)
    normalized_payload = payload.model_copy(update={"memo_type": memo_type})
    _validate_targets(db, normalized_payload)
    memo = Memo(**normalized_payload.model_dump())
    db.add(memo)
    db.commit()
    db.refresh(memo)
    return MemoRead.model_validate(memo)


def update_memo(db: Session, memo_id: int, payload: MemoUpdate) -> MemoRead:
    memo = repository.get_memo(db, memo_id)
    if memo is None:
        raise HTTPException(status_code=404, detail="memo not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(memo, key, value)
    db.commit()
    db.refresh(memo)
    return MemoRead.model_validate(memo)


def delete_memo(db: Session, memo_id: int) -> dict[str, int]:
    memo = repository.get_memo(db, memo_id)
    if memo is None:
        raise HTTPException(status_code=404, detail="memo not found")
    db.delete(memo)
    db.commit()
    return {"deleted_memo_id": memo_id}
