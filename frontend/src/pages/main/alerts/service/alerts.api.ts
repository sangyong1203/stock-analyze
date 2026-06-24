import { apiRequest } from '@/shared/utils/http'

import type { AlertCandidateSummary, AlertHistory, AlertHistorySummary, AlertSendRequest, AlertSendResult } from './alerts.types'

function historyQuery(status?: string) {
  if (!status) return ''
  const params = new URLSearchParams({ status })
  return `?${params.toString()}`
}

export const alertsApi = {
  dryRunSend: (payload: AlertSendRequest) =>
    apiRequest<AlertSendResult>('/api/news/alerts/send/dry-run', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  send: (payload: AlertSendRequest) =>
    apiRequest<AlertSendResult>('/api/news/alerts/send', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  histories: (status?: string) => apiRequest<AlertHistory[]>(`/api/news/alerts/histories${historyQuery(status)}`),
  historiesSummary: () => apiRequest<AlertHistorySummary>('/api/news/alerts/histories/summary'),
  candidateSummary: () => apiRequest<AlertCandidateSummary>('/api/news/alerts/summary'),
}
