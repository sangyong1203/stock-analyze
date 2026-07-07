<template>
  <section class="collection-page">
    <div class="kpi-grid">
      <article class="kpi-item">
        <span>전체 후보</span>
        <strong>{{ summary?.total_candidate_count ?? 0 }}</strong>
      </article>
      <article class="kpi-item">
        <span>수집 활성</span>
        <strong>{{ summary?.collect_enabled_count ?? 0 }}</strong>
      </article>
      <article class="kpi-item">
        <span>뉴스 수집</span>
        <strong>{{ summary?.collect_news_count ?? 0 }}</strong>
      </article>
      <article class="kpi-item">
        <span>알림 대상</span>
        <strong>{{ summary?.collect_alert_enabled_count ?? 0 }}</strong>
      </article>
      <article class="kpi-item">
        <span>수동 포함</span>
        <strong>{{ summary?.manual_include_count ?? 0 }}</strong>
      </article>
      <article class="kpi-item">
        <span>수동 제외</span>
        <strong>{{ summary?.manual_exclude_count ?? 0 }}</strong>
      </article>
    </div>

    <div class="content-band collection-panel">
      <div class="panel-head">
        <div>
          <h2 class="section-title">수집 종목 관리</h2>
          <p class="muted">KODEX 구성종목, 보유, 관심, 알림, 조건 규칙 기준으로 최종 수집 대상을 관리합니다.</p>
        </div>
        <div class="panel-actions">
          <el-button plain @click="openRulesDialog">수집 조건 규칙</el-button>
          <el-button type="primary" :loading="recalculating" @click="recalculate">재계산</el-button>
        </div>
      </div>

      <div class="toolbar">
        <el-input v-model="filters.keyword" placeholder="종목명, 종목코드, 섹터 검색" clearable @keyup.enter="loadData" />
        <el-select v-model="filters.market" placeholder="시장" clearable>
          <el-option label="KOSPI" value="KOSPI" />
          <el-option label="KOSDAQ" value="KOSDAQ" />
        </el-select>
        <el-select v-model="enabledFilter" placeholder="수집 여부" clearable>
          <el-option label="수집" value="true" />
          <el-option label="제외" value="false" />
        </el-select>
        <el-select v-model="filters.priority" placeholder="우선순위" clearable>
          <el-option label="high" value="high" />
          <el-option label="normal" value="normal" />
          <el-option label="low" value="low" />
        </el-select>
        <el-select v-model="filters.collect_reason" placeholder="수집 사유" clearable>
          <el-option v-for="reason in reasons" :key="reason" :label="reason" :value="reason" />
        </el-select>
        <el-button :loading="loading" @click="loadData">조회</el-button>
      </div>

      <div class="rules-summary">
        <span class="rules-summary-label">활성 규칙</span>
        <strong>{{ enabledRuleCount }}</strong>
        <span class="muted">총 {{ rules.length }}개</span>
      </div>

      <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon :closable="false" />

      <el-table v-loading="loading" :data="stocks" border>
        <el-table-column prop="stock_code" label="코드" width="105" />
        <el-table-column prop="stock_name" label="종목명" min-width="150" />
        <el-table-column prop="market" label="시장" width="100" />
        <el-table-column prop="sector" label="섹터" min-width="130" />
        <el-table-column label="시총" min-width="120" align="right">
          <template #default="{ row }">{{ formatNumber(row.market_cap) }}</template>
        </el-table-column>
        <el-table-column label="보유/관심" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.is_holding_calculated" type="success" effect="plain">보유</el-tag>
            <el-tag v-else-if="row.is_favorite" type="warning" effect="plain">관심</el-tag>
            <span v-else class="muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="수집" width="90">
          <template #default="{ row }">
            <el-switch v-model="row.collect_enabled" @change="saveSetting(row)" />
          </template>
        </el-table-column>
        <el-table-column label="뉴스" width="90">
          <template #default="{ row }">
            <el-switch v-model="row.collect_news" @change="saveSetting(row)" />
          </template>
        </el-table-column>
        <el-table-column label="알림" width="90">
          <template #default="{ row }">
            <el-switch v-model="row.collect_alert_enabled" @change="saveSetting(row)" />
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="우선순위" width="100" />
        <el-table-column prop="collect_reason" label="사유" width="140" />
        <el-table-column label="수동" width="170">
          <template #default="{ row }">
            <el-button link type="primary" @click="includeStock(row)">포함</el-button>
            <el-button link type="danger" @click="excludeStock(row)">제외</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="rulesDialogVisible" title="수집 조건 규칙 설정" width="960px" destroy-on-close>
      <div class="rules-dialog">
        <div class="rules-dialog-list">
          <div class="rules-dialog-toolbar">
            <span class="muted">규칙 목록</span>
            <el-button type="primary" plain @click="startCreateRule">새 규칙</el-button>
          </div>

          <el-table :data="rules" border empty-text="등록된 규칙이 없습니다.">
            <el-table-column prop="name" label="규칙명" min-width="180" />
            <el-table-column prop="rule_type" label="유형" width="140" />
            <el-table-column label="사용" width="90">
              <template #default="{ row }">
                <el-switch v-model="row.enabled" @change="toggleRule(row)" />
              </template>
            </el-table-column>
            <el-table-column prop="priority" label="우선순위" width="100" />
            <el-table-column label="관리" width="140">
              <template #default="{ row }">
                <el-button link type="primary" @click="startEditRule(row)">수정</el-button>
                <el-button link type="danger" @click="removeRule(row)">삭제</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="rules-dialog-form">
          <div class="rules-form-head">
            <h3>{{ editingRuleId ? '규칙 수정' : '규칙 등록' }}</h3>
            <p class="muted">조건은 JSON 형식으로 입력합니다. 예: <code>{"markets":["KOSPI"]}</code></p>
          </div>

          <el-form label-position="top">
            <el-form-item label="규칙명">
              <el-input v-model="ruleForm.name" placeholder="예: KOSPI 대형주" />
            </el-form-item>

            <el-form-item label="유형">
              <el-select v-model="ruleForm.rule_type" placeholder="유형 선택">
                <el-option label="index" value="index" />
                <el-option label="index_member" value="index_member" />
                <el-option label="market_cap" value="market_cap" />
                <el-option label="market" value="market" />
                <el-option label="sector" value="sector" />
              </el-select>
            </el-form-item>

            <el-form-item label="우선순위">
              <el-input-number v-model="ruleForm.priority" :min="1" :max="9999" />
            </el-form-item>

            <el-form-item label="활성화">
              <el-switch v-model="ruleForm.enabled" />
            </el-form-item>

            <el-form-item label="조건 JSON">
              <el-input
                v-model="ruleConditionText"
                type="textarea"
                :rows="10"
                placeholder='예: {"market_cap_min":1000000000000}'
              />
            </el-form-item>
          </el-form>

          <div class="rules-form-actions">
            <el-button @click="resetRuleForm">초기화</el-button>
            <el-button type="primary" :loading="savingRule" @click="submitRule">저장</el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </section>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, onMounted, reactive, ref, watch } from 'vue'

