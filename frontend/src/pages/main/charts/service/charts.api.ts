import { apiRequest } from '@/shared/utils/http'

import type { OhlcvResponse } from './charts.types'

interface OhlcvQuery {
  limit?: number
  date_from?: string
  date_to?: string
}

function toQuery(options: OhlcvQuery) {
  const query = new URLSearchParams()
  query.set('timeframe', 'daily')
  if (options.limit) query.set('limit', String(options.limit))
  if (options.date_from) query.set('date_from', options.date_from)
  if (options.date_to) query.set('date_to', options.date_to)
  return query.toString()
}

export const chartsApi = {
  summaryUrl: '/api/charts/summary',
  ohlcv: (stockId: number, options: OhlcvQuery = { limit: 130 }) =>
    apiRequest<OhlcvResponse>(`/api/charts/stocks/${stockId}/ohlcv?${toQuery(options)}`),
}
