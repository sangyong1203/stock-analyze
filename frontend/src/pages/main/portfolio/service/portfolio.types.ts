export interface FundPool {
  id: number
  name: string
  currency: string
  cash_balance: string | number
  description?: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface FundPoolPayload {
  name: string
  currency?: string
  description?: string | null
  is_active?: boolean
}

export interface FundTransaction {
  id: number
  fund_pool_id: number
  fund_pool_name: string
  transaction_type: string
  amount: string | number
  currency: string
  related_trade_id?: number | null
  memo?: string | null
  transaction_date: string
  created_at: string
}

export interface FundTransactionPayload {
  fund_pool_id: number | null
  transaction_type: string
  amount: number
  currency?: string
  memo?: string | null
  transaction_date: string
}

export interface FundsSummary {
  active_pool_count: number
  total_cash: string | number
  total_deposit_amount: string | number
  total_withdraw_amount: string | number
  transaction_count: number
}

export interface Holding {
  id: number
  fund_pool_id: number
  fund_pool_name: string
  stock_id: number
  stock_code: string
  stock_name: string
  quantity: number
  average_price: string | number
  total_buy_amount: string | number
  current_price?: string | number | null
  market_value?: string | number | null
  unrealized_profit_loss?: string | number | null
  unrealized_profit_loss_rate?: string | number | null
  realized_profit_loss: string | number
  first_buy_date?: string | null
  last_trade_date?: string | null
  is_closed: boolean
  created_at: string
  updated_at: string
}

export interface HoldingRow {
  stockName: string
  quantity: number
}

export interface HoldingSummary {
  holding_count: number
  closed_holding_count: number
  total_market_value: string | number
  total_unrealized_profit_loss: string | number
  total_realized_profit_loss: string | number
}

export interface HoldingRecalculateResult {
  fund_pool_ids: number[]
  processed_trade_count: number
  holding_count: number
}

export interface PortfolioSummary {
  total_cash: string | number
  total_invested_amount: string | number
  total_market_value: string | number
  total_unrealized_profit_loss: string | number
  total_unrealized_profit_loss_rate?: string | number | null
  realized_profit_loss: string | number
  total_asset_value: string | number
  holding_count: number
  today_change_amount: string | number
  today_change_rate?: string | number | null
}
