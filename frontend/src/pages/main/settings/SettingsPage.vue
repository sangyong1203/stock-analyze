<template>
  <section class="settings-page">
    <div class="kpi-grid">
      <article class="kpi-item">
        <span>시스템 설정</span>
        <strong>{{ appSettings.length }}</strong>
      </article>
      <article class="kpi-item">
        <span>스케줄 작업</span>
        <strong>{{ scheduledJobs.length }}</strong>
      </article>
      <article class="kpi-item">
        <span>뉴스 키워드</span>
        <strong>{{ newsKeywords.length }}</strong>
      </article>
      <article class="kpi-item">
        <span>알림 설정</span>
        <strong>{{ alertSettings.length }}</strong>
      </article>
    </div>

    <div class="content-band settings-panel">
      <div class="panel-head">
        <div>
          <h2 class="section-title">시스템 설정</h2>
          <p class="muted">수집 시간, 중복 기준, GPT 요약 기준, 알림 기준을 관리합니다.</p>
        </div>
        <el-button :loading="loading" @click="loadSettings">새로고침</el-button>
      </div>

      <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon :closable="false" />

      <el-tabs v-model="activeTab">
        <el-tab-pane label="전역 설정" name="app">
          <el-table :data="appSettings" border>
            <el-table-column prop="setting_key" label="키" min-width="220" />
            <el-table-column label="값" min-width="220">
              <template #default="{ row }">
                <el-input v-model="row.setting_value" @change="saveAppSetting(row)" />
              </template>
            </el-table-column>
            <el-table-column prop="value_type" label="타입" width="120" />
            <el-table-column prop="description" label="설명" min-width="240" />
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="스케줄" name="jobs">
          <el-table :data="scheduledJobs" border>
            <el-table-column prop="job_key" label="작업 키" min-width="180" />
            <el-table-column prop="job_name" label="작업명" min-width="180" />
            <el-table-column label="사용" width="100">
              <template #default="{ row }">
                <el-switch v-model="row.enabled" @change="saveScheduledJob(row)" />
              </template>
            </el-table-column>
            <el-table-column prop="schedule_type" label="스케줄 유형" width="140" />
            <el-table-column label="설정 JSON" min-width="260">
              <template #default="{ row }">
                <code>{{ row.config_json ?? {} }}</code>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="뉴스 키워드" name="keywords">
          <div class="keyword-form">
            <el-select v-model="keywordDraft.group_type" placeholder="그룹">
              <el-option v-for="group in keywordGroups" :key="group" :label="group" :value="group" />
            </el-select>
            <el-input v-model="keywordDraft.keyword" placeholder="키워드" />
            <el-input-number v-model="keywordDraft.weight" :min="-10" :max="10" />
            <el-button type="primary" @click="createKeyword">추가</el-button>
          </div>

          <el-table :data="newsKeywords" border>
            <el-table-column prop="group_type" label="그룹" width="130" />
            <el-table-column label="키워드" min-width="180">
              <template #default="{ row }">
                <el-input v-model="row.keyword" @change="saveNewsKeyword(row)" />
              </template>
            </el-table-column>
            <el-table-column label="가중치" width="140">
              <template #default="{ row }">
                <el-input-number v-model="row.weight" :min="-10" :max="10" @change="saveNewsKeyword(row)" />
              </template>
            </el-table-column>
            <el-table-column label="사용" width="100">
              <template #default="{ row }">
                <el-switch v-model="row.enabled" @change="saveNewsKeyword(row)" />
              </template>
            </el-table-column>
            <el-table-column label="삭제" width="90">
              <template #default="{ row }">
                <el-button type="danger" link :disabled="row.is_default" @click="deleteKeyword(row.id)">삭제</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="알림" name="alerts">
          <el-table :data="alertSettings" border>
            <el-table-column label="전체" width="90">
              <template #default="{ row }">
                <el-switch v-model="row.enabled" @change="saveAlertSetting(row)" />
              </template>
            </el-table-column>
            <el-table-column label="뉴스" width="90">
              <template #default="{ row }">
                <el-switch v-model="row.news_alert_enabled" @change="saveAlertSetting(row)" />
              </template>
            </el-table-column>
            <el-table-column label="가격" width="90">
              <template #default="{ row }">
                <el-switch v-model="row.price_alert_enabled" @change="saveAlertSetting(row)" />
              </template>
            </el-table-column>
            <el-table-column label="중요도" width="140">
              <template #default="{ row }">
                <el-input-number v-model="row.min_importance_score" :min="0" :max="10" @change="saveAlertSetting(row)" />
              </template>
            </el-table-column>
            <el-table-column label="중복" width="140">
              <template #default="{ row }">
                <el-input-number v-model="row.min_duplicate_count" :min="0" :max="20" @change="saveAlertSetting(row)" />
              </template>
            </el-table-column>
            <el-table-column label="일일 한도" width="150">
              <template #default="{ row }">
                <el-input-number v-model="row.max_daily_alerts" :min="0" @change="saveAlertSetting(row)" />
              </template>
            </el-table-column>
            <el-table-column label="시간당 한도" width="150">
              <template #default="{ row }">
                <el-input-number v-model="row.max_hourly_alerts" :min="0" @change="saveAlertSetting(row)" />
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { onMounted, reactive, ref } from 'vue'

