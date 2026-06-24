from sqlalchemy.orm import Session

from app.db.models import Memo, Tag


def list_memos(db: Session):
    return db.query(Memo).order_by(Memo.created_at.desc()).limit(100).all()


def list_tags(db: Session):
    return db.query(Tag).order_by(Tag.name).all()
