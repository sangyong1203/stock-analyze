<template>
  <section class="charts-page">
    <div class="content-band chart-panel">
      <div class="panel-head">
        <div>
          <h2 class="section-title">가격 차트</h2>
          <p class="muted">KRX 일봉 OHLCV 데이터를 종목별로 확인합니다.</p>
        </div>
        <div class="toolbar">
          <el-select v-model="selectedStockId" filterable placeholder="종목 선택" @change="loadChart">
            <el-option v-for="stock in stocks" :key="stock.id" :label="`${stock.code} ${stock.name}`" :value="stock.id" />
          </el-select>
          <el-input-number v-model="limit" :min="20" :max="500" :step="20" controls-position="right" @change="loadChart" />
          <el-button :loading="loading" @click="loadChart">조회</el-button>
        </div>
      </div>

      <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon :closable="false" />
      <el-empty v-else-if="!loading && chartItems.length === 0" description="가격 데이터가 없습니다. KRX 가격 수집을 먼저 실행하세요." />
      <div ref="chartRef" class="chart-box" />
    </div>
  </section>
</template>

<script setup lang="ts">
import * as echarts from 'echarts'
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'

import { stocksApi } from '@/pages/main/stocks/service/stocks.api'
import type { Stock } from '@/pages/main/stocks/service/stocks.types'

import { chartsApi } from './service/charts.api'
import type { OhlcvPoint } from './service/charts.types'

const chartRef = ref<HTMLDivElement | null>(null)
const chart = ref<echarts.ECharts | null>(null)
const stocks = ref<Stock[]>([])
const selectedStockId = ref<number | null>(null)
const chartItems = ref<OhlcvPoint[]>([])
const loading = ref(false)
const errorMessage = ref('')
const limit = ref(120)

function toNumber(value: string | number | null | undefined) {
  if (value === null || value === undefined || value === '') return 0
  return Number(value)
}

function renderChart() {
  if (!chartRef.value) return
  if (!chart.value) {
    chart.value = echarts.init(chartRef.value)
  }

  const dates = chartItems.value.map((item) => item.date)
  const candles = chartItems.value.map((item) => [toNumber(item.open), toNumber(item.close), toNumber(item.low), toNumber(item.high)])
  const volumes = chartItems.value.map((item) => item.volume ?? 0)

  chart.value.setOption({
    tooltip: { trigger: 'axis' },
    grid: [
      { left: 48, right: 24, top: 24, height: 280 },
      { left: 48, right: 24, top: 330, height: 90 },
    ],
    xAxis: [
      { type: 'category', data: dates, boundaryGap: true },
      { type: 'category', data: dates, gridIndex: 1, boundaryGap: true },
    ],
    yAxis: [
      { scale: true },
      { scale: true, gridIndex: 1 },
    ],
    dataZoom: [{ type: 'inside', xAxisIndex: [0, 1] }],
    series: [
      {
        type: 'candlestick',
        name: 'OHLC',
        data: candles,
        itemStyle: {
          color: '#d43f3a',
          color0: '#2468d8',
          borderColor: '#d43f3a',
          borderColor0: '#2468d8',
        },
      },
      {
        type: 'bar',
        name: 'Volume',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volumes,
        itemStyle: { color: '#8a96a8' },
      },
    ],
  })
}

async function loadStocks() {
  stocks.value = await stocksApi.list({ is_active: true })
  if (!selectedStockId.value && stocks.value.length > 0) {
    selectedStockId.value = stocks.value[0].id
  }
}

async function loadChart() {
  if (!selectedStockId.value) return
  loading.value = true
  errorMessage.value = ''
  try {
    const response = await chartsApi.ohlcv(selectedStockId.value, limit.value)
    chartItems.value = response.items
    await nextTick()
    renderChart()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '차트 데이터를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

function resizeChart() {
  chart.value?.resize()
}

onMounted(async () => {
  await loadStocks()
  await loadChart()
  window.addEventListener('resize', resizeChart)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart)
  chart.value?.dispose()
})
</script>

<style scoped>
.charts-page {
  margin-top: 18px;
}

.chart-panel {
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
  grid-template-columns: 280px 140px auto;
  gap: 10px;
  align-items: center;
}

.chart-box {
  width: 100%;
  height: 460px;
}

@media (max-width: 900px) {
  .panel-head,
  .toolbar {
    display: block;
  }

  .toolbar > * {
    width: 100%;
    margin-bottom: 8px;
  }
}
</style>
