export function toNumber(value: string | number | null | undefined) {
  if (value === null || value === undefined || value === '') return 0
  return typeof value === 'number' ? value : Number(value)
}

export function formatKrw(value: string | number | null | undefined) {
  return `${Math.round(toNumber(value)).toLocaleString('ko-KR')}원`
}

export function formatSignedKrw(value: string | number | null | undefined) {
  const numeric = toNumber(value)
  const sign = numeric > 0 ? '+' : ''
  return `${sign}${Math.round(numeric).toLocaleString('ko-KR')}원`
}

export function formatPercent(value: string | number | null | undefined) {
  const numeric = toNumber(value) * 100
  const sign = numeric > 0 ? '+' : ''
  return `${sign}${numeric.toFixed(2)}%`
}

export function formatDateTime(value: string | null | undefined) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatDate(value: string | null | undefined) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleDateString('ko-KR')
}
