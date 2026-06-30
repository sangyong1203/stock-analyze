<template>
  <section class="charts-page">
    <div class="content-band chart-panel">
      <div class="panel-head">
        <div>
          <h2 class="section-title">가격 차트</h2>
          <p class="muted">KRX OHLCV와 MA, RSI, MACD를 기간별로 확인합니다.</p>
        </div>
        <el-button :loading="loading" type="primary" @click="loadChart">조회</el-button>
      </div>

      <div class="control-grid">
        <div class="control-card search-card">
          <label>종목 검색</label>
          <el-select
            v-model="selectedStockId"
            filterable
            remote
            reserve-keyword
            :remote-method="searchStocks"
            :loading="stockLoading"
            placeholder="종목명 또는 종목코드 입력"
            @change="loadChart"
          >
            <el-option v-for="stock in stocks" :key="stock.id" :label="stockOptionLabel(stock)" :value="stock.id">
              <div class="stock-option">
                <span>{{ stock.name }}</span>
                <small>{{ stock.code }} · {{ stock.market || '-' }}</small>
              </div>
            </el-option>
          </el-select>
          <div v-if="selectedStock" class="selected-stock">
            <el-tag size="small" effect="dark">{{ selectedStock.market || '-' }}</el-tag>
            <strong>{{ selectedStock.name }}</strong>
            <span>{{ selectedStock.code }}</span>
          </div>
        </div>

        <div class="control-card">
          <label>시장</label>
          <el-segmented v-model="marketFilter" :options="marketOptions" @change="handleMarketChange" />
        </div>

        <div class="control-card period-card">
          <label>조회 기간</label>
          <el-segmented v-model="periodKey" :options="periodOptions" @change="handlePeriodChange" />
          <el-date-picker
            v-if="periodKey === 'custom'"
            v-model="customRange"
            type="daterange"
            range-separator="~"
            start-placeholder="시작일"
            end-placeholder="종료일"
            value-format="YYYY-MM-DD"
            @change="loadChart"
          />
        </div>
      </div>

      <div class="indicator-options">
        <span>지표 표시</span>
        <el-checkbox v-model="showMa20">MA20</el-checkbox>
        <el-checkbox v-model="showMa60">MA60</el-checkbox>
        <el-checkbox v-model="showMa120">MA120</el-checkbox>
        <el-divider direction="vertical" />
        <el-checkbox v-model="showRsi">RSI</el-checkbox>
        <el-checkbox v-model="showMacd">MACD</el-checkbox>
      </div>

      <div class="status-row">
        <el-tag v-if="chartItems.length" type="info" effect="plain">데이터 {{ chartItems.length }}건</el-tag>
        <el-tag v-if="chartDateRange" type="info" effect="plain">{{ chartDateRange }}</el-tag>
        <el-tag v-if="selectedStock" type="success" effect="plain">{{ selectedStock.name }} · {{ selectedStock.code }}</el-tag>
      </div>

      <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon :closable="false" />
      <el-empty v-else-if="!loading && chartItems.length === 0" description="가격 데이터가 없습니다. 종목 또는 조회 기간을 변경해 주세요." />

      <div v-loading="loading" class="chart-box">
        <svg v-if="chartItems.length" viewBox="0 0 1000 660" role="img" aria-label="가격 차트">
          <rect width="1000" height="660" rx="18" class="chart-bg" />
          <g v-for="line in gridLines" :key="line" class="grid-line">
            <line x1="48" :y1="line" x2="976" :y2="line" />
          </g>

          <polyline v-for="line in visiblePriceLines" :key="line.name" :points="line.points" :stroke="line.color" class="chart-line" />

          <g class="volume-bars">
            <rect
              v-for="bar in volumeBars"
              :key="bar.key"
              :x="bar.x"
              :y="bar.y"
              :width="bar.width"
              :height="bar.height"
              rx="1"
            />
          </g>

          <polyline v-if="showRsi" :points="rsiLine" stroke="#0f766e" class="chart-line sub-line" />

          <g v-if="showMacd" class="macd-bars">
            <rect
              v-for="bar in macdBars"
              :key="bar.key"
              :x="bar.x"
              :y="bar.y"
              :width="bar.width"
              :height="bar.height"
              rx="1"
              :class="{ negative: bar.negative }"
            />
          </g>
          <polyline v-if="showMacd" :points="macdLine" stroke="#dc2626" class="chart-line sub-line" />
          <polyline v-if="showMacd" :points="signalLine" stroke="#2563eb" class="chart-line sub-line" />

          <text x="54" y="34" class="axis-label">Close / MA</text>
          <text x="54" y="438" class="axis-label">Volume</text>
          <text x="54" y="515" class="axis-label">RSI</text>
          <text x="54" y="595" class="axis-label">MACD</text>
          <text x="54" y="646" class="date-label">{{ firstDate }}</text>
          <text x="900" y="646" class="date-label">{{ lastDate }}</text>
        </svg>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { stocksApi } from '@/pages/main/stocks/service/stocks.api'
