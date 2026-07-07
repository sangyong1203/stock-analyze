export interface CollectionStock {
  stock_id: number
  stock_code: string
  stock_name: string
  market?: string | null
  sector?: string | null
  market_cap?: string | number | null
  current_price?: string | number | null
  is_favorite: boolean
  is_holding_calculated: boolean
  collect_enabled: boolean
  collect_news: boolean
  collect_price_snapshot: boolean
  collect_alert_enabled: boolean
  priority: string
  collect_reason?: string | null
  manual_override: boolean
  manual_include: boolean
  manual_exclude: boolean
  last_collected_at?: string | null
}

export interface CollectionStockSummary {
  total_candidate_count: number
  collect_enabled_count: number
  collect_news_count: number
  collect_alert_enabled_count: number
  manual_include_count: number
  manual_exclude_count: number
}

export interface CollectionRule {
  id: number
  name: string
  rule_type: string
  enabled: boolean
  condition_json?: Record<string, unknown> | null
  priority: number
  created_at: string
  updated_at: string
}

export interface CollectionRuleRow {
  name: string
  enabled: boolean
}

export interface CollectionFilters {
  keyword?: string
  market?: string
  collect_enabled?: boolean
  priority?: string
  collect_reason?: string
  page?: number
  page_size?: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

export interface CollectionStockListResponse {
  items: CollectionStock[]
  total_count: number
  page: number
  page_size: number
}

export type CollectionStockListApiResponse = CollectionStockListResponse | CollectionStock[]

export interface RecalculateResult {
  processed_count: number
  collect_enabled_count: number
  manual_exclude_count: number
}