import { collectionApi } from './service/collection.api'
import type { CollectionRule, CollectionStock, CollectionStockSummary } from './service/collection.types'
import { formatNumber } from './service/collection.utils'

const loading = ref(false)
const recalculating = ref(false)
const savingRule = ref(false)
const errorMessage = ref('')
const stocks = ref<CollectionStock[]>([])
const rules = ref<CollectionRule[]>([])
const summary = ref<CollectionStockSummary | null>(null)
const enabledFilter = ref('')
const rulesDialogVisible = ref(false)
const editingRuleId = ref<number | null>(null)
const ruleConditionText = ref('{}')

const reasons = ['manual_exclude', 'manual_include', 'holding', 'favorite', 'alert', 'index_rule', 'market_cap_rule']
const filters = reactive({
  keyword: '',
  market: '',
  priority: '',
  collect_reason: '',
})

const ruleForm = reactive({
  name: '',
  rule_type: 'market',
  enabled: true,
  priority: 100,
})

const enabledRuleCount = computed(() => rules.value.filter((rule) => rule.enabled).length)

async function loadData() {
  loading.value = true
  errorMessage.value = ''
  try {
    const collectEnabled = enabledFilter.value === '' ? undefined : enabledFilter.value === 'true'
    const [stockRows, summaryData, ruleRows] = await Promise.all([
      collectionApi.listStocks({
        keyword: filters.keyword || undefined,
        market: filters.market || undefined,
        priority: filters.priority || undefined,
        collect_reason: filters.collect_reason || undefined,
        collect_enabled: collectEnabled,
      }),
      collectionApi.summary(),
      collectionApi.listRules(),
    ])
    stocks.value = stockRows
    summary.value = summaryData
    rules.value = ruleRows
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '수집 종목 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

function openRulesDialog() {
  rulesDialogVisible.value = true
  if (!editingRuleId.value) {
    resetRuleForm()
  }
}

function resetRuleForm() {
  editingRuleId.value = null
  ruleForm.name = ''
  ruleForm.rule_type = 'market'
  ruleForm.enabled = true
  ruleForm.priority = 100
  ruleConditionText.value = '{}'
}

function startCreateRule() {
  resetRuleForm()
}

function startEditRule(row: CollectionRule) {
  editingRuleId.value = row.id
  ruleForm.name = row.name
  ruleForm.rule_type = row.rule_type
  ruleForm.enabled = row.enabled
  ruleForm.priority = row.priority
  ruleConditionText.value = JSON.stringify(row.condition_json ?? {}, null, 2)
}

async function saveSetting(row: CollectionStock) {
  await collectionApi.updateStock(row.stock_id, {
    collect_enabled: row.collect_enabled,
    collect_news: row.collect_news,
    collect_price_snapshot: row.collect_price_snapshot,
    collect_alert_enabled: row.collect_alert_enabled,
    priority: row.priority,
    collect_reason: row.collect_reason,
  })
  await loadData()
}

async function includeStock(row: CollectionStock) {
  await collectionApi.includeStock(row.stock_id)
  ElMessage.success('수동 포함 처리했습니다.')
  await loadData()
}

async function excludeStock(row: CollectionStock) {
  await collectionApi.excludeStock(row.stock_id)
  ElMessage.success('수동 제외 처리했습니다.')
  await loadData()
}

async function recalculate() {
  recalculating.value = true
  try {
    const result = await collectionApi.recalculate()
    ElMessage.success(`재계산 완료: ${result.collect_enabled_count}개 수집 대상`)
    await loadData()
  } finally {
    recalculating.value = false
  }
}

async function toggleRule(row: CollectionRule) {
  await collectionApi.updateRule(row.id, { enabled: row.enabled })
  ElMessage.success('규칙 상태를 변경했습니다.')
  await loadData()
}

function parseRuleCondition() {
  try {
    return JSON.parse(ruleConditionText.value || '{}') as Record<string, unknown>
  } catch {
    throw new Error('조건 JSON 형식이 올바르지 않습니다.')
  }
}

async function submitRule() {
  if (!ruleForm.name.trim()) {
    ElMessage.error('규칙명을 입력하세요.')
    return
  }

  savingRule.value = true
  try {
    const payload = {
      name: ruleForm.name.trim(),
      rule_type: ruleForm.rule_type,
      enabled: ruleForm.enabled,
      priority: ruleForm.priority,
      condition_json: parseRuleCondition(),
    }

    if (editingRuleId.value) {
      await collectionApi.updateRule(editingRuleId.value, payload)
      ElMessage.success('규칙을 수정했습니다.')
    } else {
      await collectionApi.createRule(payload)
      ElMessage.success('규칙을 등록했습니다.')
    }

    await loadData()
    resetRuleForm()
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '규칙 저장 중 오류가 발생했습니다.')
  } finally {
    savingRule.value = false
  }
}

async function removeRule(row: CollectionRule) {
  await ElMessageBox.confirm(`"${row.name}" 규칙을 삭제할까요?`, '규칙 삭제', {
    confirmButtonText: '삭제',
    cancelButtonText: '취소',
    type: 'warning',
  })

  await collectionApi.deleteRule(row.id)
  ElMessage.success('규칙을 삭제했습니다.')
  if (editingRuleId.value === row.id) {
    resetRuleForm()
  }
  await loadData()
}

watch(() => filters.market, loadData)
watch(() => filters.priority, loadData)
watch(() => filters.collect_reason, loadData)
watch(enabledFilter, loadData)

onMounted(loadData)
</script>

<style scoped>
.collection-page {
  margin-top: 18px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
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

.collection-panel {
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

.panel-actions {
  display: flex;
  gap: 10px;
}

.toolbar {
  display: grid;
  grid-template-columns: minmax(180px, 1fr) 130px 130px 130px 170px auto;
  gap: 10px;
  margin-bottom: 12px;
}

.rules-summary {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  padding: 14px 16px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--surface-muted);
}

.rules-summary-label {
  color: var(--text-muted);
  font-size: 13px;
}

.rules-summary strong {
  font-size: 24px;
}

.rules-dialog {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(320px, 0.95fr);
  gap: 18px;
}

.rules-dialog-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.rules-form-head {
  margin-bottom: 12px;
}

.rules-form-head h3 {
  margin: 0 0 6px;
  font-size: 18px;
}

.rules-form-head p {
  margin: 0;
}

.rules-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

code {
  color: var(--text-muted);
  font-family: Consolas, "Courier New", monospace;
  white-space: pre-wrap;
}

@media (max-width: 1100px) {
  .kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .panel-head,
  .toolbar,
  .panel-actions,
  .rules-dialog {
    display: block;
  }

  .toolbar > *,
  .panel-actions > * {
    margin-bottom: 8px;
    width: 100%;
  }

  .rules-dialog-form {
    margin-top: 16px;
  }
}
</style>