import type { Stock } from '@/pages/main/stocks/service/stocks.types'

import { chartsApi } from './service/charts.api'
import type { OhlcvPoint } from './service/charts.types'

type PeriodKey = '1m' | '3m' | '6m' | '1y' | 'custom'

const periodLimitMap: Record<Exclude<PeriodKey, 'custom'>, number> = {
  '1m': 30,
  '3m': 70,
  '6m': 130,
  '1y': 260,
}

const marketOptions = [
  { label: '전체', value: '' },
  { label: 'KOSPI', value: 'KOSPI' },
  { label: 'KOSDAQ', value: 'KOSDAQ' },
]

const periodOptions = [
  { label: '1개월', value: '1m' },
  { label: '3개월', value: '3m' },
  { label: '6개월', value: '6m' },
  { label: '1년', value: '1y' },
  { label: '직접 선택', value: 'custom' },
]

const stocks = ref<Stock[]>([])
const selectedStockId = ref<number | null>(null)
const chartItems = ref<OhlcvPoint[]>([])
const loading = ref(false)
const stockLoading = ref(false)
const errorMessage = ref('')
const marketFilter = ref('')
const periodKey = ref<PeriodKey>('6m')
const customRange = ref<[string, string] | null>(null)
const showMa20 = ref(true)
const showMa60 = ref(true)
const showMa120 = ref(true)
const showRsi = ref(true)
const showMacd = ref(true)

const selectedStock = computed(() => stocks.value.find((stock) => stock.id === selectedStockId.value) ?? null)
const chartDateRange = computed(() => {
  if (!chartItems.value.length) return ''
  return `${chartItems.value[0].date} ~ ${chartItems.value[chartItems.value.length - 1].date}`
})
const firstDate = computed(() => chartItems.value[0]?.date ?? '')
const lastDate = computed(() => chartItems.value[chartItems.value.length - 1]?.date ?? '')
const gridLines = [48, 128, 208, 288, 368, 450, 535, 615]

function toNumber(value: string | number | null | undefined) {
  if (value === null || value === undefined || value === '') return null
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : null
}

function stockOptionLabel(stock: Stock) {
  return `${stock.name} ${stock.code} ${stock.market ?? ''}`
}

function xAt(index: number) {
  const count = Math.max(chartItems.value.length - 1, 1)
  return 54 + (index / count) * 910
}

function scale(value: number, min: number, max: number, top: number, height: number) {
  if (max === min) return top + height / 2
  return top + height - ((value - min) / (max - min)) * height
}

function linePoints(values: Array<number | null>, top: number, height: number) {
  const finite = values.filter((value): value is number => value !== null && Number.isFinite(value))
  if (!finite.length) return ''
  const min = Math.min(...finite)
  const max = Math.max(...finite)
  return values
    .map((value, index) => (value === null ? null : `${xAt(index)},${scale(value, min, max, top, height)}`))
    .filter(Boolean)
    .join(' ')
}

const visiblePriceLines = computed(() => {
  const lines = [
    { name: 'Close', color: '#111827', values: chartItems.value.map((item) => toNumber(item.close)), enabled: true },
    { name: 'MA20', color: '#d97706', values: chartItems.value.map((item) => toNumber(item.ma20)), enabled: showMa20.value },
    { name: 'MA60', color: '#059669', values: chartItems.value.map((item) => toNumber(item.ma60)), enabled: showMa60.value },
    { name: 'MA120', color: '#7c3aed', values: chartItems.value.map((item) => toNumber(item.ma120)), enabled: showMa120.value },
  ]
  return lines
    .filter((line) => line.enabled)
    .map((line) => ({ name: line.name, color: line.color, points: linePoints(line.values, 48, 320) }))
    .filter((line) => line.points)
})

const volumeBars = computed(() => {
  const volumes = chartItems.value.map((item) => item.volume ?? 0)
  const maxVolume = Math.max(...volumes, 1)
  const width = Math.max(2, 820 / Math.max(chartItems.value.length, 1))
  return volumes.map((volume, index) => {
    const height = (volume / maxVolume) * 62
    return { key: `${index}-${volume}`, x: xAt(index) - width / 2, y: 454 - height, width, height }
  })
})

