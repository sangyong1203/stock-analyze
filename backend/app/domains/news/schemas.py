from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MarketNewsCollectRequest(BaseModel):
    pages: int = Field(default=1, ge=1, le=10)
    max_items: int = Field(default=50, ge=1, le=200)


class NewsStockLinkRead(BaseModel):
    id: int
    news_id: int
    stock_id: int | None = None
    stock_code: str | None = None
    stock_name: str | None = None
    relation_type: str
    relation_score: int | None = None
    source_stock_code: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NewsRead(BaseModel):
    id: int
    title: str
    url: str
    source: str | None = None
    published_at: datetime | None = None
    original_summary: str | None = None
    content_preview: str | None = None
    normalized_title: str | None = None
    source_type: str
    market_scope: str | None = None
    event_type: str | None = None
    duplicate_count: int
    source_count: int
    sources_json: list | None = None
    first_published_at: datetime | None = None
    last_published_at: datetime | None = None
    filter_status: str | None = None
    filter_reason: str | None = None
    matched_keywords_json: list | None = None
    importance_score: int
    gpt_summary: str | None = None
    gpt_summary_model: str | None = None
    gpt_summary_status: str | None = None
    gpt_summary_at: datetime | None = None
    gpt_filter_result: str | None = None
    gpt_filter_reason: str | None = None
    gpt_filter_model: str | None = None
    gpt_filter_at: datetime | None = None
    is_gpt_summary_target: bool
    is_alert_target: bool
    collected_at: datetime | None = None
    stock_links: list[NewsStockLinkRead] = []

    model_config = ConfigDict(from_attributes=True)


class NewsCollectJobItemRead(BaseModel):
    id: int
    job_id: int
    item_type: str
    target: str | None = None
    status: str
    fetched_count: int
    new_count: int
    duplicate_count: int
    excluded_count: int
    error_message: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NewsCollectJobRead(BaseModel):
    id: int
    job_type: str
    source_type: str
    trigger_type: str
    status: str
    started_at: datetime | None = None
    finished_at: datetime | None = None
    target_url: str | None = None
    total_fetched_count: int
    new_count: int
    duplicate_count: int
    excluded_count: int
    gpt_target_count: int
    alert_target_count: int
    error_message: str | None = None
    created_at: datetime
    items: list[NewsCollectJobItemRead] = []

    model_config = ConfigDict(from_attributes=True)


class NewsSummary(BaseModel):
    total_news_count: int
    today_news_count: int
    linked_stock_news_count: int
    gpt_summary_target_count: int
    alert_target_count: int
    avg_importance_score: float


class GptRunRequest(BaseModel):
    limit: int = Field(default=5, ge=1, le=100)
    dry_run: bool = False


class GptRunItem(BaseModel):
    id: int
    title: str
    status: str
    result: str | None = None
    reason: str | None = None


class GptRunResult(BaseModel):
    dry_run: bool
    processed_count: int
    target_count: int
    model: str | None = None
    items: list[GptRunItem]


class GptTargetsSummary(BaseModel):
    summary_pending_count: int
    summary_done_count: int
    summary_failed_count: int
    filter_pending_count: int
    filter_done_count: int
    filter_failed_count: int


class GptStatusSummary(BaseModel):
    total_news_count: int
    gpt_summary_target_count: int
    gpt_summary_done_count: int
    gpt_filter_done_count: int
    important_count: int
    price_impact_count: int
    unnecessary_count: int


class NewsReviewItem(BaseModel):
    news_id: int
    title: str
    source: str | None = None
    published_at: datetime | None = None
    related_stocks: list[str]
    importance_score: int
    duplicate_count: int
    source_count: int
    gpt_summary: str | None = None
    gpt_filter_result: str | None = None
    gpt_filter_reason: str | None = None
    is_alert_target: bool
    filter_status: str | None = None


class NewsReviewUpdate(BaseModel):
    gpt_filter_result: str | None = None
    gpt_filter_reason: str | None = None
    is_alert_target: bool | None = None
    filter_status: str | None = None


class AlertCandidateItem(BaseModel):
    news_id: int
    title: str
    source: str | None = None
    published_at: datetime | None = None
    related_stocks: list[str]
    importance_score: int
    duplicate_count: int
    source_count: int
    gpt_filter_result: str | None = None
    gpt_filter_reason: str | None = None
    is_alert_target: bool


class AlertCandidateRecalculateResult(BaseModel):
    processed_count: int
    alert_target_count: int
    changed_count: int


class AlertCandidateSummary(BaseModel):
    alert_target_count: int
    important_count: int
    price_impact_count: int
    high_importance_count: int


class AlertSendRequest(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    force: bool = False


class AlertSendItem(BaseModel):
    news_id: int
    stock_id: int | None = None
    title: str
    recipient_email: str | None = None
    status: str
    reason: str | None = None


class AlertSendResult(BaseModel):
    candidate_count: int
    sendable_count: int
    sent_count: int = 0
    failed_count: int = 0
    skipped_count: int
    skipped_reasons: dict[str, int]
    daily_sent_count: int
    hourly_sent_count: int
    would_send_items: list[AlertSendItem]
    sent_items: list[AlertSendItem] = []
    failed_items: list[AlertSendItem] = []


class AlertHistoryRead(BaseModel):
    id: int
    news_id: int | None = None
    stock_id: int | None = None
    price_alert_id: int | None = None
    alert_type: str
    recipient_email: str | None = None
    title: str
    message: str | None = None
    link_url: str | None = None
    status: str
    sent_at: datetime | None = None
    error_message: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertHistorySummary(BaseModel):
    total_count: int
    sent_count: int
    failed_count: int
    skipped_count: int
    today_sent_count: int
    hourly_sent_count: int
