class NaverFinanceClient:
    def fetch_market_news(self) -> list[dict]:
        raise NotImplementedError("네이버 금융 수집 정책 확정 후 구현")

    def fetch_price_snapshot(self, stock_code: str) -> dict:
        raise NotImplementedError("네이버 현재가 스냅샷 파서 구현 예정")
