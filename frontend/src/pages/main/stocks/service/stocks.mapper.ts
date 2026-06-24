import type { Stock, StockPayload, StockRow } from './stocks.types'

export function mapStockRow(code: string, name: string): StockRow {
  return { code, name }
}

export function stockToPayload(stock: Stock): StockPayload {
  return {
    code: stock.code,
    name: stock.name,
    market: stock.market,
    sector: stock.sector,
    industry: stock.industry,
    market_cap: stock.market_cap == null ? null : Number(stock.market_cap),
    current_price: stock.current_price == null ? null : Number(stock.current_price),
    change_rate: stock.change_rate == null ? null : Number(stock.change_rate),
    aliases_json: stock.aliases_json ?? [],
    is_favorite: stock.is_favorite,
    is_active: stock.is_active,
  }
}
