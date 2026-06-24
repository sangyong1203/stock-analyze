from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.responses import ok
from app.db.session import get_db
from app.domains.charts.service import get_chart_summary, get_stock_ohlcv
from app.domains.charts.schemas import OhlcvResponse

router = APIRouter()


@router.get("/summary")
def summary():
    return ok(get_chart_summary())


@router.get("/stocks/{stock_id}/ohlcv", response_model=OhlcvResponse)
def stock_ohlcv(
    stock_id: int,
    timeframe: str = "daily",
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = Query(default=240, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return get_stock_ohlcv(db, stock_id, timeframe, date_from, date_to, limit)
