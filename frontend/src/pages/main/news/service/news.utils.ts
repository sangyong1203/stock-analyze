export function isImportantScore(score: number) {
  return score >= 7
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

export function formatNumber(value?: number | null) {
  return new Intl.NumberFormat('ko-KR').format(value ?? 0)
}

export function importanceTagType(score: number) {
  if (score >= 7) return 'danger'
  if (score >= 4) return 'warning'
  return 'info'
}
