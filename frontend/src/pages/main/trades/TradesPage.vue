<template>
  <section class="trades-page">
    <div class="content-band">
      <div class="panel-head">
        <div>
          <h2 class="section-title">거래 기록</h2>
          <p class="muted">매수/매도 기록과 거래 메모, 태그, 관련 뉴스를 함께 관리합니다.</p>
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
                    <small>{{ stock.code }} / {{ stock.market || '-' }}</small>
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
            <el-table-column label="작업" width="180" fixed="right">
              <template #default="{ row }">
                <div class="action-row">
                  <el-button text size="small" @click="openDetail(row)">상세</el-button>
                  <el-button text size="small" @click="startEdit(row)">수정</el-button>
                  <el-button text size="small" type="danger" @click="removeTrade(row.id)">삭제</el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>

    <el-drawer v-model="detailOpen" title="거래 상세 관리" size="42%">
      <div v-if="selectedTrade" class="detail-body">
        <h3>{{ selectedTrade.stock_name }} / {{ formatTradeType(selectedTrade.trade_type) }}</h3>
        <p class="muted">{{ selectedTrade.trade_date }} / {{ formatKrw(selectedTrade.total_amount) }} / {{ selectedTrade.fund_pool_name }}</p>

        <section class="detail-section">
          <div class="section-row">
            <h4>거래 메모</h4>
          </div>
          <el-form label-position="top" @submit.prevent>
            <el-form-item label="제목">
              <el-input v-model="tradeMemoForm.title" />
            </el-form-item>
            <el-form-item label="내용">
              <el-input v-model="tradeMemoForm.content" type="textarea" :rows="3" />
            </el-form-item>
            <div class="inline-actions">
              <el-button @click="resetTradeMemoForm">초기화</el-button>
              <el-button type="primary" :loading="memoSubmitting" @click="saveTradeMemo">
                {{ tradeMemoForm.id ? '메모 수정' : '메모 추가' }}
              </el-button>
            </div>
          </el-form>
          <el-table :data="tradeMemos" size="small" border>
            <el-table-column prop="title" label="제목" min-width="140" />
            <el-table-column prop="content" label="내용" min-width="220" show-overflow-tooltip />
            <el-table-column label="관리" width="120">
              <template #default="{ row }">
                <el-button text size="small" @click="editTradeMemo(row)">수정</el-button>
                <el-button text size="small" type="danger" @click="removeMemo(row.id)">삭제</el-button>
              </template>
            </el-table-column>
          </el-table>
        </section>

        <section class="detail-section">
          <div class="section-row">
            <h4>거래 태그</h4>
          </div>
          <div class="tag-list">
            <el-tag v-for="tag in tradeTagLinks" :key="tag.id" closable @close="removeTradeTag(tag.tag_id)">
              {{ tag.tag_name }}
            </el-tag>
            <span v-if="tradeTagLinks.length === 0" class="muted">연결된 태그가 없습니다.</span>
          </div>
          <div class="field-grid compact-grid">
            <el-select v-model="selectedTradeTagId" placeholder="기존 태그 연결" clearable>
              <el-option v-for="tag in availableTradeTags" :key="tag.id" :label="tag.name" :value="tag.id" />
            </el-select>
            <el-button :loading="tagSubmitting" @click="linkExistingTradeTag">기존 태그 연결</el-button>
          </div>
          <div class="field-grid compact-grid">
            <el-input v-model="newTradeTagName" placeholder="새 태그 이름" />
            <el-button type="primary" :loading="tagSubmitting" @click="createAndLinkTradeTag">새 태그 추가</el-button>
          </div>
        </section>

        <section class="detail-section">
          <div class="section-row">
            <h4>관련 뉴스 연결</h4>
          </div>
          <div class="field-grid compact-grid">
            <el-input v-model="newsKeyword" placeholder="뉴스 제목 검색" @keyup.enter="searchTradeNewsCandidates" />
            <el-button :loading="newsSearchLoading" @click="searchTradeNewsCandidates">뉴스 검색</el-button>
          </div>
          <el-table :data="tradeNewsLinks" size="small" border>
            <el-table-column prop="title" label="연결된 뉴스" min-width="260" show-overflow-tooltip />
            <el-table-column prop="source" label="출처" width="120" />
            <el-table-column label="관리" width="100">
              <template #default="{ row }">
                <el-button text size="small" type="danger" @click="unlinkTradeNews(row.news_id)">해제</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-table :data="newsCandidates" size="small" border class="candidate-table">
            <el-table-column prop="title" label="검색 결과" min-width="260" show-overflow-tooltip />
            <el-table-column prop="source" label="출처" width="120" />
            <el-table-column label="연결" width="90">
              <template #default="{ row }">
                <el-button text size="small" :loading="newsLinkSubmitting" @click="linkTradeNews(row.id)">연결</el-button>
              </template>
            </el-table-column>
          </el-table>
        </section>
      </div>
    </el-drawer>
  </section>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { onMounted, ref } from 'vue'

import { memosApi } from '@/pages/main/memos/service/memos.api'
import type { Memo, Tag, TagLink } from '@/pages/main/memos/service/memos.types'
import { newsApi } from '@/pages/main/news/service/news.api'
import type { News } from '@/pages/main/news/service/news.types'
import { portfolioApi } from '@/pages/main/portfolio/service/portfolio.api'
import type { FundPool } from '@/pages/main/portfolio/service/portfolio.types'
import { stocksApi } from '@/pages/main/stocks/service/stocks.api'
import type { Stock } from '@/pages/main/stocks/service/stocks.types'

import { tradesApi } from './service/trades.api'
import type { Trade, TradeNewsLink, TradePayload } from './service/trades.types'
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

