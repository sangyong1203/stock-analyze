from datetime import datetime
from html import unescape
import re
from urllib.parse import urljoin

from app.external.naver.types import NaverNewsItem

ARTICLE_PATTERN = re.compile(
    r'<dd\s+class="articleSubject">\s*'
    r'<a\s+href="(?P<href>[^"]+)"(?:\s+title="(?P<title>[^"]*)")?[^>]*>(?P<link_text>.*?)</a>\s*'
    r"</dd>\s*"
    r'<dd\s+class="articleSummary">\s*(?P<summary_block>.*?)</dd>',
    re.IGNORECASE | re.DOTALL,
)
TAG_PATTERN = re.compile(r"<[^>]+>")
SPACE_PATTERN = re.compile(r"\s+")


def _clean_text(value: str | None) -> str:
    if not value:
        return ""
    without_tags = TAG_PATTERN.sub(" ", value)
    return SPACE_PATTERN.sub(" ", unescape(without_tags)).strip()


def _extract_tag_text(block: str, class_name: str) -> str | None:
    match = re.search(
        rf'<span\s+class="{re.escape(class_name)}">\s*(?P<value>.*?)\s*</span>',
        block,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None
    return _clean_text(match.group("value"))


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M", "%Y.%m.%d %H:%M"):
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            continue
    return None


def _summary_without_meta(block: str) -> str | None:
    cleaned = re.sub(r'<span\s+class="press">.*?</span>', " ", block, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r'<span\s+class="bar">.*?</span>', " ", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r'<span\s+class="wdate">.*?</span>', " ", cleaned, flags=re.IGNORECASE | re.DOTALL)
    summary = _clean_text(cleaned)
    return summary or None


def parse_market_news(html: str) -> list[NaverNewsItem]:
    items: list[NaverNewsItem] = []
    seen_urls: set[str] = set()

    for match in ARTICLE_PATTERN.finditer(html):
        href = match.group("href").replace("&amp;", "&")
        if "news_read.naver" not in href:
            continue

        url = urljoin("https://finance.naver.com", href)
        if url in seen_urls:
            continue

        title = _clean_text(match.group("title")) or _clean_text(match.group("link_text"))
        if not title:
            continue

        summary_block = match.group("summary_block")
        source = _extract_tag_text(summary_block, "press") or "naver_finance"
        published_at = _parse_datetime(_extract_tag_text(summary_block, "wdate"))
        summary = _summary_without_meta(summary_block)

        items.append(
            NaverNewsItem(
                title=title,
                url=url,
                source=source,
                published_at=published_at,
                summary=summary,
            )
        )
        seen_urls.add(url)

    return items
