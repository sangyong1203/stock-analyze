export function formatNumber(value?: string | number | null) {
  if (value === null || value === undefined || value === '') return '-'
  const numberValue = Number(value)
  if (Number.isNaN(numberValue)) return String(value)
  return new Intl.NumberFormat('ko-KR').format(numberValue)
}

export function formatDateTime(value?: string | null) {
  if (!value) return '-'
  return new Intl.DateTimeFormat('ko-KR', {
    year: '2-digit',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

export function formatSkippedReasons(reasons: Record<string, number>) {
  const entries = Object.entries(reasons)
  if (!entries.length) return '-'
  return entries.map(([key, count]) => `${key}: ${count}`).join(', ')
}
