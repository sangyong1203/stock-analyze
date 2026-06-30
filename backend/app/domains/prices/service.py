from datetime import date, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Stock, StockPrice
from app.domains.prices import repository
from app.domains.prices.schemas import (
    KrxDailyCollectRequest,
    KrxDailyCollectResult,
    KrxRangeCollectRequest,
    KrxRangeCollectResult,
    KrxRangeDateResult,
    PriceSummary,
)
from app.external.krx import KrxClient
from app.external.krx.types import KrxDailyPrice

VALID_MARKETS = {"KOSPI", "KOSDAQ"}
UPSERT_CHUNK_SIZE = 500


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


def _get_or_create_stock_cached(db: Session, price: KrxDailyPrice, stock_cache: dict[str, Stock]) -> tuple[Stock, bool]:
    stock = stock_cache.get(price.code)
    if stock is not None:
        return stock, False
    stock, created_stock = repository.get_or_create_stock(
        db=db,
        code=price.code,
        name=price.name,
        market=price.market,
        market_cap=price.market_cap,
        current_price=price.close,
        change_rate=price.change_rate,
    )
    stock_cache[price.code] = stock
    return stock, created_stock


def _price_values(price: KrxDailyPrice) -> dict:
    return {
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


def _price_value_tuple(values: dict) -> tuple:
    return (
        values["market"],
        values["open"],
        values["high"],
        values["low"],
        values["close"],
        values["volume"],
        values["trade_value"],
        values["market_cap"],
        values["listed_shares"],
        values["change_price"],
        values["change_rate"],
        values["source"],
    )


def _should_apply_stock_latest(
    db: Session,
    stock_id: int,
    price_date: date,
    latest_date_cache: dict[int, date | None],
) -> bool:
    latest_price_date = latest_date_cache.get(stock_id)
    if stock_id not in latest_date_cache:
        latest_price_date = repository.get_latest_price_date(db, stock_id, "daily")
        latest_date_cache[stock_id] = latest_price_date
    if latest_price_date is None or price_date >= latest_price_date:
        latest_date_cache[stock_id] = price_date
        return True
    return False


def _collect_for_date(
    db: Session,
    client: KrxClient,
    bas_date: str,
    markets: list[str],
    dry_run: bool,
    stock_cache: dict[str, Stock] | None = None,
    latest_date_cache: dict[int, date | None] | None = None,
) -> KrxRangeDateResult:
    result = KrxRangeDateResult(bas_date=bas_date)
    fetched_prices: list[KrxDailyPrice] = []
    for market in markets:
        try:
            prices = client.fetch_daily_prices(market=market, bas_date=bas_date)
            result.fetched_count += len(prices)
            fetched_prices.extend(prices)
        except Exception as exc:  # noqa: BLE001 - collection errors must be returned and logged.
            result.error_count += 1
            message = f"{market}: {exc}"
            result.errors.append(message)
            repository.create_system_log_safely("error", message, {"market": market, "bas_date": bas_date})
    if dry_run:
        return result

    stock_cache = stock_cache if stock_cache is not None else {}
    latest_date_cache = latest_date_cache if latest_date_cache is not None else {}
    try:
        valid_pairs: list[tuple[KrxDailyPrice, Stock]] = []
        for price in fetched_prices:
            if not price.code or not price.name:
                result.error_count += 1
                result.errors.append(f"{price.market}: missing stock code or name")
                continue
            stock, created_stock = _get_or_create_stock_cached(db, price, stock_cache)
            result.stock_created_count += int(created_stock)
            valid_pairs.append((price, stock))

        stock_ids = [stock.id for _price, stock in valid_pairs if stock.id is not None]
        existing_price_values: dict[int, tuple] = {}
        if stock_ids:
            existing_rows = (
                db.query(
                    StockPrice.stock_id,
                    StockPrice.market,
                    StockPrice.open,
                    StockPrice.high,
                    StockPrice.low,
                    StockPrice.close,
                    StockPrice.volume,
                    StockPrice.trade_value,
                    StockPrice.market_cap,
                    StockPrice.listed_shares,
                    StockPrice.change_price,
                    StockPrice.change_rate,
                    StockPrice.source,
                )
                .filter(
                    StockPrice.date == valid_pairs[0][0].date,
                    StockPrice.timeframe == "daily",
                    StockPrice.stock_id.in_(stock_ids),
                )
                .all()
            )
            existing_price_values = {
                row.stock_id: (
                    row.market,
                    row.open,
                    row.high,
                    row.low,
                    row.close,
                    row.volume,
                    row.trade_value,
                    row.market_cap,
                    row.listed_shares,
                    row.change_price,
                    row.change_rate,
                    row.source,
                )
                for row in existing_rows
            }

        upsert_rows = []
        for price, stock in valid_pairs:
            values = _price_values(price)
            existing_values = existing_price_values.get(stock.id)
            upsert_row = {
                "stock_id": stock.id,
                "date": price.date,
                "timeframe": "daily",
                "created_at": datetime.utcnow(),
                **values,
            }
            if existing_values is not None:
                if existing_values != _price_value_tuple(values):
                    upsert_rows.append(upsert_row)
                result.updated_count += 1
            else:
                upsert_rows.append(upsert_row)
                result.inserted_count += 1
            if _should_apply_stock_latest(db, stock.id, price.date, latest_date_cache):
                _apply_stock_latest(stock, price)

        for start in range(0, len(upsert_rows), UPSERT_CHUNK_SIZE):
            statement = sqlite_insert(StockPrice).values(upsert_rows[start : start + UPSERT_CHUNK_SIZE])
            db.execute(
                statement.on_conflict_do_update(
                    index_elements=["stock_id", "date", "timeframe"],
                    set_={
                        "market": statement.excluded.market,
                        "open": statement.excluded.open,
                        "high": statement.excluded.high,
                        "low": statement.excluded.low,
                        "close": statement.excluded.close,
                        "volume": statement.excluded.volume,
                        "trade_value": statement.excluded.trade_value,
                        "market_cap": statement.excluded.market_cap,
                        "listed_shares": statement.excluded.listed_shares,
                        "change_price": statement.excluded.change_price,
                        "change_rate": statement.excluded.change_rate,
                        "source": statement.excluded.source,
                    },
                )
            )
    except Exception as exc:  # noqa: BLE001 - per-date DB failures should be returned, not crash the whole run.
        db.rollback()
        stock_cache.clear()
        latest_date_cache.clear()
        result.inserted_count = 0
        result.updated_count = 0
        result.stock_created_count = 0
        result.error_count += 1
        result.errors.append(f"db_write_failed: {exc}")
    return result


def collect_krx_daily_prices(db: Session, payload: KrxDailyCollectRequest) -> KrxDailyCollectResult:
    markets = _validate_markets(payload.markets)
    client = KrxClient(base_url=settings.krx_api_base_url, auth_key=settings.krx_auth_key)
    date_result = _collect_for_date(db, client, payload.bas_date, markets, payload.dry_run)
    result = KrxDailyCollectResult(
        bas_date=payload.bas_date,
        markets=markets,
        fetched_count=date_result.fetched_count,
        inserted_count=date_result.inserted_count,
        updated_count=date_result.updated_count,
        stock_created_count=date_result.stock_created_count,
        error_count=date_result.error_count,
        errors=date_result.errors,
    )

    if not payload.dry_run:
        try:
            db.commit()
        except Exception as exc:  # noqa: BLE001 - DB write failure should surface clearly.
            db.rollback()
            raise HTTPException(status_code=500, detail=f"failed to save KRX daily prices: {exc}") from exc
    return result


def _parse_bas_date(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y%m%d")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="date_from and date_to must be YYYYMMDD") from exc


def collect_krx_range_prices(db: Session, payload: KrxRangeCollectRequest) -> KrxRangeCollectResult:
    markets = _validate_markets(payload.markets)
    start = _parse_bas_date(payload.date_from)
    end = _parse_bas_date(payload.date_to)
    if start > end:
        raise HTTPException(status_code=400, detail="date_from must be earlier than or equal to date_to")

    requested_date_count = (end.date() - start.date()).days + 1
    if requested_date_count > 220:
        raise HTTPException(status_code=400, detail="date range must be 220 days or less")

    client = KrxClient(base_url=settings.krx_api_base_url, auth_key=settings.krx_auth_key)
    result = KrxRangeCollectResult(
        date_from=payload.date_from,
        date_to=payload.date_to,
        markets=markets,
        requested_date_count=requested_date_count,
    )

    current = start
    stock_cache: dict[str, Stock] = {}
    latest_date_cache: dict[int, date | None] = {}
    while current <= end:
        bas_date = current.strftime("%Y%m%d")
        date_result = _collect_for_date(db, client, bas_date, markets, payload.dry_run, stock_cache, latest_date_cache)
        if not payload.dry_run:
            try:
                db.commit()
            except Exception as exc:  # noqa: BLE001 - date-level failure should not discard prior committed dates.
                db.rollback()
                stock_cache.clear()
                latest_date_cache.clear()
                date_result.inserted_count = 0
                date_result.updated_count = 0
                date_result.stock_created_count = 0
                date_result.error_count += 1
                date_result.errors.append(f"commit_failed: {exc}")
        if payload.skip_empty and date_result.fetched_count == 0 and date_result.error_count == 0:
            date_result.skipped_empty = True
            result.skipped_empty_dates += 1
        result.fetched_count += date_result.fetched_count
        result.inserted_count += date_result.inserted_count
        result.updated_count += date_result.updated_count
        result.stock_created_count += date_result.stock_created_count
        result.error_count += date_result.error_count
        result.errors.extend(date_result.errors)
        result.dates.append(date_result)
        current += timedelta(days=1)

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
