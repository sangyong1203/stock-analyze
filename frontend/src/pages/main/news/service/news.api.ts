import { apiRequest } from '@/shared/utils/http'

import type {
  AlertCandidateItem,
  AlertCandidateRecalculateResult,
  AlertCandidateSummary,
  GptRunRequest,
  GptRunResult,
  GptStatusSummary,
  GptTargetsSummary,
  MarketNewsCollectRequest,
  News,
  NewsCollectJob,
  NewsFilters,
  NewsReviewItem,
  NewsReviewUpdate,
  NewsSummary,
} from './news.types'

function toQuery(filters: NewsFilters) {
  const params = new URLSearchParams()
  if (filters.keyword) params.set('keyword', filters.keyword)
  if (filters.stock_code) params.set('stock_code', filters.stock_code)
  if (filters.market_scope) params.set('market_scope', filters.market_scope)
  if (filters.event_type) params.set('event_type', filters.event_type)
  if (filters.filter_status) params.set('filter_status', filters.filter_status)
  if (filters.min_importance_score !== undefined) params.set('min_importance_score', String(filters.min_importance_score))
  if (filters.is_alert_target !== undefined) params.set('is_alert_target', String(filters.is_alert_target))
  if (filters.is_gpt_summary_target !== undefined) params.set('is_gpt_summary_target', String(filters.is_gpt_summary_target))
  if (filters.gpt_summary_status) params.set('gpt_summary_status', filters.gpt_summary_status)
  if (filters.gpt_filter_result) params.set('gpt_filter_result', filters.gpt_filter_result)
  if (filters.published_from) params.set('published_from', filters.published_from)
  if (filters.published_to) params.set('published_to', filters.published_to)
  const query = params.toString()
  return query ? `?${query}` : ''
}

export const newsApi = {
  listUrl: '/api/news',
  list: (filters: NewsFilters) => apiRequest<News[]>(`/api/news${toQuery(filters)}`),
  summary: () => apiRequest<NewsSummary>('/api/news/summary'),
  detail: (id: number) => apiRequest<News>(`/api/news/${id}`),
  collectMarket: (payload: MarketNewsCollectRequest) =>
    apiRequest<NewsCollectJob>('/api/news/collect/market', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  listJobs: () => apiRequest<NewsCollectJob[]>('/api/news/collect/jobs'),
  detailJob: (id: number) => apiRequest<NewsCollectJob>(`/api/news/collect/jobs/${id}`),
  gptTargets: () => apiRequest<GptTargetsSummary>('/api/news/gpt/targets'),
  gptStatus: () => apiRequest<GptStatusSummary>('/api/news/gpt/status'),
  runGptSummary: (payload: GptRunRequest) =>
    apiRequest<GptRunResult>('/api/news/gpt/summary/run', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  runGptFilter: (payload: GptRunRequest) =>
    apiRequest<GptRunResult>('/api/news/gpt/filter/run', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  review: (filters: NewsFilters) => apiRequest<NewsReviewItem[]>(`/api/news/gpt/review${toQuery(filters)}`),
  updateReview: (id: number, payload: NewsReviewUpdate) =>
    apiRequest<NewsReviewItem>(`/api/news/gpt/review/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    }),
  recalculateAlertCandidates: () =>
    apiRequest<AlertCandidateRecalculateResult>('/api/news/alerts/candidates/recalculate', {
      method: 'POST',
    }),
  alertCandidates: (filters: NewsFilters) => apiRequest<AlertCandidateItem[]>(`/api/news/alerts/candidates${toQuery(filters)}`),
  alertSummary: () => apiRequest<AlertCandidateSummary>('/api/news/alerts/summary'),
}
