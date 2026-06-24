import { defineStore } from 'pinia'

export const useAlertsStore = defineStore('alerts', {
  state: () => ({ enabledOnly: true }),
})
