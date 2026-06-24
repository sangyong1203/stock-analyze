import { defineStore } from 'pinia'

export const useStocksStore = defineStore('stocks', {
  state: () => ({ keyword: '' }),
})
