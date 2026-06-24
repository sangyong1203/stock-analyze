from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app.external.naver.parser import parse_market_news
from app.external.naver.types import NaverNewsItem


class NaverFinanceNewsClient:
    base_url = "https://finance.naver.com/news/news_list.naver"

    def fetch_market_news_page(self, page: int = 1, timeout: int = 10) -> str:
        query = urlencode({"page": page})
        request = Request(
            f"{self.base_url}?{query}",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
            charset = response.headers.get_content_charset() or "euc-kr"
            try:
                return raw.decode(charset, errors="replace")
            except LookupError:
                return raw.decode("euc-kr", errors="replace")

    def fetch_market_news(self, page: int = 1, timeout: int = 10) -> list[NaverNewsItem]:
        html = self.fetch_market_news_page(page=page, timeout=timeout)
        return parse_market_news(html)
