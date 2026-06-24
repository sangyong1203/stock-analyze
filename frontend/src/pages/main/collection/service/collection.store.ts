import { defineStore } from 'pinia'

export const useCollectionStore = defineStore('collection', {
  state: () => ({ selectedRuleType: 'all' }),
})
