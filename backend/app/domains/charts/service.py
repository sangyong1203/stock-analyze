from datetime import date

from sqlalchemy.orm import Session

from app.domains.charts import repository
from app.domains.charts.schemas import OhlcvPoint, OhlcvResponse


def get_chart_summary() -> dict:
    return {"timeframes": ["daily"], "indicators": []}


def get_stock_ohlcv(
    db: Session,
    stock_id: int,
    timeframe: str = "daily",
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = 240,
) -> OhlcvResponse:
    rows = list(reversed(repository.list_chart_prices(db, stock_id, timeframe, date_from, date_to, limit)))
    return OhlcvResponse(
        stock_id=stock_id,
        timeframe=timeframe,
        items=[
            OhlcvPoint(
                date=row.date,
                open=row.open,
                high=row.high,
                low=row.low,
                close=row.close,
                volume=row.volume,
                change_rate=row.change_rate,
            )
            for row in rows
        ],
    )
