from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    name: Mapped[str | None] = mapped_column(String(100))
    google_sub: Mapped[str | None] = mapped_column(String(255), unique=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime)


class AppSetting(Base, TimestampMixin):
    __tablename__ = "app_settings"
    __table_args__ = (Index("uq_app_settings_key", "setting_key", unique=True),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    setting_key: Mapped[str] = mapped_column(String(100), nullable=False)
    setting_value: Mapped[str | None] = mapped_column(Text)
    value_type: Mapped[str] = mapped_column(String(30), default="string", nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class ScheduledJob(Base, TimestampMixin):
    __tablename__ = "scheduled_jobs"
    __table_args__ = (Index("uq_scheduled_jobs_key", "job_key", unique=True),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_key: Mapped[str] = mapped_column(String(100), nullable=False)
    job_name: Mapped[str] = mapped_column(String(100), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    schedule_type: Mapped[str] = mapped_column(String(30), nullable=False)
    cron_expression: Mapped[str | None] = mapped_column(String(100))
    config_json: Mapped[dict | None] = mapped_column(JSON)
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime)
    next_run_at: Mapped[datetime | None] = mapped_column(DateTime)


class SystemLog(Base):
    __tablename__ = "system_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[str] = mapped_column(String(20), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    context_json: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Stock(Base, TimestampMixin):
    __tablename__ = "stocks"
    __table_args__ = (
        Index("uq_stocks_code", "code", unique=True),
        Index("idx_stocks_name", "name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    market: Mapped[str | None] = mapped_column(String(20))
    sector: Mapped[str | None] = mapped_column(String(100))
    industry: Mapped[str | None] = mapped_column(String(100))
    market_cap: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    current_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    change_rate: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    aliases_json: Mapped[list | None] = mapped_column(JSON)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class IndexConstituent(Base, TimestampMixin):
    __tablename__ = "index_constituents"
    __table_args__ = (
        Index("idx_index_constituents_index_code", "index_code"),
        Index("idx_index_constituents_stock_code", "stock_code"),
        Index("uq_index_constituents_unique", "index_code", "stock_code", "effective_date", unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    index_code: Mapped[str] = mapped_column(String(50), nullable=False)
    index_name: Mapped[str] = mapped_column(String(100), nullable=False)
    tracking_index: Mapped[str | None] = mapped_column(String(100))
    stock_id: Mapped[int | None] = mapped_column(ForeignKey("stocks.id"))
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False)
    stock_name: Mapped[str] = mapped_column(String(100), nullable=False)
    market: Mapped[str | None] = mapped_column(String(20))
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    source: Mapped[str | None] = mapped_column(String(50))
    stock: Mapped[Stock | None] = relationship()


class StockPrice(Base):
    __tablename__ = "stock_prices"
    __table_args__ = (
        Index("idx_stock_prices_stock_date_timeframe", "stock_id", "date", "timeframe"),
        Index("uq_stock_prices_stock_date_timeframe", "stock_id", "date", "timeframe", unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)
    market: Mapped[str | None] = mapped_column(String(20))
    date: Mapped[date] = mapped_column(Date, nullable=False)
    timeframe: Mapped[str] = mapped_column(String(20), nullable=False)
    open: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    high: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    low: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    close: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    volume: Mapped[int | None] = mapped_column(Integer)
    trade_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    market_cap: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    listed_shares: Mapped[int | None] = mapped_column(Integer)
    change_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    change_rate: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    source: Mapped[str] = mapped_column(String(30), default="KRX", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    stock: Mapped[Stock] = relationship()


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"
    __table_args__ = (Index("idx_price_snapshots_stock_type", "stock_id", "snapshot_type"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)
    snapshot_type: Mapped[str] = mapped_column(String(30), nullable=False)
    related_id: Mapped[int | None] = mapped_column(Integer)
    price: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    change_rate: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    volume: Mapped[int | None] = mapped_column(Integer)
    market_cap: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    source: Mapped[str] = mapped_column(String(30), nullable=False)
    captured_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    stock: Mapped[Stock] = relationship()


class CorporateAction(Base, TimestampMixin):
    __tablename__ = "corporate_actions"
    __table_args__ = (Index("idx_corporate_actions_stock_date", "stock_id", "action_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)
    action_type: Mapped[str] = mapped_column(String(30), nullable=False)
    action_date: Mapped[date] = mapped_column(Date, nullable=False)
    base_date: Mapped[date | None] = mapped_column(Date)
    ratio: Mapped[str | None] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(50))
    stock: Mapped[Stock] = relationship()


class StockCollectionSetting(Base, TimestampMixin):
    __tablename__ = "stock_collection_settings"
    __table_args__ = (
        Index("idx_stock_collection_enabled", "collect_enabled"),
        Index("uq_stock_collection_stock", "stock_id", unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)
    collect_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    collect_news: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    collect_price_snapshot: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    collect_alert_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), default="normal", nullable=False)
    collect_reason: Mapped[str | None] = mapped_column(String(100))
    manual_override: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    manual_include: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    manual_exclude: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_collected_at: Mapped[datetime | None] = mapped_column(DateTime)
    stock: Mapped[Stock] = relationship()


class CollectionRule(Base, TimestampMixin):
    __tablename__ = "collection_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(30), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    condition_json: Mapped[dict | None] = mapped_column(JSON)
    priority: Mapped[int] = mapped_column(Integer, default=100, nullable=False)


class News(Base, TimestampMixin):
    __tablename__ = "news"
    __table_args__ = (
        Index("uq_news_url_hash", "url_hash", unique=True),
        Index("idx_news_title_hash_published", "title_hash", "published_at"),
        Index("idx_news_group_key", "news_group_key"),
        Index("idx_news_published_at", "published_at"),
        Index("idx_news_market_scope", "market_scope"),
        Index("idx_news_event_type", "event_type"),
        Index("idx_news_filter_status", "filter_status"),
        Index("idx_news_importance_score", "importance_score"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    source: Mapped[str | None] = mapped_column(String(100))
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    original_summary: Mapped[str | None] = mapped_column(Text)
    content_preview: Mapped[str | None] = mapped_column(Text)
    normalized_title: Mapped[str | None] = mapped_column(String(500))
    url_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    title_hash: Mapped[str | None] = mapped_column(String(128))
    news_group_key: Mapped[str | None] = mapped_column(String(255))
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    market_scope: Mapped[str | None] = mapped_column(String(30))
    event_type: Mapped[str | None] = mapped_column(String(50))
    detected_stock_codes_json: Mapped[list | None] = mapped_column(JSON)
    matched_index_codes_json: Mapped[list | None] = mapped_column(JSON)
    is_index_member_news: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    duplicate_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    source_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    sources_json: Mapped[list | None] = mapped_column(JSON)
    first_published_at: Mapped[datetime | None] = mapped_column(DateTime)
    last_published_at: Mapped[datetime | None] = mapped_column(DateTime)
    duplicate_check_window_hours: Mapped[int | None] = mapped_column(Integer)
    filter_status: Mapped[str | None] = mapped_column(String(50))
    filter_reason: Mapped[str | None] = mapped_column(Text)
    matched_keywords_json: Mapped[list | None] = mapped_column(JSON)
    importance_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    gpt_summary: Mapped[str | None] = mapped_column(Text)
    gpt_summary_model: Mapped[str | None] = mapped_column(String(100))
    gpt_summary_status: Mapped[str | None] = mapped_column(String(30))
    gpt_summary_at: Mapped[datetime | None] = mapped_column(DateTime)
    gpt_filter_result: Mapped[str | None] = mapped_column(String(50))
    gpt_filter_reason: Mapped[str | None] = mapped_column(Text)
    gpt_filter_model: Mapped[str | None] = mapped_column(String(100))
    gpt_filter_at: Mapped[datetime | None] = mapped_column(DateTime)
    is_gpt_summary_target: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_alert_target: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    collected_at: Mapped[datetime | None] = mapped_column(DateTime)
    stock_links: Mapped[list["NewsStockLink"]] = relationship(back_populates="news")


class NewsStockLink(Base):
    __tablename__ = "news_stock_links"
    __table_args__ = (
        Index("idx_news_stock_links_news_id", "news_id"),
        Index("idx_news_stock_links_stock_id", "stock_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    news_id: Mapped[int] = mapped_column(ForeignKey("news.id"), nullable=False)
    stock_id: Mapped[int | None] = mapped_column(ForeignKey("stocks.id"))
    stock_code: Mapped[str | None] = mapped_column(String(20))
    stock_name: Mapped[str | None] = mapped_column(String(100))
    relation_type: Mapped[str] = mapped_column(String(30), nullable=False)
    relation_score: Mapped[int | None] = mapped_column(Integer)
    source_stock_code: Mapped[str | None] = mapped_column(String(20))
    price_snapshot_id: Mapped[int | None] = mapped_column(ForeignKey("price_snapshots.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    news: Mapped[News] = relationship(back_populates="stock_links")


class NewsKeywordSetting(Base, TimestampMixin):
    __tablename__ = "news_keyword_settings"
    __table_args__ = (
        Index("idx_news_keyword_group_enabled", "group_type", "enabled"),
        Index("uq_news_keyword_group_keyword", "group_type", "keyword", unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_type: Mapped[str] = mapped_column(String(30), nullable=False)
    keyword: Mapped[str] = mapped_column(String(100), nullable=False)
    weight: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class NewsCollectJob(Base):
    __tablename__ = "news_collect_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_type: Mapped[str] = mapped_column(String(30), nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    trigger_type: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)
    target_url: Mapped[str | None] = mapped_column(String(1000))
    total_fetched_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    new_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    duplicate_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    excluded_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    gpt_target_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    alert_target_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    items: Mapped[list["NewsCollectJobItem"]] = relationship(back_populates="job")


class NewsCollectJobItem(Base):
    __tablename__ = "news_collect_job_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("news_collect_jobs.id"), nullable=False)
    item_type: Mapped[str] = mapped_column(String(30), nullable=False)
    target: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    fetched_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    new_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    duplicate_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    excluded_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    job: Mapped[NewsCollectJob] = relationship(back_populates="items")


class FundPool(Base, TimestampMixin):
    __tablename__ = "fund_pools"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="KRW", nullable=False)
    cash_balance: Mapped[Decimal] = mapped_column(Numeric(20, 2), default=0, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class FundTransaction(Base):
    __tablename__ = "fund_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fund_pool_id: Mapped[int] = mapped_column(ForeignKey("fund_pools.id"), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(30), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="KRW", nullable=False)
    related_trade_id: Mapped[int | None] = mapped_column(ForeignKey("trades.id"))
    memo: Mapped[str | None] = mapped_column(Text)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Trade(Base, TimestampMixin):
    __tablename__ = "trades"
    __table_args__ = (Index("idx_trades_stock_date", "stock_id", "trade_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fund_pool_id: Mapped[int] = mapped_column(ForeignKey("fund_pools.id"), nullable=False)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)
    trade_type: Mapped[str] = mapped_column(String(20), nullable=False)
    trade_date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False)
    fee: Mapped[Decimal] = mapped_column(Numeric(20, 2), default=0, nullable=False)
    tax: Mapped[Decimal] = mapped_column(Numeric(20, 2), default=0, nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False)
    price_snapshot_id: Mapped[int | None] = mapped_column(ForeignKey("price_snapshots.id"))
    average_price_at_trade: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    realized_profit_loss: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    realized_profit_loss_rate: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    target_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    target_achieved: Mapped[bool | None] = mapped_column(Boolean)
    target_achievement_rate: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    loss_rate: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    reason: Mapped[str | None] = mapped_column(Text)
    memo: Mapped[str | None] = mapped_column(Text)


class TradeNewsLink(Base):
    __tablename__ = "trade_news_links"
    __table_args__ = (
        Index("idx_trade_news_links_trade_id", "trade_id"),
        Index("idx_trade_news_links_news_id", "news_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trade_id: Mapped[int] = mapped_column(ForeignKey("trades.id"), nullable=False)
    news_id: Mapped[int] = mapped_column(ForeignKey("news.id"), nullable=False)
    link_type: Mapped[str] = mapped_column(String(30), nullable=False)
    memo: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Holding(Base, TimestampMixin):
    __tablename__ = "holdings"
    __table_args__ = (Index("idx_holdings_stock", "stock_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fund_pool_id: Mapped[int] = mapped_column(ForeignKey("fund_pools.id"), nullable=False)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_price: Mapped[Decimal] = mapped_column(Numeric(20, 2), default=0, nullable=False)
    total_buy_amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), default=0, nullable=False)
    current_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    market_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    unrealized_profit_loss: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    unrealized_profit_loss_rate: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    realized_profit_loss: Mapped[Decimal] = mapped_column(Numeric(20, 2), default=0, nullable=False)
    first_buy_date: Mapped[date | None] = mapped_column(Date)
    last_trade_date: Mapped[date | None] = mapped_column(Date)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class PriceAlert(Base, TimestampMixin):
    __tablename__ = "price_alerts"
    __table_args__ = (Index("idx_price_alerts_stock_enabled", "stock_id", "enabled"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    base_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 2))
    threshold_rate: Mapped[Decimal | None] = mapped_column(Numeric(10, 4))
    direction: Mapped[str | None] = mapped_column(String(20))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    triggered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    triggered_at: Mapped[datetime | None] = mapped_column(DateTime)
    memo: Mapped[str | None] = mapped_column(Text)


class AlertSetting(Base, TimestampMixin):
    __tablename__ = "alert_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    news_alert_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    price_alert_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    target_scope: Mapped[str] = mapped_column(String(50), default="holding_favorite_alert", nullable=False)
    min_importance_score: Mapped[int] = mapped_column(Integer, default=7, nullable=False)
    min_duplicate_count: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    min_source_count: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    event_types_json: Mapped[list | None] = mapped_column(JSON)
    keyword_groups_json: Mapped[list | None] = mapped_column(JSON)
    max_daily_alerts: Mapped[int] = mapped_column(Integer, default=200, nullable=False)
    max_hourly_alerts: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    send_email: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class AlertHistory(Base):
    __tablename__ = "alert_histories"
    __table_args__ = (Index("idx_alert_histories_status", "status"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    news_id: Mapped[int | None] = mapped_column(ForeignKey("news.id"))
    stock_id: Mapped[int | None] = mapped_column(ForeignKey("stocks.id"))
    price_alert_id: Mapped[int | None] = mapped_column(ForeignKey("price_alerts.id"))
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False)
    recipient_email: Mapped[str | None] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str | None] = mapped_column(Text)
    link_url: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Memo(Base, TimestampMixin):
    __tablename__ = "memos"
    __table_args__ = (Index("idx_memos_stock", "stock_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock_id: Mapped[int | None] = mapped_column(ForeignKey("stocks.id"))
    trade_id: Mapped[int | None] = mapped_column(ForeignKey("trades.id"))
    news_id: Mapped[int | None] = mapped_column(ForeignKey("news.id"))
    price_snapshot_id: Mapped[int | None] = mapped_column(ForeignKey("price_snapshots.id"))
    memo_type: Mapped[str] = mapped_column(String(30), nullable=False)
    title: Mapped[str | None] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    context_json: Mapped[dict | None] = mapped_column(JSON)
    memo_date: Mapped[date | None] = mapped_column(Date)


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"
    __table_args__ = (Index("uq_tags_name_type", "name", "tag_type", unique=True),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str | None] = mapped_column(String(20))
    tag_type: Mapped[str] = mapped_column(String(30), nullable=False)


class TagLink(Base):
    __tablename__ = "tag_links"
    __table_args__ = (Index("idx_tag_links_target", "target_type", "target_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), nullable=False)
    target_type: Mapped[str] = mapped_column(String(30), nullable=False)
    target_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
