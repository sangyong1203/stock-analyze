import type { News } from './news.types'

export function relatedStockLabel(news: News) {
  return news.stock_links.map((link) => `${link.stock_name ?? '-'}(${link.stock_code ?? '-'})`).join(', ')
}
