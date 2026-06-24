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
          <p class="muted">KODEX 구성종목, 보유, 관심, 알림, 조건 규칙 기준으로 최종 수집 대상을 산출합니다.</p>
        </div>
        <el-button type="primary" :loading="recalculating" @click="recalculate">재계산</el-button>
      </div>

      <div class="toolbar">
        <el-input v-model="filters.keyword" placeholder="종목명/코드/섹터 검색" clearable @keyup.enter="loadData" />
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

      <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon :closable="false" />

      <el-table v-loading="loading" :data="stocks" border>
        <el-table-column prop="stock_code" label="코드" width="105" />
        <el-table-column prop="stock_name" label="종목명" min-width="150" />
        <el-table-column prop="market" label="시장" width="100" />
        <el-table-column prop="sector" label="섹터" min-width="130" />
        <el-table-column label="시총" width="120" align="right">
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

    <div class="content-band rules-panel">
      <div class="panel-head">
        <div>
          <h2 class="section-title">수집 조건 규칙</h2>
          <p class="muted">활성 규칙은 재계산 시 조건 규칙 단계에서 적용됩니다.</p>
        </div>
      </div>

      <el-table :data="rules" border>
        <el-table-column prop="name" label="규칙명" min-width="160" />
        <el-table-column prop="rule_type" label="유형" width="130" />
        <el-table-column label="사용" width="90">
          <template #default="{ row }">
            <el-switch v-model="row.enabled" @change="saveRule(row)" />
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="우선순위" width="100" />
        <el-table-column label="조건" min-width="260">
          <template #default="{ row }">
            <code>{{ row.condition_json ?? {} }}</code>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { onMounted, reactive, ref, watch } from 'vue'

import { collectionApi } from './service/collection.api'
import type { CollectionRule, CollectionStock, CollectionStockSummary } from './service/collection.types'
import { formatNumber } from './service/collection.utils'

const loading = ref(false)
const recalculating = ref(false)
const errorMessage = ref('')
const stocks = ref<CollectionStock[]>([])
const rules = ref<CollectionRule[]>([])
const summary = ref<CollectionStockSummary | null>(null)
const enabledFilter = ref('')

const reasons = ['manual_exclude', 'manual_include', 'holding', 'favorite', 'alert', 'index_rule', 'market_cap_rule']
const filters = reactive({
  keyword: '',
  market: '',
  priority: '',
  collect_reason: '',
})

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

async function saveRule(row: CollectionRule) {
  await collectionApi.updateRule(row.id, { enabled: row.enabled })
  ElMessage.success('규칙을 저장했습니다.')
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

.collection-panel,
.rules-panel {
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

.toolbar {
  display: grid;
  grid-template-columns: minmax(180px, 1fr) 130px 130px 130px 170px auto;
  gap: 10px;
  margin-bottom: 12px;
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
  .toolbar {
    display: block;
  }

  .toolbar > * {
    margin-bottom: 8px;
    width: 100%;
  }
}
</style>
