from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

from app.domains.alerts.schemas import PriceAlertSummary
from app.domains.holdings.schemas import HoldingSummary
from app.domains.news.schemas import AlertCandidateSummary
from app.domains.portfolio.schemas import PortfolioSummary


class DashboardHoldingItem(BaseModel):
    stock_id: int
    stock_code: str
    stock_name: str
    quantity: int
    current_price: Decimal | None = None
    market_value: Decimal | None = None
    unrealized_profit_loss: Decimal | None = None
    unrealized_profit_loss_rate: Decimal | None = None


class DashboardTradeItem(BaseModel):
    id: int
    stock_id: int
    stock_code: str
    stock_name: str
    fund_pool_name: str
    trade_type: str
    quantity: int
    price: Decimal
    trade_date: date
    memo: str | None = None


class DashboardNewsItem(BaseModel):
    id: int
    title: str
    source: str | None = None
    published_at: datetime | None = None
    importance_score: int
    gpt_summary_status: str | None = None
    is_alert_target: bool


class DashboardAlertHistoryItem(BaseModel):
    id: int
    alert_type: str
    status: str
    title: str
    stock_name: str | None = None
    news_title: str | None = None
    created_at: datetime
    sent_at: datetime | None = None


class DashboardMemoItem(BaseModel):
    id: int
    memo_type: str
    title: str | None = None
    content: str
    target_type: str
    target_label: str | None = None
    created_at: datetime


class DashboardTagItem(BaseModel):
    id: int
    name: str
    color: str | None = None
    tag_type: str
    usage_count: int


class DashboardMemoSummary(BaseModel):
    recent_memos: list[DashboardMemoItem]
    top_tags: list[DashboardTagItem]


class DashboardSummary(BaseModel):
    portfolio_summary: PortfolioSummary
    holding_summary: HoldingSummary
    top_holdings: list[DashboardHoldingItem]
    top_gainers: list[DashboardHoldingItem]
    top_losers: list[DashboardHoldingItem]
    recent_trades: list[DashboardTradeItem]
    recent_news: list[DashboardNewsItem]
    recent_alert_histories: list[DashboardAlertHistoryItem]
    price_alert_summary: PriceAlertSummary
    news_alert_summary: AlertCandidateSummary
    memo_summary: DashboardMemoSummary
