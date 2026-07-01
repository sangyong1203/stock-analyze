import { apiRequest } from '@/shared/utils/http'

import type { DashboardSummary } from './dashboard.types'

export const dashboardApi = {
  summaryUrl: '/api/dashboard/summary',
  summary: () => apiRequest<DashboardSummary>('/api/dashboard/summary'),
}
