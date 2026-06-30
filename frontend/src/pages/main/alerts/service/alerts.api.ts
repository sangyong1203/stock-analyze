import { apiRequest } from '@/shared/utils/http'

import type {
  AlertHistory,
  PriceAlert,
  PriceAlertEvaluationRequest,
  PriceAlertEvaluationResult,
  PriceAlertPayload,
  PriceAlertSummary,
  PriceAlertUpdatePayload,
  StockOption,
} from './alerts.types'

function historyQuery(status?: string) {
  if (!status) return ''
  const params = new URLSearchParams({ status })
  return `?${params.toString()}`
}

export const alertsApi = {
  list: () => apiRequest<PriceAlert[]>('/api/price-alerts'),
  detail: (alertId: number) => apiRequest<PriceAlert>(`/api/price-alerts/${alertId}`),
  create: (payload: PriceAlertPayload) =>
    apiRequest<PriceAlert>('/api/price-alerts', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  update: (alertId: number, payload: PriceAlertUpdatePayload) =>
    apiRequest<PriceAlert>(`/api/price-alerts/${alertId}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    }),
  remove: (alertId: number) =>
    apiRequest<void>(`/api/price-alerts/${alertId}`, {
      method: 'DELETE',
    }),
  summary: () => apiRequest<PriceAlertSummary>('/api/price-alerts/summary'),
  histories: (status?: string) => apiRequest<AlertHistory[]>(`/api/price-alerts/histories${historyQuery(status)}`),
  dryRun: (payload: PriceAlertEvaluationRequest) =>
    apiRequest<PriceAlertEvaluationResult>('/api/price-alerts/evaluate/dry-run', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  evaluate: (payload: PriceAlertEvaluationRequest) =>
    apiRequest<PriceAlertEvaluationResult>('/api/price-alerts/evaluate', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  searchStocks: (query: string) =>
    apiRequest<StockOption[]>(`/api/stocks/search?q=${encodeURIComponent(query)}`),
}
