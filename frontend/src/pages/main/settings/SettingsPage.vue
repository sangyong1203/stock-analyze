<template>
  <section class="settings-page">
    <div class="kpi-grid">
      <article class="kpi-item">
        <span>시스템 설정</span>
        <strong>{{ appSettings.length }}</strong>
      </article>
      <article class="kpi-item">
        <span>작업 수</span>
        <strong>{{ jobSummary?.total_count ?? scheduledJobs.length }}</strong>
      </article>
      <article class="kpi-item">
        <span>활성 작업</span>
        <strong>{{ jobSummary?.enabled_count ?? 0 }}</strong>
      </article>
      <article class="kpi-item">
        <span>실패 작업</span>
        <strong>{{ jobSummary?.failed_count ?? 0 }}</strong>
      </article>
    </div>

    <div class="content-band settings-panel">
      <div class="panel-head">
        <div>
          <h2 class="section-title">시스템 설정</h2>
          <p class="muted">수집, 알림, 키워드, 수동 실행 작업 상태를 관리합니다.</p>
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

        <el-tab-pane label="수동 작업" name="jobs">
          <div class="jobs-summary" v-if="jobSummary">
            <el-tag type="info" effect="plain">전체 {{ jobSummary.total_count }}</el-tag>
            <el-tag type="success" effect="plain">성공 {{ jobSummary.success_count }}</el-tag>
            <el-tag type="danger" effect="plain">실패 {{ jobSummary.failed_count }}</el-tag>
            <el-tag effect="plain">미실행 {{ jobSummary.never_run_count }}</el-tag>
          </div>

          <el-table :data="scheduledJobs" border>
            <el-table-column prop="job_key" label="작업 키" min-width="170" />
            <el-table-column prop="job_name" label="작업명" min-width="180" />
            <el-table-column label="사용" width="90">
              <template #default="{ row }">
                <el-switch v-model="row.enabled" @change="saveScheduledJob(row)" />
              </template>
            </el-table-column>
            <el-table-column prop="schedule_type" label="유형" width="100" />
            <el-table-column label="최근 상태" width="110">
              <template #default="{ row }">
                <el-tag :type="statusTagType(row.last_status)" effect="plain">{{ row.last_status || 'never' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="최근 실행" min-width="150">
              <template #default="{ row }">{{ formatDateTime(row.last_run_at) }}</template>
            </el-table-column>
            <el-table-column label="메시지" min-width="220" show-overflow-tooltip>
              <template #default="{ row }">{{ row.last_message || '-' }}</template>
            </el-table-column>
            <el-table-column label="설정 JSON" min-width="240">
              <template #default="{ row }">
                <code>{{ prettyConfig(row.config_json) }}</code>
              </template>
            </el-table-column>
            <el-table-column label="실행" width="170" fixed="right">
              <template #default="{ row }">
                <div class="action-row">
                  <el-button size="small" :loading="runningJobId === row.id" @click="runJob(row, true)">dry-run</el-button>
                  <el-button size="small" type="primary" :loading="runningJobId === row.id" @click="runJob(row, false)">실행</el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>

          <div v-if="jobSummary?.recent_runs.length" class="recent-runs">
            <h3>최근 실행 결과</h3>
            <el-table :data="jobSummary?.recent_runs ?? []" size="small" border>
              <el-table-column prop="job_key" label="작업" min-width="150" />
              <el-table-column prop="status" label="상태" width="100" />
              <el-table-column label="시작" min-width="150">
                <template #default="{ row }">{{ formatDateTime(row.started_at) }}</template>
              </el-table-column>
              <el-table-column label="종료" min-width="150">
                <template #default="{ row }">{{ formatDateTime(row.finished_at) }}</template>
              </el-table-column>
              <el-table-column prop="message" label="메시지" min-width="240" show-overflow-tooltip />
            </el-table>
          </div>
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
import type { AlertSetting, AppSetting, JobSummary, NewsKeyword, ScheduledJob } from './service/settings.types'

const activeTab = ref('app')
const loading = ref(false)
const errorMessage = ref('')
const runningJobId = ref<number | null>(null)
const appSettings = ref<AppSetting[]>([])
const scheduledJobs = ref<ScheduledJob[]>([])
const newsKeywords = ref<NewsKeyword[]>([])
const alertSettings = ref<AlertSetting[]>([])
const jobSummary = ref<JobSummary | null>(null)

const keywordGroups = ['market', 'sector', 'macro', 'policy', 'exclude', 'event']
const keywordDraft = reactive({
  group_type: 'market',
  keyword: '',
  weight: 1,
  enabled: true,
  is_default: false,
})

function formatDateTime(value: string | null | undefined) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString('ko-KR')
}

function prettyConfig(value: Record<string, unknown> | null | undefined) {
  return JSON.stringify(value ?? {}, null, 2)
}

function statusTagType(status: string | null | undefined) {
  if (status === 'success') return 'success'
  if (status === 'failed') return 'danger'
  return 'info'
}

async function loadSettings() {
  loading.value = true
  errorMessage.value = ''
  try {
    const [app, jobs, keywords, alerts, jobsSummary] = await Promise.all([
      settingsApi.listAppSettings(),
      settingsApi.listJobs(),
      settingsApi.listNewsKeywords(),
      settingsApi.listAlertSettings(),
      settingsApi.jobSummary(),
    ])
    appSettings.value = app
    scheduledJobs.value = jobs
    newsKeywords.value = keywords
    alertSettings.value = alerts
    jobSummary.value = jobsSummary
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
  ElMessage.success('작업 설정을 저장했습니다.')
}

async function runJob(row: ScheduledJob, dryRun: boolean) {
  runningJobId.value = row.id
  try {
    const result = await settingsApi.runJob(row.id, { dry_run: dryRun })
    ElMessage.success(`${result.job_key}: ${result.message}`)
    await loadSettings()
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '작업 실행에 실패했습니다.')
  } finally {
    runningJobId.value = null
  }
}

async function createKeyword() {
  if (!keywordDraft.keyword.trim()) {
    ElMessage.warning('키워드를 입력해 주세요.')
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

.jobs-summary {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.recent-runs {
  margin-top: 16px;
}

.recent-runs h3 {
  margin: 0 0 10px;
  font-size: 15px;
}

.keyword-form {
  display: grid;
  grid-template-columns: 150px minmax(160px, 1fr) 130px auto;
  gap: 10px;
  margin-bottom: 12px;
}

.action-row {
  display: flex;
  gap: 6px;
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
