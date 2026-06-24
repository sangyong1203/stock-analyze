from sqlalchemy.orm import Session

from app.domains.trades.repository import list_trades


def get_trade_list(db: Session):
    return list_trades(db)
