from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import StockPrice
from app.domains.prices import repository
from app.domains.prices.schemas import KrxDailyCollectRequest, KrxDailyCollectResult, PriceSummary
from app.external.krx import KrxClient
from app.external.krx.types import KrxDailyPrice

VALID_MARKETS = {"KOSPI", "KOSDAQ"}


def _validate_markets(markets: list[str]) -> list[str]:
    normalized = [market.upper() for market in markets]
    invalid = [market for market in normalized if market not in VALID_MARKETS]
    if invalid:
        raise HTTPException(status_code=400, detail="markets must be KOSPI or KOSDAQ")
    return list(dict.fromkeys(normalized))


def _apply_stock_latest(stock, price: KrxDailyPrice) -> None:
    stock.name = price.name or stock.name
    stock.market = price.market or stock.market
    stock.current_price = price.close
    stock.change_rate = price.change_rate
    stock.market_cap = price.market_cap
    stock.updated_at = datetime.utcnow()


def _upsert_price(db: Session, price: KrxDailyPrice) -> tuple[bool, bool, bool]:
    stock, created_stock = repository.get_or_create_stock(
        db=db,
        code=price.code,
        name=price.name,
        market=price.market,
        market_cap=price.market_cap,
        current_price=price.close,
        change_rate=price.change_rate,
    )
    existing = repository.get_price(db, stock.id, price.date, "daily")
    values = {
        "market": price.market,
        "open": price.open,
        "high": price.high,
        "low": price.low,
        "close": price.close,
        "volume": price.volume,
        "trade_value": price.trade_value,
        "market_cap": price.market_cap,
        "listed_shares": price.listed_shares,
        "change_price": price.change_price,
        "change_rate": price.change_rate,
        "source": "krx",
    }
    if existing:
        for key, value in values.items():
            setattr(existing, key, value)
        inserted = False
        updated = True
    else:
        db.add(StockPrice(stock_id=stock.id, date=price.date, timeframe="daily", **values))
        inserted = True
        updated = False
    _apply_stock_latest(stock, price)
    return inserted, updated, created_stock


def collect_krx_daily_prices(db: Session, payload: KrxDailyCollectRequest) -> KrxDailyCollectResult:
    markets = _validate_markets(payload.markets)
    client = KrxClient(base_url=settings.krx_api_base_url, auth_key=settings.krx_auth_key)
    result = KrxDailyCollectResult(bas_date=payload.bas_date, markets=markets)

    for market in markets:
        try:
            prices = client.fetch_daily_prices(market=market, bas_date=payload.bas_date)
            result.fetched_count += len(prices)
            if payload.dry_run:
                continue
            for price in prices:
                if not price.code or not price.name:
                    result.error_count += 1
                    result.errors.append(f"{market}: missing stock code or name")
                    continue
                inserted, updated, created_stock = _upsert_price(db, price)
                result.inserted_count += int(inserted)
                result.updated_count += int(updated)
                result.stock_created_count += int(created_stock)
        except Exception as exc:  # noqa: BLE001 - collection errors must be returned and logged.
            result.error_count += 1
            message = f"{market}: {exc}"
            result.errors.append(message)
            repository.create_system_log(db, "error", message, {"market": market, "bas_date": payload.bas_date})

    db.commit()
    return result


def get_price_summary(db: Session) -> PriceSummary:
    total, latest_date, kospi, kosdaq, latest_updated = repository.summary_counts(db)
    return PriceSummary(
        total_price_rows=total,
        latest_price_date=latest_date,
        kospi_price_count=kospi,
        kosdaq_price_count=kosdaq,
        latest_updated_stocks_count=latest_updated,
    )


def get_stock_prices(db: Session, stock_id: int, timeframe: str, date_from, date_to, limit: int):
    return list(reversed(repository.list_prices(db, stock_id, timeframe, date_from, date_to, limit)))


def get_latest_stock_price(db: Session, stock_id: int):
    price = repository.get_latest_price(db, stock_id)
    if price is None:
        raise HTTPException(status_code=404, detail="price not found")
    return price


def get_market_latest_prices(db: Session, market: str, limit: int):
    normalized = _validate_markets([market])[0]
    return repository.list_market_latest_prices(db, normalized, limit)
