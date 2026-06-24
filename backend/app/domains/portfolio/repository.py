from sqlalchemy.orm import Session

from app.db.models import FundPool


def list_fund_pools(db: Session):
    return db.query(FundPool).order_by(FundPool.id).all()
