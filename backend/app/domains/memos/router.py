from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domains.memos.schemas import MemoCreate, MemoRead, MemoUpdate
from app.domains.memos.service import create_memo, delete_memo, get_memo_detail, list_memos, update_memo

router = APIRouter()


@router.get("", response_model=list[MemoRead])
def list_items(
    memo_type: str | None = None,
    stock_id: int | None = None,
    trade_id: int | None = None,
    news_id: int | None = None,
    db: Session = Depends(get_db),
):
    return list_memos(db, memo_type=memo_type, stock_id=stock_id, trade_id=trade_id, news_id=news_id)


@router.post("", response_model=MemoRead, status_code=201)
def create_item(payload: MemoCreate, db: Session = Depends(get_db)):
    return create_memo(db, payload)


@router.get("/{memo_id}", response_model=MemoRead)
def detail_item(memo_id: int, db: Session = Depends(get_db)):
    return get_memo_detail(db, memo_id)


@router.patch("/{memo_id}", response_model=MemoRead)
def update_item(memo_id: int, payload: MemoUpdate, db: Session = Depends(get_db)):
    return update_memo(db, memo_id, payload)


@router.delete("/{memo_id}", status_code=204)
def delete_item(memo_id: int, db: Session = Depends(get_db)):
    delete_memo(db, memo_id)
    return Response(status_code=204)
