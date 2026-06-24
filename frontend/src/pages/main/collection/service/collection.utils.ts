export function isManualOverride(include: boolean, exclude: boolean) {
  return include || exclude
}

export function formatNumber(value?: string | number | null) {
  if (value === undefined || value === null || value === '') return '-'
  return Number(value).toLocaleString('ko-KR')
}
