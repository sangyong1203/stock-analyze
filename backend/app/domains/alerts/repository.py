from sqlalchemy.orm import Session

from app.db.models import PriceAlert


def list_price_alerts(db: Session):
    return db.query(PriceAlert).order_by(PriceAlert.id.desc()).limit(100).all()
