export interface Stock {
  id: number
  code: string
  name: string
  market?: string | null
  sector?: string | null
  industry?: string | null
  market_cap?: string | number | null
  current_price?: string | number | null
  change_rate?: string | number | null
  aliases_json?: string[] | null
  is_favorite: boolean
  is_active: boolean
  is_holding: boolean
  created_at: string
  updated_at: string
}

export interface StockPayload {
  code: string
  name: string
  market?: string | null
  sector?: string | null
  industry?: string | null
  market_cap?: number | null
  current_price?: number | null
  change_rate?: number | null
  aliases_json?: string[] | null
  is_favorite?: boolean
  is_active?: boolean
}

export interface StockFilters {
  search?: string
  market?: string
  is_favorite?: boolean
  is_active?: boolean
}

export interface StockRow {
  code: string
  name: string
}
