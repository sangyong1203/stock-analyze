from datetime import datetime, timedelta

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from app.db.models import AlertSetting, Holding, News, NewsCollectJob, NewsCollectJobItem, NewsStockLink, PriceAlert, Stock, StockCollectionSetting


def list_news(
    db: Session,
    keyword: str | None = None,
    stock_code: str | None = None,
    market_scope: str | None = None,
    event_type: str | None = None,
    filter_status: str | None = None,
    min_importance_score: int | None = None,
    is_alert_target: bool | None = None,
    is_gpt_summary_target: bool | None = None,
    gpt_summary_status: str | None = None,
    gpt_filter_result: str | None = None,
    published_from: datetime | None = None,
    published_to: datetime | None = None,
):
    query = db.query(News).options(joinedload(News.stock_links)).order_by(News.published_at.desc().nullslast(), News.id.desc())
    if stock_code:
        query = query.join(NewsStockLink, NewsStockLink.news_id == News.id).filter(NewsStockLink.stock_code == stock_code)
    if keyword:
        like = f"%{keyword.strip()}%"
        query = query.filter(or_(News.title.like(like), News.content_preview.like(like), News.original_summary.like(like)))
    if market_scope:
        query = query.filter(News.market_scope == market_scope)
    if event_type:
        query = query.filter(News.event_type == event_type)
    if filter_status:
        query = query.filter(News.filter_status == filter_status)
    if min_importance_score is not None:
        query = query.filter(News.importance_score >= min_importance_score)
    if is_alert_target is not None:
        query = query.filter(News.is_alert_target.is_(is_alert_target))
    if is_gpt_summary_target is not None:
        query = query.filter(News.is_gpt_summary_target.is_(is_gpt_summary_target))
    if gpt_summary_status:
        query = query.filter(News.gpt_summary_status == gpt_summary_status)
    if gpt_filter_result:
        query = query.filter(News.gpt_filter_result == gpt_filter_result)
    if published_from:
        query = query.filter(News.published_at >= published_from)
    if published_to:
        query = query.filter(News.published_at <= published_to)
    return query.limit(200).all()


def get_news(db: Session, news_id: int):
    return db.query(News).options(joinedload(News.stock_links)).filter(News.id == news_id).first()


def get_news_by_url_hash(db: Session, url_hash: str):
    return db.query(News).filter(News.url_hash == url_hash).first()


def get_recent_news_by_title_hash(db: Session, title_hash: str, window_hours: int = 24):
    threshold = datetime.utcnow() - timedelta(hours=window_hours)
    return db.query(News).filter(
        News.title_hash == title_hash,
        News.created_at >= threshold,
    ).order_by(News.created_at.desc()).first()


def list_collect_target_stocks(db: Session):
    return db.query(Stock).join(
        StockCollectionSetting,
        StockCollectionSetting.stock_id == Stock.id,
    ).filter(
        Stock.is_active.is_(True),
        StockCollectionSetting.collect_enabled.is_(True),
    ).all()


def summary_counts(db: Session):
    total = db.query(func.count(News.id)).scalar() or 0
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today = db.query(func.count(News.id)).filter(News.created_at >= today_start).scalar() or 0
    linked = db.query(func.count(func.distinct(NewsStockLink.news_id))).scalar() or 0
    gpt_target = db.query(func.count(News.id)).filter(News.is_gpt_summary_target.is_(True)).scalar() or 0
    alert_target = db.query(func.count(News.id)).filter(News.is_alert_target.is_(True)).scalar() or 0
    avg_score = db.query(func.avg(News.importance_score)).scalar() or 0
    return total, today, linked, gpt_target, alert_target, float(avg_score)


def list_collect_jobs(db: Session):
    return db.query(NewsCollectJob).options(joinedload(NewsCollectJob.items)).order_by(NewsCollectJob.id.desc()).limit(100).all()


def get_collect_job(db: Session, job_id: int):
    return db.query(NewsCollectJob).options(joinedload(NewsCollectJob.items)).filter(NewsCollectJob.id == job_id).first()


def list_summary_targets(db: Session, limit: int):
    return db.query(News).options(joinedload(News.stock_links)).filter(
        News.is_gpt_summary_target.is_(True),
        or_(News.gpt_summary_status.is_(None), News.gpt_summary_status.in_(["pending", "failed"])),
    ).order_by(News.importance_score.desc(), News.published_at.desc().nullslast(), News.id.desc()).limit(limit).all()


def list_filter_targets(db: Session, limit: int):
    return db.query(News).options(joinedload(News.stock_links)).filter(
        News.gpt_filter_result.is_(None),
        or_(News.gpt_summary_status == "done", News.content_preview.is_not(None), News.original_summary.is_not(None)),
    ).order_by(News.importance_score.desc(), News.published_at.desc().nullslast(), News.id.desc()).limit(limit).all()


