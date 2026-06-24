from sqlalchemy.orm import Session

from app.domains.memos.repository import list_memos, list_tags


def get_memos(db: Session):
    return list_memos(db)


def get_tags(db: Session):
    return list_tags(db)
