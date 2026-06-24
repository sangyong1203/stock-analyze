<template>
  <section class="alerts-page">
    <div class="kpi-grid">
      <article class="kpi-item">
        <span>알림 후보</span>
        <strong>{{ candidateSummary?.alert_target_count ?? 0 }}</strong>
      </article>
      <article class="kpi-item">
        <span>오늘 발송</span>
        <strong>{{ historySummary?.today_sent_count ?? 0 }}</strong>
      </article>
      <article class="kpi-item">
        <span>최근 1시간</span>
        <strong>{{ historySummary?.hourly_sent_count ?? 0 }}</strong>
      </article>
      <article class="kpi-item">
        <span>실패 이력</span>
        <strong>{{ historySummary?.failed_count ?? 0 }}</strong>
      </article>
    </div>

    <div class="content-band alert-panel">
      <div class="panel-head">
        <div>
          <h2 class="section-title">뉴스 알림 발송</h2>
          <p class="muted">Gmail SMTP 발송 전 dry-run으로 대상과 제한 적용 결과를 확인합니다.</p>
        </div>
        <div class="actions">
          <el-input-number v-model="sendForm.limit" :min="1" :max="100" size="small" />
          <el-switch v-model="sendForm.force" active-text="failed 재시도" />
          <el-button :loading="loading" @click="dryRun">dry-run</el-button>
          <el-button type="danger" :loading="sending" @click="confirmSend">실제 발송</el-button>
        </div>
      </div>

      <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon :closable="false" />
      <el-alert
        v-if="lastResult"
        class="result-alert"
        :title="`대상 ${lastResult.candidate_count}, 발송 가능 ${lastResult.sendable_count}, 스킵 ${lastResult.skipped_count}, 성공 ${lastResult.sent_count}, 실패 ${lastResult.failed_count}`"
        type="info"
        show-icon
        :closable="false"
      />

      <div v-if="lastResult" class="result-grid">
        <article>
          <span>일별 발송</span>
          <strong>{{ lastResult.daily_sent_count }}</strong>
        </article>
        <article>
          <span>시간별 발송</span>
          <strong>{{ lastResult.hourly_sent_count }}</strong>
        </article>
        <article>
          <span>스킵 사유</span>
          <code>{{ lastResult.skipped_reasons }}</code>
        </article>
      </div>

      <el-table v-if="lastResult?.would_send_items.length" :data="lastResult.would_send_items" border>
        <el-table-column prop="news_id" label="뉴스 ID" width="90" />
        <el-table-column prop="stock_id" label="종목 ID" width="90" />
        <el-table-column prop="title" label="dry-run 대상" min-width="260" show-overflow-tooltip />
        <el-table-column prop="recipient_email" label="수신자" min-width="180" />
      </el-table>
    </div>

    <div class="content-band alert-panel">
      <div class="panel-head">
        <div>
          <h2 class="section-title">발송 이력</h2>
          <p class="muted">성공/실패 이력과 실패 사유를 확인합니다.</p>
        </div>
        <div class="actions">
          <el-select v-model="statusFilter" placeholder="상태" clearable>
            <el-option label="sent" value="sent" />
            <el-option label="failed" value="failed" />
            <el-option label="skipped" value="skipped" />
          </el-select>
          <el-button :loading="loading" @click="loadData">조회</el-button>
        </div>
      </div>

      <el-table v-loading="loading" :data="histories" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="status" label="상태" width="100" />
        <el-table-column prop="news_id" label="뉴스" width="90" />
        <el-table-column prop="stock_id" label="종목" width="90" />
        <el-table-column prop="title" label="제목" min-width="260" show-overflow-tooltip />
        <el-table-column prop="recipient_email" label="수신자" min-width="170" />
        <el-table-column label="발송시각" width="150">
          <template #default="{ row }">{{ formatDateTime(row.sent_at) }}</template>
        </el-table-column>
        <el-table-column prop="error_message" label="실패 사유" min-width="220" show-overflow-tooltip />
      </el-table>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from 'element-plus'
import { onMounted, reactive, ref, watch } from 'vue'

import { alertsApi } from './service/alerts.api'
import type { AlertCandidateSummary, AlertHistory, AlertHistorySummary, AlertSendResult } from './service/alerts.types'

const loading = ref(false)
const sending = ref(false)
const errorMessage = ref('')
const statusFilter = ref('')
const histories = ref<AlertHistory[]>([])
const historySummary = ref<AlertHistorySummary | null>(null)
const candidateSummary = ref<AlertCandidateSummary | null>(null)
const lastResult = ref<AlertSendResult | null>(null)

const sendForm = reactive({
  limit: 20,
  force: false,
})

function formatDateTime(value?: string | null) {
  if (!value) return '-'
  return new Intl.DateTimeFormat('ko-KR', {
    year: '2-digit',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

async function loadData() {
  loading.value = true
  errorMessage.value = ''
  try {
    const [rows, summary, candidates] = await Promise.all([
      alertsApi.histories(statusFilter.value || undefined),
      alertsApi.historiesSummary(),
      alertsApi.candidateSummary(),
    ])
    histories.value = rows
    historySummary.value = summary
    candidateSummary.value = candidates
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '알림 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

async function dryRun() {
  loading.value = true
  try {
    lastResult.value = await alertsApi.dryRunSend({ limit: sendForm.limit, force: sendForm.force })
    ElMessage.success(`dry-run 완료: 발송 가능 ${lastResult.value.sendable_count}건`)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'dry-run에 실패했습니다.'
  } finally {
    loading.value = false
  }
}

async function confirmSend() {
  try {
    await ElMessageBox.confirm('실제 Gmail 발송을 진행할까요? 발송 제한과 중복 방지는 적용됩니다.', '뉴스 알림 실제 발송', {
      confirmButtonText: '발송',
      cancelButtonText: '취소',
      type: 'warning',
    })
  } catch {
    return
  }
  sending.value = true
  try {
    lastResult.value = await alertsApi.send({ limit: sendForm.limit, force: sendForm.force })
    ElMessage.success(`발송 완료: 성공 ${lastResult.value.sent_count}, 실패 ${lastResult.value.failed_count}`)
    await loadData()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '실제 발송에 실패했습니다.'
  } finally {
    sending.value = false
  }
}

watch(statusFilter, loadData)
onMounted(loadData)
</script>

<style scoped>
.alerts-page {
  margin-top: 18px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.kpi-item,
.result-grid article {
  border: 1px solid var(--border);
  background: var(--surface);
  padding: 16px;
}

.kpi-item span,
.result-grid span {
  display: block;
  color: var(--text-muted);
  font-size: 12px;
}

.kpi-item strong,
.result-grid strong {
  display: block;
  margin-top: 8px;
  font-size: 22px;
}

.alert-panel {
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

.actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.result-alert {
  margin: 12px 0;
}

.result-grid {
  display: grid;
  grid-template-columns: 140px 140px minmax(0, 1fr);
  gap: 10px;
  margin: 12px 0;
}

code {
  color: var(--text-muted);
  font-family: Consolas, "Courier New", monospace;
  white-space: pre-wrap;
}

@media (max-width: 900px) {
  .kpi-grid,
  .result-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .panel-head,
  .actions {
    display: block;
  }

  .actions > * {
    margin-bottom: 8px;
    width: 100%;
  }
}
</style>
