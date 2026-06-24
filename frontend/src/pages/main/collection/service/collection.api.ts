import { apiRequest } from '@/shared/utils/http'

import type { CollectionFilters, CollectionRule, CollectionStock, CollectionStockSummary, RecalculateResult } from './collection.types'

function toQuery(filters: CollectionFilters) {
  const params = new URLSearchParams()
  if (filters.keyword) params.set('keyword', filters.keyword)
  if (filters.market) params.set('market', filters.market)
  if (filters.collect_enabled !== undefined) params.set('collect_enabled', String(filters.collect_enabled))
  if (filters.priority) params.set('priority', filters.priority)
  if (filters.collect_reason) params.set('collect_reason', filters.collect_reason)
  const query = params.toString()
  return query ? `?${query}` : ''
}

export const collectionApi = {
  rulesUrl: '/api/collection/rules',
  listStocks: (filters: CollectionFilters) => apiRequest<CollectionStock[]>(`/api/collection/stocks${toQuery(filters)}`),
  summary: () => apiRequest<CollectionStockSummary>('/api/collection/stocks/summary'),
  updateStock: (stockId: number, payload: Partial<CollectionStock>) =>
    apiRequest<CollectionStock>(`/api/collection/stocks/${stockId}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    }),
  includeStock: (stockId: number) =>
    apiRequest<CollectionStock>(`/api/collection/stocks/${stockId}/include`, {
      method: 'POST',
    }),
  excludeStock: (stockId: number) =>
    apiRequest<CollectionStock>(`/api/collection/stocks/${stockId}/exclude`, {
      method: 'POST',
    }),
  recalculate: () =>
    apiRequest<RecalculateResult>('/api/collection/stocks/recalculate', {
      method: 'POST',
    }),
  listRules: () => apiRequest<CollectionRule[]>('/api/collection/rules'),
  createRule: (payload: Omit<CollectionRule, 'id' | 'created_at' | 'updated_at'>) =>
    apiRequest<CollectionRule>('/api/collection/rules', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  updateRule: (id: number, payload: Partial<CollectionRule>) =>
    apiRequest<CollectionRule>(`/api/collection/rules/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    }),
  deleteRule: (id: number) =>
    apiRequest<void>(`/api/collection/rules/${id}`, {
      method: 'DELETE',
    }),
}
