export interface DashboardHoldingItem {
  stock_id: number
  stock_code: string
  stock_name: string
  quantity: number
  current_price?: string | number | null
  market_value?: string | number | null
  unrealized_profit_loss?: string | number | null
  unrealized_profit_loss_rate?: string | number | null
}

export interface DashboardTradeItem {
  id: number
  stock_id: number
  stock_code: string
  stock_name: string
  fund_pool_name: string
  trade_type: string
  quantity: number
  price: string | number
  trade_date: string
  memo?: string | null
}

export interface DashboardNewsItem {
  id: number
  title: string
  source?: string | null
  published_at?: string | null
  importance_score: number
  gpt_summary_status?: string | null
  is_alert_target: boolean
}

export interface DashboardAlertHistoryItem {
  id: number
  alert_type: string
  status: string
  title: string
  stock_name?: string | null
  news_title?: string | null
  created_at: string
  sent_at?: string | null
}

export interface DashboardMemoItem {
  id: number
  memo_type: string
  title?: string | null
  content: string
  target_type: string
  target_label?: string | null
  created_at: string
}

export interface DashboardTagItem {
  id: number
  name: string
  color?: string | null
  tag_type: string
  usage_count: number
}

export interface DashboardPortfolioSummary {
  total_cash: string | number
  total_invested_amount: string | number
  total_market_value: string | number
  total_unrealized_profit_loss: string | number
  total_unrealized_profit_loss_rate?: string | number | null
  realized_profit_loss: string | number
  total_asset_value: string | number
  holding_count: number
  today_change_amount: string | number
  today_change_rate?: string | number | null
}

export interface DashboardHoldingSummary {
  holding_count: number
  closed_holding_count: number
  total_market_value: string | number
  total_unrealized_profit_loss: string | number
  total_realized_profit_loss: string | number
}

export interface DashboardPriceAlertSummary {
  total_count: number
  enabled_count: number
  disabled_count: number
  triggered_count: number
  sent_count: number
  failed_count: number
  skipped_count: number
  today_sent_count: number
  hourly_sent_count: number
}

export interface DashboardNewsAlertSummary {
  alert_target_count: number
  important_count: number
  price_impact_count: number
  high_importance_count: number
}

export interface DashboardMemoSummary {
  recent_memos: DashboardMemoItem[]
  top_tags: DashboardTagItem[]
}

export interface DashboardSummary {
  portfolio_summary: DashboardPortfolioSummary
  holding_summary: DashboardHoldingSummary
  top_holdings: DashboardHoldingItem[]
  top_gainers: DashboardHoldingItem[]
  top_losers: DashboardHoldingItem[]
  recent_trades: DashboardTradeItem[]
  recent_news: DashboardNewsItem[]
  recent_alert_histories: DashboardAlertHistoryItem[]
  price_alert_summary: DashboardPriceAlertSummary
  news_alert_summary: DashboardNewsAlertSummary
  memo_summary: DashboardMemoSummary
}
