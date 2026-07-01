from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import AlertHistory, Holding, Memo, News, Stock, Tag, TagLink, Trade, FundPool


def list_top_holdings(db: Session, limit: int):
    return (
        db.query(Holding, Stock)
        .join(Stock, Stock.id == Holding.stock_id)
        .filter(Holding.is_closed.is_(False), Holding.quantity > 0)
        .order_by(func.coalesce(Holding.market_value, 0).desc(), Holding.id.asc())
        .limit(limit)
        .all()
    )


def list_top_gainers(db: Session, limit: int):
    return (
        db.query(Holding, Stock)
        .join(Stock, Stock.id == Holding.stock_id)
        .filter(Holding.is_closed.is_(False), Holding.quantity > 0)
        .order_by(func.coalesce(Holding.unrealized_profit_loss_rate, -999999).desc(), Holding.id.asc())
        .limit(limit)
        .all()
    )


def list_top_losers(db: Session, limit: int):
    return (
        db.query(Holding, Stock)
        .join(Stock, Stock.id == Holding.stock_id)
        .filter(Holding.is_closed.is_(False), Holding.quantity > 0)
        .order_by(func.coalesce(Holding.unrealized_profit_loss_rate, 999999).asc(), Holding.id.asc())
        .limit(limit)
        .all()
    )


def list_recent_trades(db: Session, limit: int):
    return (
        db.query(Trade, Stock, FundPool)
        .join(Stock, Stock.id == Trade.stock_id)
        .join(FundPool, FundPool.id == Trade.fund_pool_id)
        .order_by(Trade.trade_date.desc(), Trade.id.desc())
        .limit(limit)
        .all()
    )


def list_recent_news(db: Session, limit: int):
    return db.query(News).order_by(News.published_at.desc(), News.id.desc()).limit(limit).all()


def list_recent_alert_histories(db: Session, limit: int):
    return (
        db.query(AlertHistory, Stock.name, News.title)
        .outerjoin(Stock, Stock.id == AlertHistory.stock_id)
        .outerjoin(News, News.id == AlertHistory.news_id)
        .order_by(AlertHistory.created_at.desc(), AlertHistory.id.desc())
        .limit(limit)
        .all()
    )


def list_recent_memos(db: Session, limit: int):
    return (
        db.query(Memo, Stock.name, Trade.id, News.title)
        .outerjoin(Stock, Stock.id == Memo.stock_id)
        .outerjoin(Trade, Trade.id == Memo.trade_id)
        .outerjoin(News, News.id == Memo.news_id)
        .order_by(Memo.created_at.desc(), Memo.id.desc())
        .limit(limit)
        .all()
    )


def list_top_tags(db: Session, limit: int):
    return (
        db.query(Tag, func.count(TagLink.id))
        .outerjoin(TagLink, TagLink.tag_id == Tag.id)
        .group_by(Tag.id)
        .order_by(func.count(TagLink.id).desc(), Tag.name.asc())
        .limit(limit)
        .all()
    )

