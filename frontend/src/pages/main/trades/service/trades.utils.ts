export function isSellTrade(type: string) {
  return type === 'sell'
}

export function formatTradeType(type: string) {
  return type === 'buy' ? '매수' : '매도'
}

export function formatKrw(value?: string | number | null) {
  if (value === undefined || value === null || value === '') return '-'
  return `${Number(value).toLocaleString('ko-KR')}원`
}
