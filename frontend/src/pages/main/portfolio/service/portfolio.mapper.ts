import type { HoldingRow } from './portfolio.types'

export function mapHoldingRow(stockName: string, quantity: number): HoldingRow {
  return { stockName, quantity }
}
