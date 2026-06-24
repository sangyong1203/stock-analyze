import { apiRequest } from '@/shared/utils/http'

export interface KrxDailyCollectRequest {
  bas_date: string
  markets: string[]
  dry_run: boolean
}

export interface KrxDailyCollectResult {
  bas_date: string
  markets: string[]
  fetched_count: number
  inserted_count: number
  updated_count: number
  stock_created_count: number
  error_count: number
  errors: string[]
}

export const pricesApi = {
  collectKrxDaily: (payload: KrxDailyCollectRequest) =>
    apiRequest<KrxDailyCollectResult>('/api/prices/collect/krx/daily', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
}
