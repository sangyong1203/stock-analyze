import { apiRequest } from '@/shared/utils/http'

import type {
  FundPool,
  FundPoolPayload,
  FundsSummary,
  FundTransaction,
  FundTransactionPayload,
  Holding,
  HoldingRecalculateResult,
  HoldingSummary,
  PortfolioSummary,
} from './portfolio.types'

export const portfolioApi = {
  getSummary: () => apiRequest<PortfolioSummary>('/api/portfolio/summary'),
  getHoldings: () => apiRequest<Holding[]>('/api/holdings'),
  getHoldingSummary: () => apiRequest<HoldingSummary>('/api/holdings/summary'),
  recalculateHoldings: () =>
    apiRequest<HoldingRecalculateResult>('/api/holdings/recalculate', {
      method: 'POST',
    }),
  getFundPools: () => apiRequest<FundPool[]>('/api/funds/pools'),
  createFundPool: (payload: FundPoolPayload) =>
    apiRequest<FundPool>('/api/funds/pools', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  getFundTransactions: () => apiRequest<FundTransaction[]>('/api/funds/transactions'),
  createFundTransaction: (payload: FundTransactionPayload) =>
    apiRequest<FundTransaction>('/api/funds/transactions', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  getFundsSummary: () => apiRequest<FundsSummary>('/api/funds/summary'),
}
