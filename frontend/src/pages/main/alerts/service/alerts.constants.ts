import type { PriceAlertType } from './alerts.types'

export const ALERT_TYPE_OPTIONS: Array<{ label: string; value: PriceAlertType }> = [
  { label: '목표가 이상', value: 'TARGET_PRICE_ABOVE' },
  { label: '목표가 이하', value: 'TARGET_PRICE_BELOW' },
  { label: '고점 대비 하락률', value: 'DROP_FROM_HIGH' },
  { label: '저점 대비 상승률', value: 'RISE_FROM_LOW' },
]
