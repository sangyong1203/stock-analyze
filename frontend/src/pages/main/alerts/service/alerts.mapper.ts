import type { PriceAlert, PriceAlertPayload } from './alerts.types'

export function alertToPayload(alert: PriceAlert): PriceAlertPayload {
  return {
    stock_id: alert.stock_id,
    alert_type: alert.alert_type,
    target_price: alert.target_price == null ? null : Number(alert.target_price),
    threshold_percent: alert.threshold_percent == null ? null : Number(alert.threshold_percent),
    is_enabled: alert.is_enabled,
    memo: alert.memo ?? '',
  }
}
