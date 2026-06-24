import type { PriceAlertRow } from './alerts.types'

export function mapPriceAlert(alertType: string, enabled: boolean): PriceAlertRow {
  return { alertType, enabled }
}
