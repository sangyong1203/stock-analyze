import { defineStore } from 'pinia'

export const useMemosStore = defineStore('memos', {
  state: () => ({ memoType: 'general' as 'stock' | 'trade' | 'news' | 'chart' | 'general' }),
})
