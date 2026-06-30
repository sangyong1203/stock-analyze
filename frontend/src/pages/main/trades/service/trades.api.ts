import { apiRequest } from '@/shared/utils/http'

import type { Trade, TradePayload, TradeUpdatePayload } from './trades.types'

export const tradesApi = {
  list: () => apiRequest<Trade[]>('/api/trades'),
  detail: (tradeId: number) => apiRequest<Trade>(`/api/trades/${tradeId}`),
  create: (payload: TradePayload) =>
    apiRequest<Trade>('/api/trades', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  update: (tradeId: number, payload: TradeUpdatePayload) =>
    apiRequest<Trade>(`/api/trades/${tradeId}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    }),
  remove: (tradeId: number) =>
    apiRequest<{ deleted_trade_id: number }>(`/api/trades/${tradeId}`, {
      method: 'DELETE',
    }),
}
