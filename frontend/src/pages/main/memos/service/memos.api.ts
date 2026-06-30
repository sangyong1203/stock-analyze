import { apiRequest } from '@/shared/utils/http'

import type {
  Memo,
  MemoPayload,
  MemoUpdatePayload,
  Tag,
  TagLink,
  TagLinkPayload,
  TagPayload,
  TagTargetType,
  TagUpdatePayload,
} from './memos.types'

function memoQuery(filters: { memo_type?: string; stock_id?: number; trade_id?: number; news_id?: number }) {
  const params = new URLSearchParams()
  if (filters.memo_type) params.set('memo_type', filters.memo_type)
  if (filters.stock_id !== undefined) params.set('stock_id', String(filters.stock_id))
  if (filters.trade_id !== undefined) params.set('trade_id', String(filters.trade_id))
  if (filters.news_id !== undefined) params.set('news_id', String(filters.news_id))
  const query = params.toString()
  return query ? `?${query}` : ''
}

function tagQuery(filters: { tag_type?: string }) {
  const params = new URLSearchParams()
  if (filters.tag_type) params.set('tag_type', filters.tag_type)
  const query = params.toString()
  return query ? `?${query}` : ''
}

function linkQuery(target_type?: TagTargetType, target_id?: number) {
  const params = new URLSearchParams()
  if (target_type) params.set('target_type', target_type)
  if (target_id !== undefined) params.set('target_id', String(target_id))
  const query = params.toString()
  return query ? `?${query}` : ''
}

export const memosApi = {
  list: (filters: { memo_type?: string; stock_id?: number; trade_id?: number; news_id?: number }) =>
    apiRequest<Memo[]>(`/api/memos${memoQuery(filters)}`),
  create: (payload: MemoPayload) =>
    apiRequest<Memo>('/api/memos', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  update: (memoId: number, payload: MemoUpdatePayload) =>
    apiRequest<Memo>(`/api/memos/${memoId}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    }),
  remove: (memoId: number) =>
    apiRequest<void>(`/api/memos/${memoId}`, {
      method: 'DELETE',
    }),
  listTags: (filters: { tag_type?: string } = {}) => apiRequest<Tag[]>(`/api/tags${tagQuery(filters)}`),
  createTag: (payload: TagPayload) =>
    apiRequest<Tag>('/api/tags', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  updateTag: (tagId: number, payload: TagUpdatePayload) =>
    apiRequest<Tag>(`/api/tags/${tagId}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    }),
  removeTag: (tagId: number) =>
    apiRequest<void>(`/api/tags/${tagId}`, {
      method: 'DELETE',
    }),
  listTagLinks: (target_type?: TagTargetType, target_id?: number) =>
    apiRequest<TagLink[]>(`/api/tags/links${linkQuery(target_type, target_id)}`),
  createTagLink: (payload: TagLinkPayload) =>
    apiRequest<TagLink>('/api/tags/link', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  removeTagLink: (tagId: number, targetType: TagTargetType, targetId: number) =>
    apiRequest<{ deleted_tag_id: number; target_type: string; target_id: number }>(
      `/api/tags/link?tag_id=${tagId}&target_type=${targetType}&target_id=${targetId}`,
      { method: 'DELETE' },
    ),
}
