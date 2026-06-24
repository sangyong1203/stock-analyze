from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from app.external.krx.types import KrxDailyPrice


def normalize_stock_code(value: Any) -> str:
    text = str(value or "").strip()
    return text.zfill(6) if text.isdigit() else text


def parse_decimal(value: Any) -> Decimal | None:
    if value is None:
        return None
    text = str(value).replace(",", "").replace("%", "").strip()
    if text in {"", "-", "N/A"}:
        return None
    try:
        return Decimal(text)
    except InvalidOperation:
        return None


def parse_int(value: Any) -> int | None:
    decimal_value = parse_decimal(value)
    return int(decimal_value) if decimal_value is not None else None


def parse_date(value: Any):
    text = str(value or "").replace("-", "").strip()
    return datetime.strptime(text, "%Y%m%d").date()


def parse_daily_price(row: dict[str, Any], default_market: str) -> KrxDailyPrice:
    return KrxDailyPrice(
        date=parse_date(row.get("BAS_DD")),
        code=normalize_stock_code(row.get("ISU_CD")),
        name=str(row.get("ISU_NM") or "").strip(),
        market=str(row.get("MKT_NM") or default_market).strip() or default_market,
        open=parse_decimal(row.get("TDD_OPNPRC")),
        high=parse_decimal(row.get("TDD_HGPRC")),
        low=parse_decimal(row.get("TDD_LWPRC")),
        close=parse_decimal(row.get("TDD_CLSPRC")),
        change_price=parse_decimal(row.get("CMPPREVDD_PRC")),
        change_rate=parse_decimal(row.get("FLUC_RT")),
        volume=parse_int(row.get("ACC_TRDVOL")),
        trade_value=parse_decimal(row.get("ACC_TRDVAL")),
        market_cap=parse_decimal(row.get("MKTCAP")),
        listed_shares=parse_int(row.get("LIST_SHRS")),
    )


def extract_rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("OutBlock_1", "output", "data", "list"):
        rows = payload.get(key)
        if isinstance(rows, list):
            return [item for item in rows if isinstance(item, dict)]
    return []
