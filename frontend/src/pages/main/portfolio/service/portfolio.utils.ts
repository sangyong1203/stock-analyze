export function formatKrw(value?: string | number | null) {
  if (value === undefined || value === null || value === '') return '-'
  return `${Number(value).toLocaleString('ko-KR')}원`
}

export function formatPercent(value?: string | number | null) {
  if (value === undefined || value === null || value === '') return '-'
  return `${(Number(value) * 100).toFixed(2)}%`
}
