from sqlalchemy.orm import Session

from app.db.models import StockPrice


def list_prices(db: Session, stock_id: int):
    return db.query(StockPrice).filter(StockPrice.stock_id == stock_id).order_by(StockPrice.date.desc()).limit(200).all()
