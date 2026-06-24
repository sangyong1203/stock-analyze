import { defineStore } from 'pinia'

export const useChartsStore = defineStore('charts', {
  state: () => ({ timeframe: 'daily' as 'daily' | 'weekly' | 'monthly' }),
})
