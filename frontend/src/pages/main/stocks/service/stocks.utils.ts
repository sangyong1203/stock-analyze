export function normalizeStockCode(code: string) {
  return code.trim().padStart(6, '0')
}

export function parseAliasText(value: string) {
  return value
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean)
}

export function formatNumber(value?: string | number | null) {
  if (value === undefined || value === null || value === '') return '-'
  return Number(value).toLocaleString('ko-KR')
}
