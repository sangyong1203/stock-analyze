export type MemoType = 'stock' | 'trade' | 'news' | 'general'
export type TagTargetType = 'stock' | 'trade' | 'news' | 'memo'

export interface Memo {
  id: number
  memo_type: MemoType
  title?: string | null
  content: string
  stock_id?: number | null
  trade_id?: number | null
  news_id?: number | null
  price_snapshot_id?: number | null
  memo_date?: string | null
  context_json?: Record<string, unknown> | null
  created_at: string
  updated_at: string
}

export interface MemoPayload {
  memo_type: MemoType
  title?: string | null
  content: string
  stock_id?: number | null
  trade_id?: number | null
  news_id?: number | null
  memo_date?: string | null
  context_json?: Record<string, unknown> | null
}

export type MemoUpdatePayload = Partial<Pick<MemoPayload, 'title' | 'content' | 'memo_date' | 'context_json'>>

export interface Tag {
  id: number
  name: string
  color?: string | null
  tag_type: string
  created_at: string
  updated_at: string
}

export interface TagPayload {
  name: string
  color?: string | null
  tag_type: string
}

export type TagUpdatePayload = Partial<TagPayload>

export interface TagLink {
  id: number
  tag_id: number
  target_type: TagTargetType
  target_id: number
  created_at: string
  tag_name: string
  tag_color?: string | null
  tag_type: string
}

export interface TagLinkPayload {
  tag_id: number
  target_type: TagTargetType
  target_id: number
}
