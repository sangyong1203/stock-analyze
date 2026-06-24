import { apiRequest } from '@/shared/utils/http'

import type { OhlcvResponse } from './charts.types'

function toQuery(limit: number) {
  const query = new URLSearchParams()
  query.set('timeframe', 'daily')
  query.set('limit', String(limit))
  return query.toString()
}

export const chartsApi = {
  summaryUrl: '/api/charts/summary',
  ohlcv: (stockId: number, limit = 120) => apiRequest<OhlcvResponse>(`/api/charts/stocks/${stockId}/ohlcv?${toQuery(limit)}`),
}
