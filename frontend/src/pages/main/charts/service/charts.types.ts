export type ChartTimeframe = 'daily'

export interface OhlcvPoint {
  date: string
  open?: string | number | null
  high?: string | number | null
  low?: string | number | null
  close?: string | number | null
  volume?: number | null
  change_rate?: string | number | null
}

export interface OhlcvResponse {
  stock_id: number
  timeframe: ChartTimeframe
  items: OhlcvPoint[]
}
