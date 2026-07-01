export interface AppSetting {
  id: number
  setting_key: string
  setting_value?: string | null
  value_type: string
  description?: string | null
  created_at: string
  updated_at: string
}

export interface ScheduledJob {
  id: number
  job_key: string
  job_name: string
  enabled: boolean
  schedule_type: string
  cron_expression?: string | null
  config_json?: Record<string, unknown> | null
  last_run_at?: string | null
  next_run_at?: string | null
  last_status?: string | null
  last_message?: string | null
  last_started_at?: string | null
  last_finished_at?: string | null
  created_at: string
  updated_at: string
}

export interface JobRunResult {
  job_id: number
  job_key: string
  status: string
  started_at: string
  finished_at: string
  message: string
  result: Record<string, unknown>
}

export interface JobSummary {
  total_count: number
  enabled_count: number
  disabled_count: number
  success_count: number
  failed_count: number
  never_run_count: number
  recent_runs: JobRunResult[]
}

export interface NewsKeyword {
  id: number
  group_type: string
  keyword: string
  weight: number
  enabled: boolean
  is_default: boolean
  created_at: string
  updated_at: string
}

export interface AlertSetting {
  id: number
  enabled: boolean
  news_alert_enabled: boolean
  price_alert_enabled: boolean
  target_scope: string
  min_importance_score: number
  min_duplicate_count: number
  min_source_count: number
  event_types_json?: string[] | null
  keyword_groups_json?: string[] | null
  max_daily_alerts: number
  max_hourly_alerts: number
  send_email: boolean
  created_at: string
  updated_at: string
}

export interface SettingRow {
  settingKey: string
  settingValue?: string | null
}
