import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.external.krx.parser import extract_rows, parse_daily_price
from app.external.krx.types import KrxDailyPrice


MARKET_ENDPOINTS = {
    "KOSPI": "/sto/stk_bydd_trd",
    "KOSDAQ": "/sto/ksq_bydd_trd",
}


class KrxClient:
    def __init__(self, base_url: str, auth_key: str = "", timeout: int = 20) -> None:
        self.base_url = base_url.rstrip("/")
        self.auth_key = auth_key
        self.timeout = timeout

    def fetch_daily_prices(self, market: str, bas_date: str) -> list[KrxDailyPrice]:
        endpoint = MARKET_ENDPOINTS.get(market.upper())
        if endpoint is None:
            raise ValueError("market must be KOSPI or KOSDAQ")

        payload = json.dumps({"basDd": bas_date}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.auth_key:
            headers["AUTH_KEY"] = self.auth_key

        request = Request(
            url=f"{self.base_url}{endpoint}",
            data=payload,
            headers=headers,
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                response_body = response.read().decode("utf-8")
                raw_payload = json.loads(response_body) if response_body else {}
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"KRX API HTTP {exc.code}: {body[:300]}") from exc
        except URLError as exc:
            raise RuntimeError(f"KRX API request failed: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError("KRX API returned invalid JSON") from exc

        return [parse_daily_price(row, market.upper()) for row in extract_rows(raw_payload)]
