import { defineStore } from 'pinia'

export const useTradesStore = defineStore('trades', {
  state: () => ({ tradeType: 'buy' as 'buy' | 'sell' }),
})
