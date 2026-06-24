import { defineStore } from 'pinia'

export const useNewsStore = defineStore('news', {
  state: () => ({ filterStatus: 'all' }),
})
