<template>
  <section class="portfolio-page">
    <div class="summary-grid">
      <article v-for="card in summaryCards" :key="card.label" class="summary-card">
        <span>{{ card.label }}</span>
        <strong :class="card.tone">{{ card.value }}</strong>
      </article>
    </div>

    <div class="content-band portfolio-layout">
      <div class="side-column">
        <section class="panel-card">
          <div class="panel-head">
            <div>
              <h2 class="section-title">자금 풀</h2>
              <p class="muted">투자 자금 풀을 생성하고 현금 흐름을 기록합니다.</p>
            </div>
          </div>

          <el-form label-position="top" @submit.prevent>
            <el-form-item label="풀 이름">
              <el-input v-model="poolForm.name" placeholder="예: 국내주식 계좌" />
            </el-form-item>
            <el-form-item label="설명">
              <el-input v-model="poolForm.description" />
            </el-form-item>
            <el-button type="primary" :loading="poolSubmitting" @click="submitPool">자금 풀 생성</el-button>
          </el-form>

          <el-divider />

          <el-form label-position="top" @submit.prevent>
            <el-form-item label="대상 자금 풀">
              <el-select v-model="transactionForm.fund_pool_id" placeholder="자금 풀 선택">
                <el-option v-for="pool in fundPools" :key="pool.id" :label="pool.name" :value="pool.id" />
              </el-select>
            </el-form-item>
            <div class="field-grid">
              <el-form-item label="유형">
                <el-select v-model="transactionForm.transaction_type">
                  <el-option label="입금" value="deposit" />
                  <el-option label="출금" value="withdraw" />
                </el-select>
              </el-form-item>
              <el-form-item label="일자">
                <el-date-picker v-model="transactionForm.transaction_date" type="date" value-format="YYYY-MM-DD" />
              </el-form-item>
            </div>
            <el-form-item label="금액">
              <el-input-number v-model="transactionForm.amount" :min="0" :step="10000" />
            </el-form-item>
            <el-form-item label="메모">
              <el-input v-model="transactionForm.memo" />
            </el-form-item>
            <el-button type="primary" :loading="transactionSubmitting" :disabled="!fundPools.length" @click="submitTransaction">입출금 저장</el-button>
          </el-form>
        </section>

        <section class="panel-card">
          <div class="card-inline">
            <div>
              <h3 class="section-title">보유 재계산</h3>
              <p class="muted">거래 기록 기준으로 holdings를 다시 계산합니다.</p>
            </div>
            <el-button :loading="recalculating" @click="recalculate">재계산</el-button>
          </div>
          <el-alert v-if="message" :title="message" type="success" :closable="false" show-icon />
          <el-alert v-if="errorMessage" :title="errorMessage" type="error" :closable="false" show-icon />
        </section>
      </div>

      <div class="main-column">
        <section class="panel-card">
          <div class="card-inline">
            <div>
              <h2 class="section-title">보유 종목</h2>
              <p class="muted">평균단가, 평가금액, 평가손익 기준입니다.</p>
            </div>
            <el-tag type="info" effect="plain">{{ holdings.length }}건</el-tag>
          </div>
          <el-empty v-if="!loading && !holdings.length" description="보유 데이터가 없습니다." />
          <el-table v-else v-loading="loading" :data="holdings" stripe>
            <el-table-column label="종목" min-width="180">
              <template #default="{ row }">
                <div class="stack">
                  <strong>{{ row.stock_name }}</strong>
                  <small>{{ row.stock_code }} · {{ row.fund_pool_name }}</small>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="수량" width="90" />
            <el-table-column label="평균단가" width="120">
              <template #default="{ row }">{{ formatKrw(row.average_price) }}</template>
            </el-table-column>
            <el-table-column label="현재가" width="120">
              <template #default="{ row }">{{ formatKrw(row.current_price) }}</template>
            </el-table-column>
            <el-table-column label="평가금액" width="130">
              <template #default="{ row }">{{ formatKrw(row.market_value) }}</template>
            </el-table-column>
            <el-table-column label="평가손익" width="130">
              <template #default="{ row }">{{ formatKrw(row.unrealized_profit_loss) }}</template>
            </el-table-column>
            <el-table-column label="수익률" width="100">
              <template #default="{ row }">{{ formatPercent(row.unrealized_profit_loss_rate) }}</template>
            </el-table-column>
          </el-table>
        </section>

        <section class="panel-card">
          <div class="card-inline">
            <div>
              <h2 class="section-title">현금 흐름</h2>
              <p class="muted">입금/출금과 거래 연계 현금 흐름을 함께 봅니다.</p>
            </div>
            <el-tag type="info" effect="plain">{{ fundTransactions.length }}건</el-tag>
          </div>
          <el-table :data="fundTransactions" stripe>
            <el-table-column prop="transaction_date" label="일자" width="110" />
            <el-table-column prop="fund_pool_name" label="자금 풀" min-width="140" />
            <el-table-column prop="transaction_type" label="유형" width="90" />
            <el-table-column label="금액" width="130">
              <template #default="{ row }">{{ formatKrw(row.amount) }}</template>
            </el-table-column>
            <el-table-column prop="memo" label="메모" min-width="180" />
          </el-table>
        </section>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { portfolioApi } from './service/portfolio.api'
import type {
  FundPool,
  FundPoolPayload,
  FundsSummary,
  FundTransaction,
  FundTransactionPayload,
  Holding,
  HoldingSummary,
  PortfolioSummary,
} from './service/portfolio.types'
import { formatKrw, formatPercent } from './service/portfolio.utils'

