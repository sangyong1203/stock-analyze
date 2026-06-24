export interface NewsStockLink {
  id: number
  news_id: number
  stock_id?: number | null
  stock_code?: string | null
  stock_name?: string | null
  relation_type: string
  relation_score?: number | null
  source_stock_code?: string | null
  created_at: string
}

export interface News {
  id: number
  title: string
  url: string
  source?: string | null
  published_at?: string | null
  original_summary?: string | null
  content_preview?: string | null
  normalized_title?: string | null
  source_type: string
  market_scope?: string | null
  event_type?: string | null
  duplicate_count: number
  source_count: number
  sources_json?: string[] | null
  first_published_at?: string | null
  last_published_at?: string | null
  filter_status?: string | null
  filter_reason?: string | null
  matched_keywords_json?: string[] | null
  importance_score: number
  gpt_summary?: string | null
  gpt_summary_model?: string | null
  gpt_summary_status?: string | null
  gpt_summary_at?: string | null
  gpt_filter_result?: string | null
  gpt_filter_reason?: string | null
  gpt_filter_model?: string | null
  gpt_filter_at?: string | null
  is_gpt_summary_target: boolean
  is_alert_target: boolean
  collected_at?: string | null
  stock_links: NewsStockLink[]
}

export interface NewsFilters {
  keyword?: string
  stock_code?: string
  market_scope?: string
  event_type?: string
  filter_status?: string
  min_importance_score?: number
  is_alert_target?: boolean
  is_gpt_summary_target?: boolean
  gpt_summary_status?: string
  gpt_filter_result?: string
  published_from?: string
  published_to?: string
}

export interface NewsSummary {
  total_news_count: number
  today_news_count: number
  linked_stock_news_count: number
  gpt_summary_target_count: number
  alert_target_count: number
  avg_importance_score: number
}

export interface MarketNewsCollectRequest {
  pages: number
  max_items: number
}

export interface NewsCollectJobItem {
  id: number
  job_id: number
  item_type: string
  target?: string | null
  status: string
  fetched_count: number
  new_count: number
  duplicate_count: number
  excluded_count: number
  error_message?: string | null
  started_at?: string | null
  finished_at?: string | null
  created_at: string
}

export interface NewsCollectJob {
  id: number
  job_type: string
  source_type: string
  trigger_type: string
  status: string
  started_at?: string | null
  finished_at?: string | null
  target_url?: string | null
  total_fetched_count: number
  new_count: number
  duplicate_count: number
  excluded_count: number
  gpt_target_count: number
  alert_target_count: number
  error_message?: string | null
  created_at: string
  items: NewsCollectJobItem[]
}

export interface GptRunRequest {
  limit: number
  dry_run: boolean
}

export interface GptRunItem {
  id: number
  title: string
  status: string
  result?: string | null
  reason?: string | null
}

export interface GptRunResult {
  dry_run: boolean
  processed_count: number
  target_count: number
  model?: string | null
  items: GptRunItem[]
}

export interface GptTargetsSummary {
  summary_pending_count: number
  summary_done_count: number
  summary_failed_count: number
  filter_pending_count: number
  filter_done_count: number
  filter_failed_count: number
}

export interface GptStatusSummary {
  total_news_count: number
  gpt_summary_target_count: number
  gpt_summary_done_count: number
  gpt_filter_done_count: number
  important_count: number
  price_impact_count: number
  unnecessary_count: number
}

export interface NewsReviewItem {
  news_id: number
  title: string
  source?: string | null
  published_at?: string | null
  related_stocks: string[]
  importance_score: number
  duplicate_count: number
  source_count: number
  gpt_summary?: string | null
  gpt_filter_result?: string | null
  gpt_filter_reason?: string | null
  is_alert_target: boolean
  filter_status?: string | null
}

export interface NewsReviewUpdate {
  gpt_filter_result?: string | null
  gpt_filter_reason?: string | null
  is_alert_target?: boolean
  filter_status?: string | null
}

export interface AlertCandidateItem {
  news_id: number
  title: string
  source?: string | null
  published_at?: string | null
  related_stocks: string[]
  importance_score: number
  duplicate_count: number
  source_count: number
  gpt_filter_result?: string | null
  gpt_filter_reason?: string | null
  is_alert_target: boolean
}

export interface AlertCandidateRecalculateResult {
  processed_count: number
  alert_target_count: number
  changed_count: number
}

export interface AlertCandidateSummary {
  alert_target_count: number
  important_count: number
  price_impact_count: number
  high_importance_count: number
}
