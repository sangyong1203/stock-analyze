from dataclasses import dataclass
from datetime import datetime


@dataclass
class NaverNewsItem:
    title: str
    url: str
    source: str | None = None
    published_at: datetime | None = None
    summary: str | None = None