import { settingsApi } from './service/settings.api'
import type { AlertSetting, AppSetting, NewsKeyword, ScheduledJob } from './service/settings.types'

const activeTab = ref('app')
const loading = ref(false)
const errorMessage = ref('')
const appSettings = ref<AppSetting[]>([])
const scheduledJobs = ref<ScheduledJob[]>([])
const newsKeywords = ref<NewsKeyword[]>([])
const alertSettings = ref<AlertSetting[]>([])

const keywordGroups = ['market', 'sector', 'macro', 'policy', 'exclude', 'event']
const keywordDraft = reactive({
  group_type: 'market',
  keyword: '',
  weight: 1,
  enabled: true,
  is_default: false,
})

async function loadSettings() {
  loading.value = true
  errorMessage.value = ''
  try {
    const [app, jobs, keywords, alerts] = await Promise.all([
      settingsApi.listAppSettings(),
      settingsApi.listScheduledJobs(),
      settingsApi.listNewsKeywords(),
      settingsApi.listAlertSettings(),
    ])
    appSettings.value = app
    scheduledJobs.value = jobs
    newsKeywords.value = keywords
    alertSettings.value = alerts
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '설정을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

async function saveAppSetting(row: AppSetting) {
  await settingsApi.updateAppSetting(row.id, {
    setting_value: row.setting_value,
    value_type: row.value_type,
    description: row.description,
  })
  ElMessage.success('전역 설정을 저장했습니다.')
}

async function saveScheduledJob(row: ScheduledJob) {
  await settingsApi.updateScheduledJob(row.id, {
    job_name: row.job_name,
    enabled: row.enabled,
    schedule_type: row.schedule_type,
    cron_expression: row.cron_expression,
    config_json: row.config_json,
  })
  ElMessage.success('스케줄 설정을 저장했습니다.')
}

async function createKeyword() {
  if (!keywordDraft.keyword.trim()) {
    ElMessage.warning('키워드를 입력하세요.')
    return
  }
  await settingsApi.createNewsKeyword({ ...keywordDraft, keyword: keywordDraft.keyword.trim() })
  keywordDraft.keyword = ''
  await loadSettings()
  ElMessage.success('뉴스 키워드를 추가했습니다.')
}

async function saveNewsKeyword(row: NewsKeyword) {
  await settingsApi.updateNewsKeyword(row.id, {
    group_type: row.group_type,
    keyword: row.keyword,
    weight: row.weight,
    enabled: row.enabled,
    is_default: row.is_default,
  })
  ElMessage.success('뉴스 키워드를 저장했습니다.')
}

async function deleteKeyword(id: number) {
  await settingsApi.deleteNewsKeyword(id)
  await loadSettings()
  ElMessage.success('뉴스 키워드를 삭제했습니다.')
}

async function saveAlertSetting(row: AlertSetting) {
  await settingsApi.updateAlertSetting(row.id, {
    enabled: row.enabled,
    news_alert_enabled: row.news_alert_enabled,
    price_alert_enabled: row.price_alert_enabled,
    target_scope: row.target_scope,
    min_importance_score: row.min_importance_score,
    min_duplicate_count: row.min_duplicate_count,
    min_source_count: row.min_source_count,
    event_types_json: row.event_types_json,
    keyword_groups_json: row.keyword_groups_json,
    max_daily_alerts: row.max_daily_alerts,
    max_hourly_alerts: row.max_hourly_alerts,
    send_email: row.send_email,
  })
  ElMessage.success('알림 설정을 저장했습니다.')
}

onMounted(loadSettings)
</script>

<style scoped>
.settings-page {
  margin-top: 18px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.kpi-item {
  border: 1px solid var(--border);
  background: var(--surface);
  padding: 16px;
}

.kpi-item span {
  display: block;
  color: var(--text-muted);
  font-size: 12px;
}

.kpi-item strong {
  display: block;
  margin-top: 8px;
  font-size: 22px;
}

.settings-panel {
  padding: 16px;
}

.panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.panel-head p {
  margin: 6px 0 0;
}

.keyword-form {
  display: grid;
  grid-template-columns: 150px minmax(160px, 1fr) 130px auto;
  gap: 10px;
  margin-bottom: 12px;
}

code {
  color: var(--text-muted);
  font-family: Consolas, "Courier New", monospace;
  white-space: pre-wrap;
}

@media (max-width: 900px) {
  .kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .panel-head,
  .keyword-form {
    display: block;
  }

  .keyword-form > * {
    margin-bottom: 8px;
    width: 100%;
  }
}
</style>
