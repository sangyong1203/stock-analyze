from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domains.prices import service
from app.domains.prices.schemas import KrxDailyCollectRequest, KrxDailyCollectResult, PriceSummary, StockPriceRead

router = APIRouter()


@router.post("/collect/krx/daily", response_model=KrxDailyCollectResult)
def collect_krx_daily(payload: KrxDailyCollectRequest, db: Session = Depends(get_db)):
    return service.collect_krx_daily_prices(db, payload)


@router.get("/summary", response_model=PriceSummary)
def summary(db: Session = Depends(get_db)):
    return service.get_price_summary(db)


@router.get("/stocks/{stock_id}", response_model=list[StockPriceRead])
def stock_prices(
    stock_id: int,
    timeframe: str = "daily",
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = Query(default=240, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return service.get_stock_prices(db, stock_id, timeframe, date_from, date_to, limit)


@router.get("/stocks/{stock_id}/latest", response_model=StockPriceRead)
def latest_stock_price(stock_id: int, db: Session = Depends(get_db)):
    return service.get_latest_stock_price(db, stock_id)


@router.get("/markets/{market}/latest", response_model=list[StockPriceRead])
def latest_market_prices(market: str, limit: int = Query(default=200, ge=1, le=1000), db: Session = Depends(get_db)):
    return service.get_market_latest_prices(db, market, limit)
