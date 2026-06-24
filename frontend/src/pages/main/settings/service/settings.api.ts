import { apiRequest } from '@/shared/utils/http'

import type { AlertSetting, AppSetting, NewsKeyword, ScheduledJob } from './settings.types'

export const settingsApi = {
  listUrl: '/api/settings/app-settings',
  listAppSettings: () => apiRequest<AppSetting[]>('/api/settings/app-settings'),
  updateAppSetting: (id: number, payload: Partial<AppSetting>) =>
    apiRequest<AppSetting>(`/api/settings/app-settings/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    }),
  listScheduledJobs: () => apiRequest<ScheduledJob[]>('/api/settings/scheduled-jobs'),
  updateScheduledJob: (id: number, payload: Partial<ScheduledJob>) =>
    apiRequest<ScheduledJob>(`/api/settings/scheduled-jobs/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    }),
  listNewsKeywords: () => apiRequest<NewsKeyword[]>('/api/settings/news-keywords'),
  createNewsKeyword: (payload: Omit<NewsKeyword, 'id' | 'created_at' | 'updated_at'>) =>
    apiRequest<NewsKeyword>('/api/settings/news-keywords', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  updateNewsKeyword: (id: number, payload: Partial<NewsKeyword>) =>
    apiRequest<NewsKeyword>(`/api/settings/news-keywords/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    }),
  deleteNewsKeyword: (id: number) =>
    apiRequest<void>(`/api/settings/news-keywords/${id}`, {
      method: 'DELETE',
    }),
  listAlertSettings: () => apiRequest<AlertSetting[]>('/api/settings/alert-settings'),
  updateAlertSetting: (id: number, payload: Partial<AlertSetting>) =>
    apiRequest<AlertSetting>(`/api/settings/alert-settings/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    }),
}
