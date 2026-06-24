from sqlalchemy.orm import Session

from app.db.models import StockPrice


def list_chart_prices(db: Session, stock_id: int, timeframe: str):
    return db.query(StockPrice).filter(
        StockPrice.stock_id == stock_id,
        StockPrice.timeframe == timeframe,
    ).order_by(StockPrice.date).all()
