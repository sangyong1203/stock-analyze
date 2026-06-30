from sqlalchemy.orm import Session

from app.db.models import Memo


def list_memos(
    db: Session,
    memo_type: str | None = None,
    stock_id: int | None = None,
    trade_id: int | None = None,
    news_id: int | None = None,
):
    query = db.query(Memo).order_by(Memo.created_at.desc(), Memo.id.desc())
    if memo_type:
        query = query.filter(Memo.memo_type == memo_type)
    if stock_id is not None:
        query = query.filter(Memo.stock_id == stock_id)
    if trade_id is not None:
        query = query.filter(Memo.trade_id == trade_id)
    if news_id is not None:
        query = query.filter(Memo.news_id == news_id)
    return query.limit(200).all()


def get_memo(db: Session, memo_id: int) -> Memo | None:
    return db.get(Memo, memo_id)
