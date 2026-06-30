export type ChartTimeframe = 'daily'

export interface OhlcvPoint {
  date: string
  open?: string | number | null
  high?: string | number | null
  low?: string | number | null
  close?: string | number | null
  volume?: number | null
  change_rate?: string | number | null
  ma20?: string | number | null
  ma60?: string | number | null
  ma120?: string | number | null
  rsi14?: string | number | null
  macd?: string | number | null
  macd_signal?: string | number | null
  macd_histogram?: string | number | null
}

export interface OhlcvResponse {
  stock_id: number
  timeframe: ChartTimeframe
  items: OhlcvPoint[]
}