const rsiLine = computed(() => linePoints(chartItems.value.map((item) => toNumber(item.rsi14)), 470, 62))
const macdLine = computed(() => linePoints(chartItems.value.map((item) => toNumber(item.macd)), 552, 62))
const signalLine = computed(() => linePoints(chartItems.value.map((item) => toNumber(item.macd_signal)), 552, 62))
const macdBars = computed(() => {
  const values = chartItems.value.map((item) => toNumber(item.macd_histogram) ?? 0)
  const maxAbs = Math.max(...values.map((value) => Math.abs(value)), 1)
  const width = Math.max(2, 820 / Math.max(chartItems.value.length, 1))
  return values.map((value, index) => {
    const height = (Math.abs(value) / maxAbs) * 28
    const baseline = 584
    return {
      key: `${index}-${value}`,
      x: xAt(index) - width / 2,
      y: value >= 0 ? baseline - height : baseline,
      width,
      height,
      negative: value < 0,
    }
  })
})

async function searchStocks(query = '') {
  stockLoading.value = true
  try {
    stocks.value = await stocksApi.list({
      search: query || undefined,
      market: marketFilter.value || undefined,
      is_active: true,
    })
  } finally {
    stockLoading.value = false
  }
}

async function loadInitialStock() {
  await searchStocks('005930')
  if (!selectedStockId.value && stocks.value.length > 0) {
    selectedStockId.value = stocks.value[0].id
  }
}

async function handleMarketChange() {
  selectedStockId.value = null
  chartItems.value = []
  await searchStocks('')
}

async function handlePeriodChange() {
  if (periodKey.value !== 'custom') {
    customRange.value = null
    await loadChart()
  }
}

async function loadChart() {
  if (!selectedStockId.value) return
  loading.value = true
  errorMessage.value = ''
  try {
    const response =
      periodKey.value === 'custom' && customRange.value
        ? await chartsApi.ohlcv(selectedStockId.value, { date_from: customRange.value[0], date_to: customRange.value[1], limit: 1000 })
        : await chartsApi.ohlcv(selectedStockId.value, { limit: periodLimitMap[periodKey.value as Exclude<PeriodKey, 'custom'>] })
    chartItems.value = response.items
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '차트 데이터를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadInitialStock()
  await loadChart()
})
</script>

<style scoped>
.charts-page {
  margin-top: 18px;
}

.chart-panel {
  padding: 18px;
}

.panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.panel-head p {
  margin: 6px 0 0;
}

.control-grid {
  display: grid;
  grid-template-columns: minmax(320px, 1.4fr) minmax(220px, 0.8fr) minmax(420px, 1.6fr);
  gap: 12px;
  margin-bottom: 14px;
}

.control-card {
  min-width: 0;
  padding: 12px;
  border: 1px solid rgba(15, 23, 42, 0.1);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.72);
}

.control-card label {
  display: block;
  margin-bottom: 8px;
  color: #64748b;
  font-size: 12px;
  font-weight: 700;
}

.search-card :deep(.el-select),
.period-card :deep(.el-date-editor) {
  width: 100%;
}

.period-card :deep(.el-segmented) {
  margin-bottom: 8px;
}

.stock-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.stock-option small,
.selected-stock span {
  color: #64748b;
}

.selected-stock {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
}

.indicator-options {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.indicator-options > span {
  color: #64748b;
  font-size: 12px;
  font-weight: 700;
}

.status-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  min-height: 24px;
  margin-bottom: 12px;
}

.chart-box {
  width: 100%;
  min-height: 680px;
}

.chart-box svg {
  width: 100%;
  height: auto;
  min-height: 620px;
}

.chart-bg {
  fill: #f8fafc;
}

.grid-line line {
  stroke: rgba(100, 116, 139, 0.18);
  stroke-width: 1;
}

.chart-line {
  fill: none;
  stroke-width: 2.4;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.sub-line {
  stroke-width: 1.8;
}

.volume-bars rect {
  fill: #94a3b8;
  opacity: 0.34;
}

.macd-bars rect {
  fill: #dc2626;
  opacity: 0.42;
}

.macd-bars rect.negative {
  fill: #2563eb;
}

.axis-label,
.date-label {
  fill: #64748b;
  font-size: 13px;
  font-weight: 700;
}

@media (max-width: 1180px) {
  .control-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .panel-head {
    display: block;
  }

  .panel-head .el-button {
    width: 100%;
    margin-top: 12px;
  }

  .chart-box {
    min-height: 540px;
  }
}
</style>