const detailOpen = ref(false)
const selectedTrade = ref<Trade | null>(null)
const tradeMemos = ref<Memo[]>([])
const tradeTagLinks = ref<TagLink[]>([])
const availableTradeTags = ref<Tag[]>([])
const tradeNewsLinks = ref<TradeNewsLink[]>([])
const newsCandidates = ref<News[]>([])
const memoSubmitting = ref(false)
const tagSubmitting = ref(false)
const newsSearchLoading = ref(false)
const newsLinkSubmitting = ref(false)
const selectedTradeTagId = ref<number | null>(null)
const newTradeTagName = ref('')
const newsKeyword = ref('')

const tradeMemoForm = ref({
  id: null as number | null,
  title: '',
  content: '',
})

const form = ref<TradePayload>({
  fund_pool_id: null,
  stock_id: null,
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
    fund_pool_id: fundPools.value[0]?.id ?? null,
    stock_id: null,
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

function resetTradeMemoForm() {
  tradeMemoForm.value = { id: null, title: '', content: '' }
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

async function loadTradeConnections(tradeId: number) {
  const [memoRows, tagRows, tagList, newsLinks] = await Promise.all([
    memosApi.list({ trade_id: tradeId }),
    memosApi.listTagLinks('trade', tradeId),
    memosApi.listTags({ tag_type: 'trade' }),
    tradesApi.listNews(tradeId),
  ])
  tradeMemos.value = memoRows
  tradeTagLinks.value = tagRows
  availableTradeTags.value = tagList
  tradeNewsLinks.value = newsLinks
}

async function openDetail(item: Trade) {
  selectedTrade.value = item
  detailOpen.value = true
  resetTradeMemoForm()
  selectedTradeTagId.value = null
  newTradeTagName.value = ''
  newsKeyword.value = ''
  newsCandidates.value = []
  await loadTradeConnections(item.id)
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
    if (selectedTrade.value?.id === tradeId) {
      detailOpen.value = false
      selectedTrade.value = null
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '거래 삭제에 실패했습니다.'
  }
}

function editTradeMemo(item: Memo) {
  tradeMemoForm.value = {
    id: item.id,
    title: item.title ?? '',
    content: item.content,
  }
}

async function saveTradeMemo() {
  if (!selectedTrade.value || !tradeMemoForm.value.content.trim()) return
  memoSubmitting.value = true
  try {
    if (tradeMemoForm.value.id) {
      await memosApi.update(tradeMemoForm.value.id, {
        title: tradeMemoForm.value.title,
        content: tradeMemoForm.value.content,
      })
    } else {
      await memosApi.create({
        memo_type: 'trade',
        trade_id: selectedTrade.value.id,
        title: tradeMemoForm.value.title,
        content: tradeMemoForm.value.content,
      })
    }
    resetTradeMemoForm()
    await loadTradeConnections(selectedTrade.value.id)
  } finally {
    memoSubmitting.value = false
  }
}

async function removeMemo(memoId: number) {
  if (!selectedTrade.value) return
  await memosApi.remove(memoId)
  await loadTradeConnections(selectedTrade.value.id)
}

async function linkExistingTradeTag() {
  if (!selectedTrade.value || !selectedTradeTagId.value) return
  tagSubmitting.value = true
  try {
    await memosApi.createTagLink({
      tag_id: selectedTradeTagId.value,
      target_type: 'trade',
      target_id: selectedTrade.value.id,
    })
    selectedTradeTagId.value = null
    await loadTradeConnections(selectedTrade.value.id)
  } finally {
    tagSubmitting.value = false
  }
}

async function createAndLinkTradeTag() {
  if (!selectedTrade.value || !newTradeTagName.value.trim()) return
  tagSubmitting.value = true
  try {
    const tag = await memosApi.createTag({
      name: newTradeTagName.value.trim(),
      tag_type: 'trade',
    })
    await memosApi.createTagLink({
      tag_id: tag.id,
      target_type: 'trade',
      target_id: selectedTrade.value.id,
    })
    newTradeTagName.value = ''
    await loadTradeConnections(selectedTrade.value.id)
  } finally {
    tagSubmitting.value = false
  }
}

async function removeTradeTag(tagId: number) {
  if (!selectedTrade.value) return
  await memosApi.removeTagLink(tagId, 'trade', selectedTrade.value.id)
  await loadTradeConnections(selectedTrade.value.id)
}

async function searchTradeNewsCandidates() {
  newsSearchLoading.value = true
  try {
    newsCandidates.value = await newsApi.list({ keyword: newsKeyword.value || undefined })
  } finally {
    newsSearchLoading.value = false
  }
}

async function linkTradeNews(newsId: number) {
  if (!selectedTrade.value) return
  newsLinkSubmitting.value = true
  try {
    await tradesApi.linkNews(selectedTrade.value.id, { news_id: newsId, link_type: 'reference' })
    await loadTradeConnections(selectedTrade.value.id)
  } finally {
    newsLinkSubmitting.value = false
  }
}

async function unlinkTradeNews(newsId: number) {
  if (!selectedTrade.value) return
  await tradesApi.unlinkNews(selectedTrade.value.id, newsId)
  await loadTradeConnections(selectedTrade.value.id)
}

onMounted(async () => {
  await Promise.all([loadBaseData(), searchStocks('005930')])
})
</script>

<style scoped>
.trades-page {
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

.card-head,
.section-row {
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

.compact-grid {
  margin-bottom: 12px;
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

.action-row,
.inline-actions,
.tag-list {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.detail-body h3 {
  margin-top: 0;
  margin-bottom: 6px;
}

.detail-section {
  margin-top: 20px;
}

.candidate-table {
  margin-top: 12px;
}

@media (max-width: 1100px) {
  .trade-layout {
    grid-template-columns: 1fr;
  }
}
</style>