const loading = ref(false)
const poolSubmitting = ref(false)
const transactionSubmitting = ref(false)
const recalculating = ref(false)
const errorMessage = ref('')
const message = ref('')

const summary = ref<PortfolioSummary | null>(null)
const holdingSummary = ref<HoldingSummary | null>(null)
const fundsSummary = ref<FundsSummary | null>(null)
const fundPools = ref<FundPool[]>([])
const holdings = ref<Holding[]>([])
const fundTransactions = ref<FundTransaction[]>([])

const poolForm = ref<FundPoolPayload>({
  name: '',
  description: '',
  currency: 'KRW',
  is_active: true,
})

const transactionForm = ref<FundTransactionPayload>({
  fund_pool_id: null,
  transaction_type: 'deposit',
  amount: 0,
  transaction_date: new Date().toISOString().slice(0, 10),
  memo: '',
  currency: 'KRW',
})

const summaryCards = computed(() => [
  { label: '총 자산', value: formatKrw(summary.value?.total_asset_value) },
  { label: '현금 잔고', value: formatKrw(summary.value?.total_cash) },
  { label: '평가금액', value: formatKrw(summary.value?.total_market_value) },
  { label: '평가손익', value: formatKrw(summary.value?.total_unrealized_profit_loss), tone: Number(summary.value?.total_unrealized_profit_loss ?? 0) >= 0 ? 'metric-rise' : 'metric-fall' },
  { label: '평가수익률', value: formatPercent(summary.value?.total_unrealized_profit_loss_rate) },
  { label: '실현손익', value: formatKrw(summary.value?.realized_profit_loss), tone: Number(summary.value?.realized_profit_loss ?? 0) >= 0 ? 'metric-rise' : 'metric-fall' },
])

async function loadPortfolio() {
  loading.value = true
  errorMessage.value = ''
  try {
    const [portfolioSummary, holdingsRows, holdingSummaryRow, poolRows, transactionRows, fundsSummaryRow] = await Promise.all([
      portfolioApi.getSummary(),
      portfolioApi.getHoldings(),
      portfolioApi.getHoldingSummary(),
      portfolioApi.getFundPools(),
      portfolioApi.getFundTransactions(),
      portfolioApi.getFundsSummary(),
    ])
    summary.value = portfolioSummary
    holdings.value = holdingsRows
    holdingSummary.value = holdingSummaryRow
    fundPools.value = poolRows
    fundTransactions.value = transactionRows
    fundsSummary.value = fundsSummaryRow
    if (!transactionForm.value.fund_pool_id && poolRows.length > 0) {
      transactionForm.value.fund_pool_id = poolRows[0].id
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '포트폴리오 데이터를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

async function submitPool() {
  if (!poolForm.value.name?.trim()) {
    errorMessage.value = '자금 풀 이름을 입력해 주세요.'
    return
  }
  poolSubmitting.value = true
  errorMessage.value = ''
  message.value = ''
  try {
    await portfolioApi.createFundPool(poolForm.value)
    message.value = '자금 풀을 생성했습니다.'
    poolForm.value = { name: '', description: '', currency: 'KRW', is_active: true }
    await loadPortfolio()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '자금 풀 생성에 실패했습니다.'
  } finally {
    poolSubmitting.value = false
  }
}

async function submitTransaction() {
  if (!transactionForm.value.fund_pool_id) {
    errorMessage.value = '대상 자금 풀을 선택해 주세요.'
    return
  }
  transactionSubmitting.value = true
  errorMessage.value = ''
  message.value = ''
  try {
    await portfolioApi.createFundTransaction(transactionForm.value)
    message.value = '입출금 기록을 저장했습니다.'
    transactionForm.value = {
      fund_pool_id: transactionForm.value.fund_pool_id,
      transaction_type: 'deposit',
      amount: 0,
      transaction_date: new Date().toISOString().slice(0, 10),
      memo: '',
      currency: 'KRW',
    }
    await loadPortfolio()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '입출금 저장에 실패했습니다.'
  } finally {
    transactionSubmitting.value = false
  }
}

async function recalculate() {
  recalculating.value = true
  errorMessage.value = ''
  message.value = ''
  try {
    const result = await portfolioApi.recalculateHoldings()
    message.value = `보유 재계산 완료: 거래 ${result.processed_trade_count}건, 보유 ${result.holding_count}건`
    await loadPortfolio()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '보유 재계산에 실패했습니다.'
  } finally {
    recalculating.value = false
  }
}

onMounted(loadPortfolio)
</script>

<style scoped>
.portfolio-page {
  margin-top: 18px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.summary-card {
  padding: 16px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.78);
}

.summary-card span {
  display: block;
  color: #64748b;
  font-size: 12px;
  font-weight: 700;
}

.summary-card strong {
  display: block;
  margin-top: 10px;
  color: #0f172a;
  font-size: 20px;
}

.metric-rise {
  color: #dc2626;
}

.metric-fall {
  color: #2563eb;
}

.portfolio-layout {
  display: grid;
  grid-template-columns: minmax(300px, 360px) minmax(0, 1fr);
  gap: 16px;
}

.side-column,
.main-column {
  display: grid;
  gap: 16px;
}

.panel-card {
  padding: 16px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.82);
}

.panel-head p,
.card-inline p {
  margin: 6px 0 0;
}

.card-inline {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.field-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stack {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stack small {
  color: #64748b;
}

@media (max-width: 1200px) {
  .summary-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .portfolio-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 760px) {
  .summary-grid,
  .field-grid {
    grid-template-columns: 1fr;
  }
}
</style>
