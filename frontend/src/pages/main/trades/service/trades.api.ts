import { apiRequest } from '@/shared/utils/http'

import type { Trade, TradeNewsLink, TradeNewsLinkPayload, TradePayload, TradeUpdatePayload } from './trades.types'

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
  listNews: (tradeId: number) => apiRequest<TradeNewsLink[]>(`/api/trades/${tradeId}/news`),
  linkNews: (tradeId: number, payload: TradeNewsLinkPayload) =>
    apiRequest<TradeNewsLink>(`/api/trades/${tradeId}/news`, {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  unlinkNews: (tradeId: number, newsId: number) =>
    apiRequest<{ trade_id: number; news_id: number }>(`/api/trades/${tradeId}/news/${newsId}`, {
      method: 'DELETE',
    }),
}
