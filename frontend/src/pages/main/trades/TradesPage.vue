<template>
  <section class="trades-page">
    <div class="content-band">
      <div class="panel-head">
        <div>
          <h2 class="section-title">거래 기록</h2>
          <p class="muted">매수/매도 기록을 저장하고 보유현황 계산에 반영합니다.</p>
        </div>
      </div>

      <el-alert
        v-if="!fundPools.length"
        title="먼저 포트폴리오 화면에서 자금 풀을 생성해 주세요."
        type="warning"
        :closable="false"
        show-icon
      />

      <div class="trade-layout">
        <div class="trade-form-card">
          <div class="card-head">
            <strong>{{ editingTradeId ? '거래 수정' : '거래 등록' }}</strong>
            <el-button v-if="editingTradeId" text @click="resetForm">취소</el-button>
          </div>
          <el-form label-position="top" @submit.prevent>
            <el-form-item label="자금 풀">
              <el-select v-model="form.fund_pool_id" placeholder="자금 풀 선택">
                <el-option v-for="pool in fundPools" :key="pool.id" :label="pool.name" :value="pool.id" />
              </el-select>
            </el-form-item>

            <el-form-item label="종목">
              <el-select
                v-model="form.stock_id"
                filterable
                remote
                reserve-keyword
                placeholder="종목명 또는 종목코드 입력"
                :loading="stockLoading"
                :remote-method="searchStocks"
              >
                <el-option v-for="stock in stocks" :key="stock.id" :label="`${stock.name} ${stock.code}`" :value="stock.id">
                  <div class="stock-option">
                    <span>{{ stock.name }}</span>
                    <small>{{ stock.code }} · {{ stock.market || '-' }}</small>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>

            <div class="field-grid">
              <el-form-item label="거래 구분">
                <el-segmented v-model="form.trade_type" :options="tradeTypeOptions" />
              </el-form-item>
              <el-form-item label="거래일">
                <el-date-picker v-model="form.trade_date" type="date" value-format="YYYY-MM-DD" />
              </el-form-item>
            </div>

            <div class="field-grid">
              <el-form-item label="수량">
                <el-input-number v-model="form.quantity" :min="1" :step="1" />
              </el-form-item>
              <el-form-item label="가격">
                <el-input-number v-model="form.price" :min="1" :step="100" />
              </el-form-item>
            </div>

            <div class="field-grid">
              <el-form-item label="수수료">
                <el-input-number v-model="form.fee" :min="0" :step="100" />
              </el-form-item>
              <el-form-item label="세금">
                <el-input-number v-model="form.tax" :min="0" :step="100" />
              </el-form-item>
            </div>

            <el-form-item label="거래 사유">
              <el-input v-model="form.reason" />
            </el-form-item>
            <el-form-item label="메모">
              <el-input v-model="form.memo" type="textarea" :rows="3" />
            </el-form-item>
            <el-button type="primary" :loading="submitting" :disabled="!fundPools.length" @click="submitTrade">
              {{ editingTradeId ? '수정 저장' : '거래 등록' }}
            </el-button>
          </el-form>
        </div>

        <div class="trade-list-card">
          <div class="card-head">
            <strong>거래 목록</strong>
            <el-tag type="info" effect="plain">{{ trades.length }}건</el-tag>
          </div>
          <el-alert v-if="errorMessage" :title="errorMessage" type="error" :closable="false" show-icon />
          <el-empty v-else-if="!loading && !trades.length" description="등록된 거래가 없습니다." />
          <el-table v-else v-loading="loading" :data="trades" stripe>
            <el-table-column prop="trade_date" label="거래일" width="110" />
            <el-table-column label="종목" min-width="180">
              <template #default="{ row }">
                <div class="stack">
                  <strong>{{ row.stock_name }}</strong>
                  <small>{{ row.stock_code }}</small>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="구분" width="80">
              <template #default="{ row }">
                <el-tag :type="row.trade_type === 'buy' ? 'danger' : 'primary'">{{ formatTradeType(row.trade_type) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="수량" width="90" />
            <el-table-column label="가격" width="120">
              <template #default="{ row }">{{ formatKrw(row.price) }}</template>
            </el-table-column>
            <el-table-column label="총액" width="120">
              <template #default="{ row }">{{ formatKrw(row.total_amount) }}</template>
            </el-table-column>
            <el-table-column label="실현손익" width="120">
              <template #default="{ row }">{{ formatKrw(row.realized_profit_loss) }}</template>
            </el-table-column>
            <el-table-column label="자금 풀" min-width="120" prop="fund_pool_name" />
            <el-table-column label="작업" width="140" fixed="right">
              <template #default="{ row }">
                <div class="action-row">
                  <el-button text size="small" @click="startEdit(row)">수정</el-button>
                  <el-button text size="small" type="danger" @click="removeTrade(row.id)">삭제</el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { portfolioApi } from '@/pages/main/portfolio/service/portfolio.api'
import type { FundPool } from '@/pages/main/portfolio/service/portfolio.types'
import { stocksApi } from '@/pages/main/stocks/service/stocks.api'
import type { Stock } from '@/pages/main/stocks/service/stocks.types'

import { tradesApi } from './service/trades.api'
import type { Trade, TradePayload } from './service/trades.types'
import { formatKrw, formatTradeType } from './service/trades.utils'

const tradeTypeOptions = [
  { label: '매수', value: 'buy' },
  { label: '매도', value: 'sell' },
]

const stocks = ref<Stock[]>([])
const fundPools = ref<FundPool[]>([])
const trades = ref<Trade[]>([])
const stockLoading = ref(false)
const loading = ref(false)
const submitting = ref(false)
const errorMessage = ref('')
const editingTradeId = ref<number | null>(null)

const form = ref<TradePayload>({
  fund_pool_id: 0,
  stock_id: 0,
  trade_type: 'buy',
  trade_date: new Date().toISOString().slice(0, 10),
  quantity: 1,
  price: 0,
  fee: 0,
  tax: 0,
  reason: '',
  memo: '',
})

function resetForm() {
  editingTradeId.value = null
  form.value = {
    fund_pool_id: fundPools.value[0]?.id ?? 0,
    stock_id: 0,
    trade_type: 'buy',
    trade_date: new Date().toISOString().slice(0, 10),
    quantity: 1,
    price: 0,
    fee: 0,
    tax: 0,
    reason: '',
    memo: '',
  }
}

async function searchStocks(query = '') {
  stockLoading.value = true
  try {
    stocks.value = await stocksApi.list({ search: query || undefined, is_active: true })
  } finally {
    stockLoading.value = false
  }
}

async function loadBaseData() {
  loading.value = true
  errorMessage.value = ''
  try {
    const [tradeRows, poolRows] = await Promise.all([tradesApi.list(), portfolioApi.getFundPools()])
    trades.value = tradeRows
    fundPools.value = poolRows
    if (!form.value.fund_pool_id && poolRows.length > 0) {
      form.value.fund_pool_id = poolRows[0].id
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '거래 데이터를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

function startEdit(item: Trade) {
  editingTradeId.value = item.id
  form.value = {
    fund_pool_id: item.fund_pool_id,
    stock_id: item.stock_id,
    trade_type: item.trade_type,
    trade_date: item.trade_date,
    quantity: item.quantity,
    price: Number(item.price),
    fee: Number(item.fee),
    tax: Number(item.tax),
    reason: item.reason ?? '',
    memo: item.memo ?? '',
  }
}

async function submitTrade() {
  if (!form.value.fund_pool_id || !form.value.stock_id) {
    errorMessage.value = '자금 풀과 종목을 선택해 주세요.'
    return
  }
  submitting.value = true
  errorMessage.value = ''
  try {
    if (editingTradeId.value) {
      await tradesApi.update(editingTradeId.value, form.value)
    } else {
      await tradesApi.create(form.value)
    }
    await loadBaseData()
    resetForm()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '거래 저장에 실패했습니다.'
  } finally {
    submitting.value = false
  }
}

async function removeTrade(tradeId: number) {
  try {
    await tradesApi.remove(tradeId)
    await loadBaseData()
    if (editingTradeId.value === tradeId) {
      resetForm()
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '거래 삭제에 실패했습니다.'
  }
}

onMounted(async () => {
  await Promise.all([loadBaseData(), searchStocks('005930')])
})
</script>

<style scoped>
.trades-page {
  margin-top: 18px;
}

.panel-head {
  margin-bottom: 16px;
}

.panel-head p {
  margin: 6px 0 0;
}

.trade-layout {
  display: grid;
  grid-template-columns: minmax(320px, 420px) minmax(0, 1fr);
  gap: 16px;
}

.trade-form-card,
.trade-list-card {
  padding: 16px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.82);
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.field-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stock-option,
.stack {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.stack {
  flex-direction: column;
  gap: 2px;
}

.stack small,
.stock-option small {
  color: #64748b;
}

.action-row {
  display: flex;
  gap: 6px;
}

@media (max-width: 1100px) {
  .trade-layout {
    grid-template-columns: 1fr;
  }
}
</style>
