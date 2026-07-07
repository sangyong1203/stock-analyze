export function isManualOverride(include: boolean, exclude: boolean) {
  return include || exclude
}

export function formatNumber(value?: string | number | null) {
  if (value === undefined || value === null || value === '') return '-'
  return Number(value).toLocaleString('ko-KR')
}

export function formatCompactKoreanNumber(value?: string | number | null) {
  if (value === undefined || value === null || value === '') return '-'

  const numericValue = Number(value)
  if (!Number.isFinite(numericValue)) return '-'

  const absValue = Math.abs(numericValue)
  if (absValue >= 1_0000_0000_0000) {
    return `${(numericValue / 1_0000_0000_0000).toFixed(2)}조`
  }
  if (absValue >= 1_0000_0000) {
    return `${(numericValue / 1_0000_0000).toFixed(0)}억`
  }
  if (absValue >= 1_0000) {
    return `${(numericValue / 1_0000).toFixed(0)}만`
  }
  return numericValue.toLocaleString('ko-KR')
}
