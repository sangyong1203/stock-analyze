from sqlalchemy import exists, func, or_
from sqlalchemy.orm import Session

from app.db.models import (
    CollectionRule,
    Holding,
    IndexConstituent,
    PriceAlert,
    Stock,
    StockCollectionSetting,
)


def list_collection_rules(db: Session):
    return db.query(CollectionRule).order_by(CollectionRule.priority, CollectionRule.id).all()


def get_collection_rule(db: Session, rule_id: int):
    return db.get(CollectionRule, rule_id)


def list_active_rules(db: Session):
    return db.query(CollectionRule).filter(CollectionRule.enabled.is_(True)).order_by(CollectionRule.priority).all()


def get_stock_collection_setting(db: Session, stock_id: int):
    return db.query(StockCollectionSetting).filter(StockCollectionSetting.stock_id == stock_id).first()


def list_active_stocks(db: Session):
    return db.query(Stock).filter(Stock.is_active.is_(True)).order_by(Stock.code).all()


def list_index_constituents(db: Session, index_code: str | None = None, is_active: bool | None = True):
    query = db.query(IndexConstituent)
    if index_code:
        query = query.filter(IndexConstituent.index_code == index_code)
    if is_active is not None:
        query = query.filter(IndexConstituent.is_active.is_(is_active))
    return query.order_by(IndexConstituent.index_code, IndexConstituent.stock_code).all()


def get_stock_by_code(db: Session, code: str):
    return db.query(Stock).filter(Stock.code == code).first()


def get_active_index_codes_by_stock(db: Session) -> dict[int, set[str]]:
    rows = db.query(IndexConstituent.stock_id, IndexConstituent.index_code).filter(
        IndexConstituent.is_active.is_(True),
        IndexConstituent.stock_id.is_not(None),
    ).all()
    result: dict[int, set[str]] = {}
    for stock_id, index_code in rows:
        result.setdefault(stock_id, set()).add(index_code)
    return result


def get_holding_stock_ids(db: Session) -> set[int]:
    rows = db.query(Holding.stock_id).filter(Holding.is_closed.is_(False), Holding.quantity > 0).distinct().all()
    return {row[0] for row in rows}


def get_alert_stock_ids(db: Session) -> set[int]:
    rows = db.query(PriceAlert.stock_id).filter(PriceAlert.enabled.is_(True)).distinct().all()
    return {row[0] for row in rows}


def list_collection_stocks(
    db: Session,
    collect_enabled: bool | None = None,
    collect_news: bool | None = None,
    collect_alert_enabled: bool | None = None,
    priority: str | None = None,
    collect_reason: str | None = None,
    market: str | None = None,
    index_code: str | None = None,
    is_favorite: bool | None = None,
    keyword: str | None = None,
    page: int = 1,
    page_size: int = 50,
):
    holding_exists = exists().where(
        Holding.stock_id == Stock.id,
        Holding.is_closed.is_(False),
        Holding.quantity > 0,
    )
    query = db.query(Stock, StockCollectionSetting, holding_exists.label("is_holding_calculated")).outerjoin(
        StockCollectionSetting,
        StockCollectionSetting.stock_id == Stock.id,
    ).filter(Stock.is_active.is_(True))

    if index_code:
        query = query.join(IndexConstituent, IndexConstituent.stock_id == Stock.id).filter(
            IndexConstituent.index_code == index_code,
            IndexConstituent.is_active.is_(True),
        )
    if collect_enabled is not None:
        query = query.filter(StockCollectionSetting.collect_enabled.is_(collect_enabled))
    if collect_news is not None:
        query = query.filter(StockCollectionSetting.collect_news.is_(collect_news))
    if collect_alert_enabled is not None:
        query = query.filter(StockCollectionSetting.collect_alert_enabled.is_(collect_alert_enabled))
    if priority:
        query = query.filter(StockCollectionSetting.priority == priority)
    if collect_reason:
        query = query.filter(StockCollectionSetting.collect_reason == collect_reason)
    if market:
        query = query.filter(Stock.market == market)
    if is_favorite is not None:
        query = query.filter(Stock.is_favorite.is_(is_favorite))
    if keyword:
        like = f"%{keyword.strip()}%"
        query = query.filter(or_(Stock.code.like(like), Stock.name.like(like), Stock.sector.like(like)))

    total_count = query.count()
    rows = query.order_by(Stock.code).offset((page - 1) * page_size).limit(page_size).all()
    return rows, total_count


def collection_summary_counts(db: Session):
    total = db.query(func.count(Stock.id)).filter(Stock.is_active.is_(True)).scalar() or 0
    enabled = db.query(func.count(StockCollectionSetting.id)).filter(StockCollectionSetting.collect_enabled.is_(True)).scalar() or 0
    news = db.query(func.count(StockCollectionSetting.id)).filter(StockCollectionSetting.collect_news.is_(True)).scalar() or 0
    alert = db.query(func.count(StockCollectionSetting.id)).filter(StockCollectionSetting.collect_alert_enabled.is_(True)).scalar() or 0
    manual_include = db.query(func.count(StockCollectionSetting.id)).filter(StockCollectionSetting.manual_include.is_(True)).scalar() or 0
    manual_exclude = db.query(func.count(StockCollectionSetting.id)).filter(StockCollectionSetting.manual_exclude.is_(True)).scalar() or 0
    return total, enabled, news, alert, manual_include, manual_exclude
