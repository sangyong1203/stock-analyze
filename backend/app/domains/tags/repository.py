from sqlalchemy.orm import Session

from app.db.models import Memo, News, Stock, Tag, TagLink, Trade


def list_tags(db: Session, tag_type: str | None = None):
    query = db.query(Tag).order_by(Tag.name.asc(), Tag.id.asc())
    if tag_type:
        query = query.filter(Tag.tag_type == tag_type)
    return query.all()


def get_tag(db: Session, tag_id: int) -> Tag | None:
    return db.get(Tag, tag_id)


def get_tag_by_name_type(db: Session, name: str, tag_type: str) -> Tag | None:
    return db.query(Tag).filter(Tag.name == name, Tag.tag_type == tag_type).first()


def list_tag_links(db: Session, target_type: str | None = None, target_id: int | None = None):
    query = db.query(TagLink, Tag.name, Tag.color, Tag.tag_type).join(Tag, Tag.id == TagLink.tag_id).order_by(TagLink.id.desc())
    if target_type:
        query = query.filter(TagLink.target_type == target_type)
    if target_id is not None:
        query = query.filter(TagLink.target_id == target_id)
    return query.limit(300).all()


def get_tag_link(db: Session, tag_id: int, target_type: str, target_id: int) -> TagLink | None:
    return (
        db.query(TagLink)
        .filter(TagLink.tag_id == tag_id, TagLink.target_type == target_type, TagLink.target_id == target_id)
        .first()
    )


def list_links_by_tag(db: Session, tag_id: int):
    return db.query(TagLink).filter(TagLink.tag_id == tag_id).all()


def get_stock(db: Session, stock_id: int):
    return db.get(Stock, stock_id)


def get_trade(db: Session, trade_id: int):
    return db.get(Trade, trade_id)


def get_news(db: Session, news_id: int):
    return db.get(News, news_id)


def get_memo(db: Session, memo_id: int):
    return db.get(Memo, memo_id)
