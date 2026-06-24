from sqlalchemy.orm import Session

from app.domains.alerts.repository import list_price_alerts


def get_price_alerts(db: Session):
    return list_price_alerts(db)
