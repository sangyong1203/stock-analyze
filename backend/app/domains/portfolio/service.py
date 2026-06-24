from sqlalchemy.orm import Session

from app.domains.portfolio.repository import list_fund_pools


def get_fund_pools(db: Session):
    return list_fund_pools(db)
