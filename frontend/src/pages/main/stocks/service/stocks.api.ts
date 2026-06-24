import { apiRequest } from '@/shared/utils/http'

import type { Stock, StockFilters, StockPayload } from './stocks.types'

function toQuery(filters: StockFilters) {
  const params = new URLSearchParams()
  if (filters.search) params.set('search', filters.search)
  if (filters.market) params.set('market', filters.market)
  if (filters.is_favorite !== undefined) params.set('is_favorite', String(filters.is_favorite))
  if (filters.is_active !== undefined) params.set('is_active', String(filters.is_active))
  const query = params.toString()
  return query ? `?${query}` : ''
}

export const stocksApi = {
  listUrl: '/api/stocks',
  list: (filters: StockFilters) => apiRequest<Stock[]>(`/api/stocks${toQuery(filters)}`),
  detail: (id: number) => apiRequest<Stock>(`/api/stocks/${id}`),
  create: (payload: StockPayload) =>
    apiRequest<Stock>('/api/stocks', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  update: (id: number, payload: Partial<StockPayload>) =>
    apiRequest<Stock>(`/api/stocks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    }),
  deactivate: (id: number) =>
    apiRequest<Stock>(`/api/stocks/${id}`, {
      method: 'DELETE',
    }),
  setFavorite: (id: number, isFavorite: boolean) =>
    apiRequest<Stock>(`/api/stocks/${id}/favorite`, {
      method: 'PATCH',
      body: JSON.stringify({ is_favorite: isFavorite }),
    }),
}
