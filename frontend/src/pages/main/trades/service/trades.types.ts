export type TradeType = 'buy' | 'sell'

export interface Trade {
  id: number
  fund_pool_id: number
  fund_pool_name: string
  stock_id: number
  stock_code: string
  stock_name: string
  trade_type: TradeType
  trade_date: string
  quantity: number
  price: string | number
  amount: string | number
  fee: string | number
  tax: string | number
  total_amount: string | number
  average_price_at_trade?: string | number | null
  realized_profit_loss?: string | number | null
  realized_profit_loss_rate?: string | number | null
  reason?: string | null
  memo?: string | null
  created_at: string
  updated_at: string
}

export interface TradeNewsLink {
  id: number
  trade_id: number
  news_id: number
  link_type: string
  memo?: string | null
  created_at: string
  title: string
  source?: string | null
  published_at?: string | null
}

export interface TradeNewsLinkPayload {
  news_id: number
  link_type?: string
  memo?: string | null
}

export interface TradePayload {
  fund_pool_id: number
  stock_id: number
  trade_type: TradeType
  trade_date: string
  quantity: number
  price: number
  fee: number
  tax: number
  reason?: string | null
  memo?: string | null
}

export type TradeUpdatePayload = Partial<TradePayload>
