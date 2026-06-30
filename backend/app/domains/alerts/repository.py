from datetime import date, datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import AlertHistory, AlertSetting, PriceAlert, Stock, StockPrice


def list_price_alerts(db: Session, stock_id: int | None = None, enabled: bool | None = None):
    query = db.query(PriceAlert, Stock).join(Stock, Stock.id == PriceAlert.stock_id).order_by(PriceAlert.id.desc())
    if stock_id is not None:
        query = query.filter(PriceAlert.stock_id == stock_id)
    if enabled is not None:
        query = query.filter(PriceAlert.enabled.is_(enabled))
    return query.limit(200).all()


def get_price_alert(db: Session, alert_id: int):
    return (
        db.query(PriceAlert, Stock)
        .join(Stock, Stock.id == PriceAlert.stock_id)
        .filter(PriceAlert.id == alert_id)
        .first()
    )


def get_price_alert_model(db: Session, alert_id: int):
    return db.query(PriceAlert).filter(PriceAlert.id == alert_id).first()


def get_stock(db: Session, stock_id: int):
    return db.query(Stock).filter(Stock.id == stock_id).first()


def list_evaluation_targets(db: Session, alert_ids: list[int] | None = None):
    query = db.query(PriceAlert, Stock).join(Stock, Stock.id == PriceAlert.stock_id).order_by(PriceAlert.id.asc())
    if alert_ids:
        query = query.filter(PriceAlert.id.in_(alert_ids))
    return query.all()


def get_latest_price_row(db: Session, stock_id: int):
    return (
        db.query(StockPrice)
        .filter(StockPrice.stock_id == stock_id, StockPrice.timeframe == "daily")
        .order_by(StockPrice.date.desc())
        .first()
    )


def get_price_range_stats(db: Session, stock_id: int, latest_date: date, lookback_days: int):
    start_date = latest_date - timedelta(days=max(lookback_days - 1, 0))
    return (
        db.query(
            func.max(StockPrice.high),
            func.min(StockPrice.low),
            func.max(StockPrice.date),
        )
        .filter(
            StockPrice.stock_id == stock_id,
            StockPrice.timeframe == "daily",
            StockPrice.date >= start_date,
            StockPrice.date <= latest_date,
        )
        .first()
    )


def get_alert_setting(db: Session):
    return db.query(AlertSetting).order_by(AlertSetting.id.asc()).first()


def get_sent_history_today(db: Session, price_alert_id: int, stock_id: int, today_start: datetime):
    return (
        db.query(AlertHistory)
        .filter(
            AlertHistory.alert_type == "price",
            AlertHistory.price_alert_id == price_alert_id,
            AlertHistory.stock_id == stock_id,
            AlertHistory.status == "sent",
            AlertHistory.created_at >= today_start,
        )
        .first()
    )


def get_failed_history_today(db: Session, price_alert_id: int, stock_id: int, today_start: datetime):
    return (
        db.query(AlertHistory)
        .filter(
            AlertHistory.alert_type == "price",
            AlertHistory.price_alert_id == price_alert_id,
            AlertHistory.stock_id == stock_id,
            AlertHistory.status == "failed",
            AlertHistory.created_at >= today_start,
        )
        .first()
    )


def count_sent_alerts_since(db: Session, since: datetime):
    return (
        db.query(func.count(AlertHistory.id))
        .filter(
            AlertHistory.alert_type == "price",
            AlertHistory.status == "sent",
            AlertHistory.sent_at >= since,
        )
        .scalar()
        or 0
    )


def list_alert_histories(db: Session, status: str | None = None):
    query = db.query(AlertHistory).filter(AlertHistory.alert_type == "price").order_by(AlertHistory.id.desc())
    if status:
        query = query.filter(AlertHistory.status == status)
    return query.limit(200).all()


def summary_counts(db: Session):
    total = db.query(func.count(PriceAlert.id)).scalar() or 0
    enabled = db.query(func.count(PriceAlert.id)).filter(PriceAlert.enabled.is_(True)).scalar() or 0
    disabled = db.query(func.count(PriceAlert.id)).filter(PriceAlert.enabled.is_(False)).scalar() or 0
    triggered = db.query(func.count(PriceAlert.id)).filter(PriceAlert.triggered.is_(True)).scalar() or 0
    sent = db.query(func.count(AlertHistory.id)).filter(AlertHistory.alert_type == "price", AlertHistory.status == "sent").scalar() or 0
    failed = db.query(func.count(AlertHistory.id)).filter(AlertHistory.alert_type == "price", AlertHistory.status == "failed").scalar() or 0
    skipped = db.query(func.count(AlertHistory.id)).filter(AlertHistory.alert_type == "price", AlertHistory.status == "skipped").scalar() or 0
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    hour_start = datetime.utcnow() - timedelta(hours=1)
    today_sent = count_sent_alerts_since(db, today_start)
    hourly_sent = count_sent_alerts_since(db, hour_start)
    return total, enabled, disabled, triggered, sent, failed, skipped, today_sent, hourly_sent
