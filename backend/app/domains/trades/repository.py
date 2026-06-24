from sqlalchemy.orm import Session

from app.db.models import Trade


def list_trades(db: Session):
    return db.query(Trade).order_by(Trade.trade_date.desc()).limit(100).all()
