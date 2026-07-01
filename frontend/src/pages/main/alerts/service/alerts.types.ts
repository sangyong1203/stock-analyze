export type PriceAlertType =
  | 'TARGET_PRICE_ABOVE'
  | 'TARGET_PRICE_BELOW'
  | 'DROP_FROM_HIGH'
  | 'RISE_FROM_LOW'

export interface StockOption {
  id: number
  code: string
  name: string
  market?: string | null
  current_price?: string | number | null
}

export interface PriceAlert {
  id: number
  stock_id: number
  stock_code: string
  stock_name: string
  current_price?: string | number | null
  alert_type: PriceAlertType
  target_price?: string | number | null
  threshold_percent?: string | number | null
  lookback_days: number
  is_enabled: boolean
  triggered: boolean
  triggered_at?: string | null
  memo?: string | null
  created_at: string
  updated_at: string
}

export interface PriceAlertPayload {
  stock_id: number | null
  alert_type: PriceAlertType
  target_price?: number | null
  threshold_percent?: number | null
  is_enabled: boolean
  memo?: string | null
}

export interface PriceAlertUpdatePayload {
  stock_id?: number | null
  alert_type?: PriceAlertType
  target_price?: number | null
  threshold_percent?: number | null
  is_enabled?: boolean
  memo?: string | null
}

export interface PriceAlertSummary {
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

export interface AlertHistory {
  id: number
  stock_id?: number | null
  price_alert_id?: number | null
  alert_type: string
  recipient_email?: string | null
  title: string
  message?: string | null
  status: string
  sent_at?: string | null
  error_message?: string | null
  created_at: string
}

export interface PriceAlertEvaluationRequest {
  alert_ids?: number[]
  limit: number
  force: boolean
}

export interface PriceAlertEvaluationItem {
  price_alert_id: number
  stock_id: number
  stock_code: string
  stock_name: string
  alert_type: PriceAlertType
  current_price?: string | number | null
  target_price?: string | number | null
  threshold_percent?: string | number | null
  lookback_days: number
  recent_high?: string | number | null
  recent_low?: string | number | null
  trigger_price?: string | number | null
  latest_price_date?: string | null
  matched: boolean
  status: string
  skip_reason?: string | null
  recipient_email?: string | null
  subject?: string | null
  reason?: string | null
}

export interface PriceAlertEvaluationResult {
  evaluated_count: number
  matched_count: number
  sendable_count: number
  sent_count: number
  failed_count: number
  skipped_count: number
  skipped_reasons: Record<string, number>
  daily_sent_count: number
  hourly_sent_count: number
  items: PriceAlertEvaluationItem[]
}
