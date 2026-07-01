from sqlalchemy.orm import Session

from app.domains.alerts.service import get_price_alert_summary
from app.domains.dashboard import repository
from app.domains.dashboard.schemas import (
    DashboardAlertHistoryItem,
    DashboardHoldingItem,
    DashboardMemoItem,
    DashboardMemoSummary,
    DashboardNewsItem,
    DashboardSummary,
    DashboardTagItem,
    DashboardTradeItem,
)
from app.domains.holdings.service import get_holding_summary
from app.domains.news.service import get_alert_summary as get_news_alert_summary
from app.domains.portfolio.service import get_portfolio_summary

DEFAULT_HOLDING_LIMIT = 5
DEFAULT_RECENT_LIMIT = 5
DEFAULT_TAG_LIMIT = 10


def _serialize_holding(item, stock) -> DashboardHoldingItem:
    return DashboardHoldingItem(
        stock_id=stock.id,
        stock_code=stock.code,
        stock_name=stock.name,
        quantity=item.quantity,
        current_price=item.current_price,
        market_value=item.market_value,
        unrealized_profit_loss=item.unrealized_profit_loss,
        unrealized_profit_loss_rate=item.unrealized_profit_loss_rate,
    )


def _serialize_trade(trade, stock, fund_pool) -> DashboardTradeItem:
    return DashboardTradeItem(
        id=trade.id,
        stock_id=stock.id,
        stock_code=stock.code,
        stock_name=stock.name,
        fund_pool_name=fund_pool.name,
        trade_type=trade.trade_type,
        quantity=trade.quantity,
        price=trade.price,
        trade_date=trade.trade_date,
        memo=trade.memo,
    )


def _serialize_news(news) -> DashboardNewsItem:
    return DashboardNewsItem(
        id=news.id,
        title=news.title,
        source=news.source,
        published_at=news.published_at,
        importance_score=news.importance_score,
        gpt_summary_status=news.gpt_summary_status,
        is_alert_target=news.is_alert_target,
    )


def _serialize_history(history, stock_name: str | None, news_title: str | None) -> DashboardAlertHistoryItem:
    return DashboardAlertHistoryItem(
        id=history.id,
        alert_type=history.alert_type,
        status=history.status,
        title=history.title,
        stock_name=stock_name,
        news_title=news_title,
        created_at=history.created_at,
        sent_at=history.sent_at,
    )


def _serialize_memo(memo, stock_name: str | None, trade_id: int | None, news_title: str | None) -> DashboardMemoItem:
    if memo.stock_id is not None:
        target_type = "stock"
        target_label = stock_name
    elif memo.trade_id is not None:
        target_type = "trade"
        target_label = f"Trade #{trade_id}" if trade_id is not None else None
    elif memo.news_id is not None:
        target_type = "news"
        target_label = news_title
    else:
        target_type = "general"
        target_label = None
    return DashboardMemoItem(
        id=memo.id,
        memo_type=memo.memo_type,
        title=memo.title,
        content=memo.content,
        target_type=target_type,
        target_label=target_label,
        created_at=memo.created_at,
    )


def _serialize_tag(tag, usage_count: int) -> DashboardTagItem:
    return DashboardTagItem(
        id=tag.id,
        name=tag.name,
        color=tag.color,
        tag_type=tag.tag_type,
        usage_count=usage_count,
    )


def get_dashboard_summary(db: Session) -> DashboardSummary:
    portfolio_summary = get_portfolio_summary(db)
    holding_summary = get_holding_summary(db)
    price_alert_summary = get_price_alert_summary(db)
    news_alert_summary = get_news_alert_summary(db)

    top_holdings = [_serialize_holding(item, stock) for item, stock in repository.list_top_holdings(db, DEFAULT_HOLDING_LIMIT)]
    top_gainers = [_serialize_holding(item, stock) for item, stock in repository.list_top_gainers(db, DEFAULT_HOLDING_LIMIT)]
    top_losers = [_serialize_holding(item, stock) for item, stock in repository.list_top_losers(db, DEFAULT_HOLDING_LIMIT)]
    recent_trades = [_serialize_trade(trade, stock, fund_pool) for trade, stock, fund_pool in repository.list_recent_trades(db, DEFAULT_RECENT_LIMIT)]
    recent_news = [_serialize_news(news) for news in repository.list_recent_news(db, DEFAULT_RECENT_LIMIT)]
    recent_alert_histories = [
        _serialize_history(history, stock_name, news_title)
        for history, stock_name, news_title in repository.list_recent_alert_histories(db, DEFAULT_RECENT_LIMIT)
    ]
    recent_memos = [
        _serialize_memo(memo, stock_name, trade_id, news_title)
        for memo, stock_name, trade_id, news_title in repository.list_recent_memos(db, DEFAULT_RECENT_LIMIT)
    ]
    top_tags = [_serialize_tag(tag, usage_count) for tag, usage_count in repository.list_top_tags(db, DEFAULT_TAG_LIMIT)]

    return DashboardSummary(
        portfolio_summary=portfolio_summary,
        holding_summary=holding_summary,
        top_holdings=top_holdings,
        top_gainers=top_gainers,
        top_losers=top_losers,
        recent_trades=recent_trades,
        recent_news=recent_news,
        recent_alert_histories=recent_alert_histories,
        price_alert_summary=price_alert_summary,
        news_alert_summary=news_alert_summary,
        memo_summary=DashboardMemoSummary(recent_memos=recent_memos, top_tags=top_tags),
    )

