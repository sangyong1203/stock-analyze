<template>
  <section class="alerts-page">
    <div class="kpi-grid">
      <article class="kpi-item">
        <span>전체 알림</span>
        <strong>{{ summary?.total_count ?? 0 }}</strong>
      </article>
      <article class="kpi-item">
        <span>활성 알림</span>
        <strong>{{ summary?.enabled_count ?? 0 }}</strong>
      </article>
      <article class="kpi-item">
        <span>오늘 발송</span>
        <strong>{{ summary?.today_sent_count ?? 0 }}</strong>
      </article>
      <article class="kpi-item">
        <span>최근 1시간 발송</span>
        <strong>{{ summary?.hourly_sent_count ?? 0 }}</strong>
      </article>
    </div>

    <div class="content-band alerts-layout">
      <section class="panel-card">
        <div class="panel-head">
          <div>
            <h2 class="section-title">{{ editingAlertId ? '가격 알림 수정' : '가격 알림 추가' }}</h2>
            <p class="muted">종목, 조건, 기준값을 등록하고 dry-run 또는 실제 발송을 실행합니다.</p>
          </div>
        </div>

        <el-form label-position="top" @submit.prevent>
          <el-form-item label="종목">
            <el-select
              v-model="form.stock_id"
              filterable
              remote
              reserve-keyword
              placeholder="종목명 또는 코드 검색"
              :remote-method="searchStocks"
              :loading="stockSearching"
            >
              <el-option
                v-for="stock in stockOptions"
                :key="stock.id"
                :label="`${stock.name} (${stock.code})`"
                :value="stock.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="알림 조건">
            <el-select v-model="form.alert_type">
              <el-option
                v-for="option in ALERT_TYPE_OPTIONS"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </el-form-item>

          <div class="field-grid">
            <el-form-item label="목표가" :class="{ mutedField: isRangeAlert }">
              <el-input-number v-model="form.target_price" :min="0" :disabled="isRangeAlert" />
            </el-form-item>
            <el-form-item label="변동률(%)" :class="{ mutedField: !isRangeAlert }">
              <el-input-number v-model="form.threshold_percent" :min="0" :step="0.5" :disabled="!isRangeAlert" />
            </el-form-item>
          </div>

          <el-alert
            v-if="isRangeAlert"
            class="criteria-alert"
            type="info"
            :closable="false"
            show-icon
            title="최근 60일 기준으로 최근 고점/저점을 계산합니다."
          />

          <el-form-item label="활성 여부">
            <el-switch v-model="form.is_enabled" />
          </el-form-item>

          <el-form-item label="메모">
            <el-input v-model="form.memo" type="textarea" :rows="3" />
          </el-form-item>

          <div class="actions">
            <el-button @click="resetForm">초기화</el-button>
            <el-button type="primary" :loading="saving" @click="saveAlert">
              {{ editingAlertId ? '수정 저장' : '알림 생성' }}
            </el-button>
          </div>
        </el-form>
      </section>

      <section class="panel-card">
        <div class="panel-head">
          <div>
            <h2 class="section-title">평가 실행</h2>
            <p class="muted">조건 충족 여부를 확인하고 Gmail 발송 결과와 skip 사유를 검증합니다.</p>
          </div>
          <div class="actions">
            <el-input-number v-model="evaluationForm.limit" :min="1" :max="100" size="small" />
            <el-switch v-model="evaluationForm.force" active-text="failed 재시도" />
            <el-button :loading="loading" @click="runDryRun">dry-run</el-button>
            <el-button type="danger" :loading="sending" @click="runEvaluate">실제 발송</el-button>
          </div>
        </div>

        <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon :closable="false" />
        <el-alert
          v-if="evaluationResult"
          class="result-alert"
          type="info"
          show-icon
          :closable="false"
          :title="`평가 ${evaluationResult.evaluated_count}, 조건 충족 ${evaluationResult.matched_count}, 발송 가능 ${evaluationResult.sendable_count}, sent ${evaluationResult.sent_count}, failed ${evaluationResult.failed_count}, skipped ${evaluationResult.skipped_count}`"
        />

        <div v-if="evaluationResult" class="result-grid">
          <article>
            <span>일일 발송 수</span>
            <strong>{{ evaluationResult.daily_sent_count }}</strong>
          </article>
          <article>
            <span>시간당 발송 수</span>
            <strong>{{ evaluationResult.hourly_sent_count }}</strong>
          </article>
          <article>
            <span>skip 사유</span>
            <strong>{{ formatSkippedReasons(evaluationResult.skipped_reasons) }}</strong>
          </article>
        </div>

        <el-table v-if="evaluationResult" :data="evaluationResult.items" border>
          <el-table-column prop="stock_code" label="코드" width="90" />
          <el-table-column prop="stock_name" label="종목" min-width="130" />
          <el-table-column prop="alert_type" label="조건" width="180" />
          <el-table-column label="현재가" width="110" align="right">
            <template #default="{ row }">{{ formatNumber(row.current_price) }}</template>
          </el-table-column>
          <el-table-column label="트리거가" width="110" align="right">
            <template #default="{ row }">{{ formatNumber(row.trigger_price) }}</template>
          </el-table-column>
          <el-table-column prop="status" label="상태" width="110" />
          <el-table-column prop="skip_reason" label="skip 사유" min-width="150" />
          <el-table-column prop="reason" label="오류" min-width="180" show-overflow-tooltip />
        </el-table>
      </section>
    </div>

    <div class="content-band panel-card">
      <div class="panel-head">
        <div>
          <h2 class="section-title">가격 알림 목록</h2>
          <p class="muted">목표가, 변동률, 최근 60일 기준 여부, 최근 트리거 상태를 확인합니다.</p>
        </div>
        <el-button :loading="loading" @click="loadData">새로고침</el-button>
      </div>

      <el-table v-loading="loading" :data="alerts" border>
        <el-table-column prop="stock_code" label="코드" width="90" />
        <el-table-column prop="stock_name" label="종목" min-width="140" />
        <el-table-column prop="alert_type" label="조건" width="180" />
        <el-table-column label="목표가" width="110" align="right">
          <template #default="{ row }">{{ formatNumber(row.target_price) }}</template>
        </el-table-column>
        <el-table-column label="변동률" width="90" align="right">
          <template #default="{ row }">{{ row.threshold_percent ?? '-' }}</template>
        </el-table-column>
        <el-table-column label="기준" width="140">
          <template #default="{ row }">
            {{ row.alert_type === 'DROP_FROM_HIGH' || row.alert_type === 'RISE_FROM_LOW' ? '최근 60일 기준' : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="활성" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_enabled ? 'success' : 'info'" effect="plain">
              {{ row.is_enabled ? '활성' : '비활성' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="트리거" width="90">
          <template #default="{ row }">
            <el-tag :type="row.triggered ? 'danger' : 'info'" effect="plain">
              {{ row.triggered ? '감지' : '대기' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="최근 감지 시각" width="150">
          <template #default="{ row }">{{ formatDateTime(row.triggered_at) }}</template>
        </el-table-column>
        <el-table-column label="관리" width="170">
          <template #default="{ row }">
            <el-button link type="primary" @click="editAlert(row)">수정</el-button>
            <el-button link @click="runSingleDryRun(row.id)">개별 dry-run</el-button>
            <el-button link type="danger" @click="removeAlert(row.id)">삭제</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="content-band panel-card">
      <div class="panel-head">
        <div>
          <h2 class="section-title">발송 이력</h2>
          <p class="muted">sent, failed, skipped 이력을 확인합니다.</p>
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
        <el-table-column prop="price_alert_id" label="알림 ID" width="90" />
        <el-table-column prop="stock_id" label="종목 ID" width="90" />
        <el-table-column prop="status" label="상태" width="100" />
        <el-table-column prop="title" label="제목" min-width="220" show-overflow-tooltip />
        <el-table-column prop="recipient_email" label="수신자" min-width="180" />
        <el-table-column label="발송 시각" width="150">
          <template #default="{ row }">{{ formatDateTime(row.sent_at) }}</template>
        </el-table-column>
        <el-table-column prop="error_message" label="오류/skip" min-width="200" show-overflow-tooltip />
      </el-table>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, onMounted, reactive, ref, watch } from 'vue'

import { ALERT_TYPE_OPTIONS } from './service/alerts.constants'
import { alertsApi } from './service/alerts.api'
import { alertToPayload } from './service/alerts.mapper'
import type {
  AlertHistory,
  PriceAlert,
  PriceAlertEvaluationResult,
  PriceAlertPayload,
  PriceAlertSummary,
  StockOption,
} from './service/alerts.types'
import { formatDateTime, formatNumber, formatSkippedReasons } from './service/alerts.utils'

const loading = ref(false)
const saving = ref(false)
const sending = ref(false)
const stockSearching = ref(false)
const errorMessage = ref('')
const statusFilter = ref('')
const editingAlertId = ref<number | null>(null)

const summary = ref<PriceAlertSummary | null>(null)
const alerts = ref<PriceAlert[]>([])
const histories = ref<AlertHistory[]>([])
const stockOptions = ref<StockOption[]>([])
const evaluationResult = ref<PriceAlertEvaluationResult | null>(null)

const form = reactive<PriceAlertPayload>({
  stock_id: null,
  alert_type: 'TARGET_PRICE_ABOVE',
  target_price: null,
  threshold_percent: null,
  is_enabled: true,
  memo: '',
})

const evaluationForm = reactive({
  limit: 20,
  force: false,
})

const isRangeAlert = computed(() => form.alert_type === 'DROP_FROM_HIGH' || form.alert_type === 'RISE_FROM_LOW')

function resetForm() {
  editingAlertId.value = null
  Object.assign(form, {
    stock_id: null,
    alert_type: 'TARGET_PRICE_ABOVE',
    target_price: null,
    threshold_percent: null,
    is_enabled: true,
    memo: '',
  })
}

async function searchStocks(query: string) {
  if (!query.trim()) {
    stockOptions.value = []
    return
  }
  stockSearching.value = true
  try {
    stockOptions.value = await alertsApi.searchStocks(query)
  } finally {
    stockSearching.value = false
  }
}

async function loadData() {
  loading.value = true
  errorMessage.value = ''
  try {
    const [alertRows, summaryRow, historyRows] = await Promise.all([
      alertsApi.list(),
      alertsApi.summary(),
      alertsApi.histories(statusFilter.value || undefined),
    ])
    alerts.value = alertRows
    summary.value = summaryRow
    histories.value = historyRows
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '가격 알림 데이터를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

function validateForm() {
  if (!form.stock_id) {
    ElMessage.warning('종목을 선택해 주세요.')
    return false
  }
  if (isRangeAlert.value) {
    if (form.threshold_percent == null || form.threshold_percent <= 0) {
      ElMessage.warning('변동률(%)을 입력해 주세요.')
      return false
    }
  } else if (form.target_price == null || form.target_price <= 0) {
    ElMessage.warning('목표가를 입력해 주세요.')
    return false
  }
  return true
}

async function saveAlert() {
  if (!validateForm()) return
  saving.value = true
  errorMessage.value = ''
  try {
    if (editingAlertId.value) {
      await alertsApi.update(editingAlertId.value, form)
      ElMessage.success('가격 알림을 수정했습니다.')
    } else {
      await alertsApi.create(form)
      ElMessage.success('가격 알림을 생성했습니다.')
    }
    resetForm()
    await loadData()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '가격 알림 저장에 실패했습니다.'
  } finally {
    saving.value = false
  }
}

function editAlert(alert: PriceAlert) {
  editingAlertId.value = alert.id
  Object.assign(form, alertToPayload(alert))
  stockOptions.value = [
    {
      id: alert.stock_id,
      code: alert.stock_code,
      name: alert.stock_name,
      current_price: alert.current_price,
    },
  ]
}

async function removeAlert(alertId: number) {
  try {
    await ElMessageBox.confirm('가격 알림을 삭제할까요?', '가격 알림 삭제', {
      confirmButtonText: '삭제',
      cancelButtonText: '취소',
      type: 'warning',
    })
  } catch {
    return
  }
  try {
    await alertsApi.remove(alertId)
    ElMessage.success('가격 알림을 삭제했습니다.')
    if (editingAlertId.value === alertId) resetForm()
    await loadData()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '가격 알림 삭제에 실패했습니다.'
  }
}

async function runDryRun() {
  loading.value = true
  errorMessage.value = ''
  try {
    evaluationResult.value = await alertsApi.dryRun({
      limit: evaluationForm.limit,
      force: evaluationForm.force,
    })
    ElMessage.success(`dry-run 완료: 발송 가능 ${evaluationResult.value.sendable_count}건`)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'dry-run 실행에 실패했습니다.'
  } finally {
    loading.value = false
  }
}

async function runSingleDryRun(alertId: number) {
  loading.value = true
  errorMessage.value = ''
  try {
    evaluationResult.value = await alertsApi.dryRun({
      alert_ids: [alertId],
      limit: 1,
      force: evaluationForm.force,
    })
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '개별 dry-run 실행에 실패했습니다.'
  } finally {
    loading.value = false
  }
}

async function runEvaluate() {
  try {
    await ElMessageBox.confirm('실제 Gmail 발송을 실행할까요?', '가격 알림 발송', {
      confirmButtonText: '발송',
      cancelButtonText: '취소',
      type: 'warning',
    })
  } catch {
    return
  }
  sending.value = true
  errorMessage.value = ''
  try {
    evaluationResult.value = await alertsApi.evaluate({
      limit: evaluationForm.limit,
      force: evaluationForm.force,
    })
    ElMessage.success(`발송 완료: sent ${evaluationResult.value.sent_count}, failed ${evaluationResult.value.failed_count}`)
    await loadData()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '가격 알림 발송에 실패했습니다.'
  } finally {
    sending.value = false
  }
}

watch(statusFilter, loadData)
watch(
  () => form.alert_type,
  (value) => {
    if (value === 'DROP_FROM_HIGH' || value === 'RISE_FROM_LOW') {
      form.target_price = null
    } else {
      form.threshold_percent = null
    }
  },
)

onMounted(loadData)
</script>

<style scoped>
.alerts-page {
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.kpi-item {
  padding: 16px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.82);
}

.kpi-item span {
  display: block;
  color: #64748b;
  font-size: 12px;
  font-weight: 700;
}

.kpi-item strong {
  display: block;
  margin-top: 10px;
  color: #0f172a;
  font-size: 22px;
}

.alerts-layout {
  display: grid;
  grid-template-columns: minmax(320px, 360px) minmax(0, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.panel-card {
  padding: 16px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.82);
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

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.result-alert {
  margin-bottom: 12px;
}

.criteria-alert {
  margin-bottom: 16px;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 12px;
}

.result-grid article {
  padding: 14px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 12px;
  background: rgba(248, 250, 252, 0.9);
}

.result-grid span {
  display: block;
  color: #64748b;
  font-size: 12px;
}

.result-grid strong {
  display: block;
  margin-top: 8px;
  color: #0f172a;
}

.mutedField :deep(.el-form-item__label) {
  color: #94a3b8;
}

@media (max-width: 1100px) {
  .alerts-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .kpi-grid,
  .field-grid,
  .result-grid {
    grid-template-columns: 1fr;
  }

  .panel-head,
  .actions {
    display: block;
  }

  .actions > * {
    width: 100%;
    margin-bottom: 8px;
  }
}
</style>
