from datetime import date

from sqlalchemy.orm import Session

from app.db.models import StockPrice


def list_chart_prices(
    db: Session,
    stock_id: int,
    timeframe: str = "daily",
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = 240,
):
    query = db.query(StockPrice).filter(StockPrice.stock_id == stock_id, StockPrice.timeframe == timeframe)
    if date_from:
        query = query.filter(StockPrice.date >= date_from)
    if date_to:
        query = query.filter(StockPrice.date <= date_to)
    return query.order_by(StockPrice.date.desc()).limit(limit).all()
