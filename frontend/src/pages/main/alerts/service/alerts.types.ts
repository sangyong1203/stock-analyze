export interface AlertSendRequest {
  limit: number
  force: boolean
}

export interface PriceAlertRow {
  alertType: string
  enabled: boolean
}

export interface AlertSendItem {
  news_id: number
  stock_id?: number | null
  title: string
  recipient_email?: string | null
  status: string
  reason?: string | null
}

export interface AlertSendResult {
  candidate_count: number
  sendable_count: number
  sent_count: number
  failed_count: number
  skipped_count: number
  skipped_reasons: Record<string, number>
  daily_sent_count: number
  hourly_sent_count: number
  would_send_items: AlertSendItem[]
  sent_items: AlertSendItem[]
  failed_items: AlertSendItem[]
}

export interface AlertHistory {
  id: number
  news_id?: number | null
  stock_id?: number | null
  alert_type: string
  recipient_email?: string | null
  title: string
  message?: string | null
  link_url?: string | null
  status: string
  sent_at?: string | null
  error_message?: string | null
  created_at: string
}

export interface AlertHistorySummary {
  total_count: number
  sent_count: number
  failed_count: number
  skipped_count: number
  today_sent_count: number
  hourly_sent_count: number
}

export interface AlertCandidateSummary {
  alert_target_count: number
  important_count: number
  price_impact_count: number
  high_importance_count: number
}
