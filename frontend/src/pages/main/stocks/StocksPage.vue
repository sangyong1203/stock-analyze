<template>
  <section class="stocks-page">
    <div class="kpi-grid">
      <article class="kpi-item">
        <span>표시 종목</span>
        <strong>{{ stocks.length }}</strong>
      </article>
      <article class="kpi-item">
        <span>관심 종목</span>
        <strong>{{ favoriteCount }}</strong>
      </article>
      <article class="kpi-item">
        <span>보유 종목</span>
        <strong>{{ holdingCount }}</strong>
      </article>
      <article class="kpi-item">
        <span>활성 종목</span>
        <strong>{{ activeCount }}</strong>
      </article>
    </div>

    <div class="content-band stocks-panel">
      <div class="panel-head">
        <div>
          <h2 class="section-title">종목 기본정보</h2>
          <p class="muted">종목 코드, 시장, 가격, 시가총액, 관심 여부를 관리합니다.</p>
        </div>
        <div class="panel-actions">
          <el-button :loading="collecting" @click="collectPrices">KRX 가격 수집</el-button>
          <el-button type="primary" @click="openCreate">종목 추가</el-button>
        </div>
      </div>

      <div class="toolbar">
        <el-input v-model="filters.search" placeholder="종목명 또는 코드 검색" clearable @keyup.enter="loadStocks" />
        <el-select v-model="filters.market" placeholder="시장" clearable>
          <el-option label="KOSPI" value="KOSPI" />
          <el-option label="KOSDAQ" value="KOSDAQ" />
        </el-select>
        <el-checkbox v-model="favoriteOnly">관심종목만</el-checkbox>
        <el-button :loading="loading" @click="loadStocks">조회</el-button>
      </div>

      <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon :closable="false" />

      <el-table v-loading="loading" :data="stocks" border>
        <el-table-column prop="code" label="코드" width="110" />
        <el-table-column prop="name" label="종목명" min-width="160" />
        <el-table-column prop="market" label="시장" width="110" />
        <el-table-column prop="sector" label="섹터" min-width="150" />
        <el-table-column label="현재가" width="130" align="right">
          <template #default="{ row }">{{ formatNumber(row.current_price) }}</template>
        </el-table-column>
        <el-table-column label="등락률" width="110" align="right">
          <template #default="{ row }">
            <span :class="Number(row.change_rate ?? 0) < 0 ? 'metric-fall' : 'metric-rise'">
              {{ row.change_rate ?? '-' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="시가총액" width="150" align="right">
          <template #default="{ row }">{{ formatNumber(row.market_cap) }}</template>
        </el-table-column>
        <el-table-column label="보유" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_holding ? 'success' : 'info'" effect="plain">{{ row.is_holding ? '보유' : '미보유' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="관심" width="90">
          <template #default="{ row }">
            <el-button :type="row.is_favorite ? 'danger' : 'default'" link @click="toggleFavorite(row)">
              {{ row.is_favorite ? '해제' : '설정' }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="관리" width="150">
          <template #default="{ row }">
            <el-button link type="primary" @click="openEdit(row)">수정</el-button>
            <el-button link type="danger" :disabled="!row.is_active" @click="deactivateStock(row)">비활성화</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" :title="editingStock ? '종목 수정' : '종목 추가'" width="560px">
      <el-form label-position="top">
        <el-form-item label="종목 코드">
          <el-input v-model="form.code" placeholder="005930" />
        </el-form-item>
        <el-form-item label="종목명">
          <el-input v-model="form.name" placeholder="삼성전자" />
        </el-form-item>
        <div class="form-grid">
          <el-form-item label="시장">
            <el-select v-model="form.market" placeholder="시장" clearable>
              <el-option label="KOSPI" value="KOSPI" />
              <el-option label="KOSDAQ" value="KOSDAQ" />
            </el-select>
          </el-form-item>
          <el-form-item label="섹터">
            <el-input v-model="form.sector" />
          </el-form-item>
        </div>
        <el-form-item label="업종">
          <el-input v-model="form.industry" />
        </el-form-item>
        <div class="form-grid">
          <el-form-item label="현재가">
            <el-input-number v-model="form.current_price" :min="0" controls-position="right" />
          </el-form-item>
          <el-form-item label="시가총액">
            <el-input-number v-model="form.market_cap" :min="0" controls-position="right" />
          </el-form-item>
        </div>
        <el-form-item label="뉴스 매칭 별칭">
          <el-input v-model="aliasText" placeholder="쉼표로 구분" />
        </el-form-item>
        <el-checkbox v-model="form.is_favorite">관심종목</el-checkbox>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">취소</el-button>
        <el-button type="primary" @click="saveStock">저장</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { computed, onMounted, reactive, ref, watch } from 'vue'

import { pricesApi } from './service/prices.api'
import { stocksApi } from './service/stocks.api'
import { stockToPayload } from './service/stocks.mapper'
import type { Stock, StockPayload } from './service/stocks.types'
import { formatNumber, normalizeStockCode, parseAliasText } from './service/stocks.utils'

const loading = ref(false)
const collecting = ref(false)
const errorMessage = ref('')
const stocks = ref<Stock[]>([])
const favoriteOnly = ref(false)
const dialogVisible = ref(false)
const editingStock = ref<Stock | null>(null)
const aliasText = ref('')

const filters = reactive({
  search: '',
  market: '',
})

const form = reactive<StockPayload>({
  code: '',
  name: '',
  market: null,
  sector: null,
  industry: null,
  market_cap: null,
  current_price: null,
  change_rate: null,
  aliases_json: [],
  is_favorite: false,
  is_active: true,
})

const favoriteCount = computed(() => stocks.value.filter((stock) => stock.is_favorite).length)
const holdingCount = computed(() => stocks.value.filter((stock) => stock.is_holding).length)
const activeCount = computed(() => stocks.value.filter((stock) => stock.is_active).length)

async function loadStocks() {
  loading.value = true
  errorMessage.value = ''
  try {
    stocks.value = await stocksApi.list({
      search: filters.search || undefined,
      market: filters.market || undefined,
      is_favorite: favoriteOnly.value ? true : undefined,
      is_active: true,
    })
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '종목 목록을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

function resetForm() {
  Object.assign(form, {
    code: '',
    name: '',
    market: null,
    sector: null,
    industry: null,
    market_cap: null,
    current_price: null,
    change_rate: null,
    aliases_json: [],
    is_favorite: false,
    is_active: true,
  })
  aliasText.value = ''
}

function openCreate() {
  editingStock.value = null
  resetForm()
  dialogVisible.value = true
}

function openEdit(stock: Stock) {
  editingStock.value = stock
  Object.assign(form, stockToPayload(stock))
  aliasText.value = (stock.aliases_json ?? []).join(', ')
  dialogVisible.value = true
}

async function saveStock() {
  if (!form.code.trim() || !form.name.trim()) {
    ElMessage.warning('종목 코드와 종목명을 입력하세요.')
    return
  }

  const payload: StockPayload = {
    ...form,
    code: normalizeStockCode(form.code),
    aliases_json: parseAliasText(aliasText.value),
  }

  if (editingStock.value) {
    await stocksApi.update(editingStock.value.id, payload)
    ElMessage.success('종목이 수정됐습니다.')
  } else {
    await stocksApi.create(payload)
    ElMessage.success('종목이 추가됐습니다.')
  }

  dialogVisible.value = false
  await loadStocks()
}

async function toggleFavorite(stock: Stock) {
  await stocksApi.setFavorite(stock.id, !stock.is_favorite)
  await loadStocks()
}

async function deactivateStock(stock: Stock) {
  await stocksApi.deactivate(stock.id)
  ElMessage.success('종목이 비활성화됐습니다.')
  await loadStocks()
}

function todayText() {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${year}${month}${day}`
}

async function collectPrices() {
  collecting.value = true
  try {
    const result = await pricesApi.collectKrxDaily({
      bas_date: todayText(),
      markets: ['KOSPI', 'KOSDAQ'],
      dry_run: false,
    })
    if (result.error_count > 0) {
      ElMessage.warning(`KRX 가격 수집 오류 ${result.error_count}건: ${result.errors[0] ?? '확인 필요'}`)
    } else {
      ElMessage.success(`KRX 가격 수집 완료: insert ${result.inserted_count}, update ${result.updated_count}`)
    }
    await loadStocks()
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : 'KRX 가격 수집 실패')
  } finally {
    collecting.value = false
  }
}

watch(favoriteOnly, loadStocks)
watch(() => filters.market, loadStocks)

onMounted(loadStocks)
</script>

<style scoped>
.stocks-page {
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

.stocks-panel {
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
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.toolbar {
  display: grid;
  grid-template-columns: minmax(180px, 1fr) 150px 130px auto;
  gap: 10px;
  align-items: center;
  margin-bottom: 12px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

@media (max-width: 900px) {
  .kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .panel-head,
  .toolbar,
  .form-grid {
    display: block;
  }

  .toolbar > *,
  .form-grid > * {
    margin-bottom: 8px;
    width: 100%;
  }
}
</style>
