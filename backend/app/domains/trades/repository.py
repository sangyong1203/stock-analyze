from sqlalchemy.orm import Session

from app.db.models import FundPool, FundTransaction, News, Stock, Trade, TradeNewsLink


def list_trades(db: Session):
    return (
        db.query(Trade, FundPool.name, Stock.code, Stock.name)
        .join(FundPool, FundPool.id == Trade.fund_pool_id)
        .join(Stock, Stock.id == Trade.stock_id)
        .order_by(Trade.trade_date.desc(), Trade.id.desc())
        .limit(300)
        .all()
    )


def get_trade_detail_row(db: Session, trade_id: int):
    return (
        db.query(Trade, FundPool.name, Stock.code, Stock.name)
        .join(FundPool, FundPool.id == Trade.fund_pool_id)
        .join(Stock, Stock.id == Trade.stock_id)
        .filter(Trade.id == trade_id)
        .first()
    )


def get_trade(db: Session, trade_id: int) -> Trade | None:
    return db.get(Trade, trade_id)


def get_trade_fund_transaction(db: Session, trade_id: int) -> FundTransaction | None:
    return db.query(FundTransaction).filter(FundTransaction.related_trade_id == trade_id).first()


def list_trade_news_links(db: Session, trade_id: int):
    return (
        db.query(TradeNewsLink, News.title, News.source, News.published_at)
        .join(News, News.id == TradeNewsLink.news_id)
        .filter(TradeNewsLink.trade_id == trade_id)
        .order_by(TradeNewsLink.id.desc())
        .all()
    )


def get_trade_news_link(db: Session, trade_id: int, news_id: int) -> TradeNewsLink | None:
    return (
        db.query(TradeNewsLink)
        .filter(TradeNewsLink.trade_id == trade_id, TradeNewsLink.news_id == news_id)
        .first()
    )


def list_news_trade_links(db: Session, news_id: int):
    return (
        db.query(
            TradeNewsLink,
            FundPool.name,
            Stock.code,
            Stock.name,
            Trade.fund_pool_id,
            Trade.stock_id,
            Trade.trade_type,
            Trade.trade_date,
            Trade.quantity,
            Trade.price,
        )
        .join(Trade, Trade.id == TradeNewsLink.trade_id)
        .join(FundPool, FundPool.id == Trade.fund_pool_id)
        .join(Stock, Stock.id == Trade.stock_id)
        .filter(TradeNewsLink.news_id == news_id)
        .order_by(Trade.trade_date.desc(), Trade.id.desc())
        .all()
    )
