from datetime import date, datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import Stock, StockPrice, SystemLog
from app.db.session import SessionLocal


def get_stock_by_code(db: Session, code: str) -> Stock | None:
    return db.query(Stock).filter(Stock.code == code).first()


def get_or_create_stock(db: Session, code: str, name: str, market: str, market_cap, current_price, change_rate) -> tuple[Stock, bool]:
    stock = get_stock_by_code(db, code)
    if stock:
        return stock, False
    stock = Stock(
        code=code,
        name=name,
        market=market,
        market_cap=market_cap,
        current_price=current_price,
        change_rate=change_rate,
        aliases_json=[],
        is_active=True,
    )
    db.add(stock)
    db.flush()
    return stock, True


def get_price(db: Session, stock_id: int, price_date: date, timeframe: str) -> StockPrice | None:
    return (
        db.query(StockPrice)
        .filter(
            StockPrice.stock_id == stock_id,
            StockPrice.date == price_date,
            StockPrice.timeframe == timeframe,
        )
        .first()
    )


def get_latest_price_date(db: Session, stock_id: int, timeframe: str = "daily") -> date | None:
    return db.query(func.max(StockPrice.date)).filter(StockPrice.stock_id == stock_id, StockPrice.timeframe == timeframe).scalar()


def list_prices(
    db: Session,
    stock_id: int,
    timeframe: str = "daily",
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = 240,
) -> list[StockPrice]:
    query = db.query(StockPrice).filter(StockPrice.stock_id == stock_id, StockPrice.timeframe == timeframe)
    if date_from:
        query = query.filter(StockPrice.date >= date_from)
    if date_to:
        query = query.filter(StockPrice.date <= date_to)
    return query.order_by(StockPrice.date.desc()).limit(limit).all()


def get_latest_price(db: Session, stock_id: int, timeframe: str = "daily") -> StockPrice | None:
    return (
        db.query(StockPrice)
        .filter(StockPrice.stock_id == stock_id, StockPrice.timeframe == timeframe)
        .order_by(StockPrice.date.desc())
        .first()
    )


def list_market_latest_prices(db: Session, market: str, limit: int = 200) -> list[StockPrice]:
    latest_date = db.query(func.max(StockPrice.date)).filter(StockPrice.market == market).scalar()
    if latest_date is None:
        return []
    return (
        db.query(StockPrice)
        .filter(StockPrice.market == market, StockPrice.date == latest_date, StockPrice.timeframe == "daily")
        .order_by(StockPrice.market_cap.desc().nullslast(), StockPrice.id)
        .limit(limit)
        .all()
    )


def summary_counts(db: Session):
    total = db.query(func.count(StockPrice.id)).scalar() or 0
    latest_date = db.query(func.max(StockPrice.date)).scalar()
    kospi = db.query(func.count(StockPrice.id)).filter(StockPrice.market == "KOSPI").scalar() or 0
    kosdaq = db.query(func.count(StockPrice.id)).filter(StockPrice.market == "KOSDAQ").scalar() or 0
    latest_updated = 0
    if latest_date is not None:
        latest_updated = (
            db.query(func.count(Stock.id))
            .join(StockPrice, StockPrice.stock_id == Stock.id)
            .filter(StockPrice.date == latest_date)
            .scalar()
            or 0
        )
    return total, latest_date, kospi, kosdaq, latest_updated


def create_system_log(db: Session, level: str, message: str, context: dict | None = None) -> None:
    db.add(SystemLog(level=level, category="krx_price_collection", message=message, context_json=context, created_at=datetime.utcnow()))


def create_system_log_safely(level: str, message: str, context: dict | None = None) -> None:
    log_db = SessionLocal()
    try:
        log_db.add(
            SystemLog(
                level=level,
                category="krx_price_collection",
                message=message,
                context_json=context,
                created_at=datetime.utcnow(),
            )
        )
        log_db.commit()
    except Exception:  # noqa: BLE001 - logging must not break collection flow.
        log_db.rollback()
    finally:
        log_db.close()