def gpt_targets_counts(db: Session):
    summary_pending = db.query(func.count(News.id)).filter(
        News.is_gpt_summary_target.is_(True),
        or_(News.gpt_summary_status.is_(None), News.gpt_summary_status.in_(["pending", "failed"])),
    ).scalar() or 0
    summary_done = db.query(func.count(News.id)).filter(News.gpt_summary_status == "done").scalar() or 0
    summary_failed = db.query(func.count(News.id)).filter(News.gpt_summary_status == "failed").scalar() or 0
    filter_pending = db.query(func.count(News.id)).filter(
        News.gpt_filter_result.is_(None),
        or_(News.gpt_summary_status == "done", News.content_preview.is_not(None), News.original_summary.is_not(None)),
    ).scalar() or 0
    filter_done = db.query(func.count(News.id)).filter(News.gpt_filter_result.in_(["important", "price_impact", "unnecessary"])).scalar() or 0
    filter_failed = db.query(func.count(News.id)).filter(News.gpt_filter_result == "failed").scalar() or 0
    return summary_pending, summary_done, summary_failed, filter_pending, filter_done, filter_failed


def gpt_status_counts(db: Session):
    total = db.query(func.count(News.id)).scalar() or 0
    summary_target = db.query(func.count(News.id)).filter(News.is_gpt_summary_target.is_(True)).scalar() or 0
    summary_done = db.query(func.count(News.id)).filter(News.gpt_summary_status == "done").scalar() or 0
    filter_done = db.query(func.count(News.id)).filter(News.gpt_filter_result.in_(["important", "price_impact", "unnecessary"])).scalar() or 0
    important = db.query(func.count(News.id)).filter(News.gpt_filter_result == "important").scalar() or 0
    price_impact = db.query(func.count(News.id)).filter(News.gpt_filter_result == "price_impact").scalar() or 0
    unnecessary = db.query(func.count(News.id)).filter(News.gpt_filter_result == "unnecessary").scalar() or 0
    return total, summary_target, summary_done, filter_done, important, price_impact, unnecessary


def list_review_news(
    db: Session,
    gpt_summary_status: str | None = None,
    gpt_filter_result: str | None = None,
    min_importance_score: int | None = None,
    stock_code: str | None = None,
    keyword: str | None = None,
    published_from: datetime | None = None,
    published_to: datetime | None = None,
):
    return list_news(
        db=db,
        keyword=keyword,
        stock_code=stock_code,
        min_importance_score=min_importance_score,
        gpt_summary_status=gpt_summary_status,
        gpt_filter_result=gpt_filter_result,
        published_from=published_from,
        published_to=published_to,
    )


def list_alert_candidate_news(
    db: Session,
    stock_code: str | None = None,
    gpt_filter_result: str | None = None,
    min_importance_score: int | None = None,
    published_from: datetime | None = None,
    published_to: datetime | None = None,
    only_alert_targets: bool = True,
    limit: int | None = 200,
):
    query = db.query(News).options(joinedload(News.stock_links)).order_by(News.published_at.desc().nullslast(), News.id.desc())
    if only_alert_targets:
        query = query.filter(News.is_alert_target.is_(True))
    if stock_code:
        query = query.join(NewsStockLink, NewsStockLink.news_id == News.id).filter(NewsStockLink.stock_code == stock_code)
    if gpt_filter_result:
        query = query.filter(News.gpt_filter_result == gpt_filter_result)
    if min_importance_score is not None:
        query = query.filter(News.importance_score >= min_importance_score)
    if published_from:
        query = query.filter(News.published_at >= published_from)
    if published_to:
        query = query.filter(News.published_at <= published_to)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


def get_alert_setting(db: Session):
    return db.query(AlertSetting).order_by(AlertSetting.id).first()


def get_attention_stock_ids(db: Session) -> set[int]:
    favorite_ids = {row[0] for row in db.query(Stock.id).filter(Stock.is_favorite.is_(True)).all()}
    holding_ids = {
        row[0]
        for row in db.query(Holding.stock_id).filter(Holding.is_closed.is_(False), Holding.quantity > 0).distinct().all()
    }
    price_alert_ids = {row[0] for row in db.query(PriceAlert.stock_id).filter(PriceAlert.enabled.is_(True)).distinct().all()}
    return favorite_ids | holding_ids | price_alert_ids


def alert_summary_counts(db: Session):
    alert_target = db.query(func.count(News.id)).filter(News.is_alert_target.is_(True)).scalar() or 0
    important = db.query(func.count(News.id)).filter(News.is_alert_target.is_(True), News.gpt_filter_result == "important").scalar() or 0
    price_impact = db.query(func.count(News.id)).filter(News.is_alert_target.is_(True), News.gpt_filter_result == "price_impact").scalar() or 0
    high_importance = db.query(func.count(News.id)).filter(News.is_alert_target.is_(True), News.importance_score >= 7).scalar() or 0
    return alert_target, important, price_impact, high_importance
