from datetime import date

from sqlalchemy.orm import Session

from app.domains.charts.indicators import calculate_indicators
from app.domains.charts import repository
from app.domains.charts.schemas import OhlcvPoint, OhlcvResponse


def get_chart_summary() -> dict:
    return {"timeframes": ["daily"], "indicators": ["MA20", "MA60", "MA120", "RSI14", "MACD"]}


def get_stock_ohlcv(
    db: Session,
    stock_id: int,
    timeframe: str = "daily",
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = 240,
) -> OhlcvResponse:
    rows = list(reversed(repository.list_chart_prices(db, stock_id, timeframe, date_from, date_to, limit)))
    closes = [row.close for row in rows]
    indicators = calculate_indicators(closes)
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
                ma20=indicators["ma20"][index],
                ma60=indicators["ma60"][index],
                ma120=indicators["ma120"][index],
                rsi14=indicators["rsi14"][index],
                macd=indicators["macd"][index],
                macd_signal=indicators["macd_signal"][index],
                macd_histogram=indicators["macd_histogram"][index],
            )
            for index, row in enumerate(rows)
        ],
    )
