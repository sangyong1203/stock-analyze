<template>
  <section class="news-page">
    <KpiGrid :items="kpiItems" :columns="4" />

    <el-tabs v-model="activeNewsTab" class="news-tabs">
      <el-tab-pane label="뉴스 수집/조회" name="news">
        <div class="content-band news-panel">
      <div class="panel-head">
        <div class="panel-head-title">
          <h2 class="section-title">뉴스 수집/조회</h2>
          <p class="muted">네이버 금융 시장 뉴스를 수집하고 수집 대상 종목과 매칭된 결과를 확인합니다.</p>
        </div>
        <div class="collect-actions">
          <el-input-number v-model="collectForm.pages" :min="1" :max="10" size="small" />
          <el-input-number v-model="collectForm.max_items" :min="1" :max="200" size="small" />
          <el-button type="primary" :loading="collecting" @click="collectMarketNews">시장 뉴스 수집</el-button>
        </div>
      </div>

      <div class="gpt-actions">
        <span class="muted">
          요약 대기 {{ gptTargets?.summary_pending_count ?? 0 }} /
          필터 대기 {{ gptTargets?.filter_pending_count ?? 0 }}
        </span>
        <el-input-number v-model="gptForm.limit" :min="1" :max="100" size="small" />
        <el-button :loading="gptRunning" @click="runGptSummary(true)">요약 dry-run</el-button>
        <el-button type="primary" :loading="gptRunning" @click="runGptSummary(false)">요약 실행</el-button>
        <el-button :loading="gptRunning" @click="runGptFilter(true)">재필터 dry-run</el-button>
        <el-button type="warning" :loading="gptRunning" @click="runGptFilter(false)">재필터 실행</el-button>
        <el-button type="danger" :loading="alertRecalculating" @click="recalculateAlerts">알림 후보 재계산</el-button>
      </div>

      <div class="toolbar">
        <el-input v-model="filters.keyword" placeholder="제목/요약 검색" clearable @keyup.enter="loadData" />
        <el-input v-model="filters.stock_code" placeholder="종목코드" clearable @keyup.enter="loadData" />
        <el-select v-model="filters.market_scope" placeholder="범위" clearable>
          <el-option label="market" value="market" />
          <el-option label="stock" value="stock" />
        </el-select>
        <el-input-number v-model="importanceFilter" :min="0" :max="10" placeholder="최소 중요도" />
        <el-select v-model="gptTargetFilter" placeholder="GPT 대상" clearable>
          <el-option label="대상" value="true" />
          <el-option label="비대상" value="false" />
        </el-select>
        <el-select v-model="filters.gpt_summary_status" placeholder="요약 상태" clearable>
          <el-option label="pending" value="pending" />
          <el-option label="done" value="done" />
          <el-option label="failed" value="failed" />
          <el-option label="skipped" value="skipped" />
        </el-select>
        <el-select v-model="filters.gpt_filter_result" placeholder="필터 결과" clearable>
          <el-option label="important" value="important" />
          <el-option label="price_impact" value="price_impact" />
          <el-option label="unnecessary" value="unnecessary" />
          <el-option label="failed" value="failed" />
        </el-select>
        <el-date-picker
          v-model="publishedRange"
          type="datetimerange"
          range-separator="~"
          start-placeholder="시작"
          end-placeholder="종료"
          value-format="YYYY-MM-DDTHH:mm:ss"
        />
        <el-button :loading="loading" @click="loadData">조회</el-button>
      </div>

      <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon :closable="false" />
      <el-alert
        v-if="lastJob"
        class="job-alert"
        :title="`최근 수집 job #${lastJob.id} ${lastJob.status}: 신규 ${lastJob.new_count}, 중복 ${lastJob.duplicate_count}, 제외 ${lastJob.excluded_count}`"
        :type="lastJob.status === 'success' ? 'success' : 'warning'"
        show-icon
        :closable="false"
      />

      <div class="table-shell">
        <el-table v-loading="loading" class="news-table" :data="pagedNewsRows" border height="100%" @row-click="openDetail">
        <el-table-column label="발행시각" width="150">
          <template #default="{ row }">{{ formatDateTime(row.published_at) }}</template>
        </el-table-column>
        <el-table-column prop="title" label="제목" min-width="260" show-overflow-tooltip />
        <el-table-column prop="source" label="출처" width="130" />
        <el-table-column label="관련 종목" min-width="180">
          <template #default="{ row }">
            <el-tag v-for="link in row.stock_links" :key="link.id" class="stock-tag" effect="plain">
              {{ link.stock_name }}({{ link.stock_code }})
            </el-tag>
            <span v-if="row.stock_links.length === 0" class="muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="중요도" width="90">
          <template #default="{ row }">
            <el-tag :type="importanceTagType(row.importance_score)">{{ row.importance_score }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="duplicate_count" label="중복" width="80" align="right" />
        <el-table-column prop="filter_status" label="필터 상태" width="150" />
        <el-table-column label="GPT 대상" width="90">
          <template #default="{ row }">
            <el-tag :type="row.is_gpt_summary_target ? 'success' : 'info'" effect="plain">
              {{ row.is_gpt_summary_target ? '대상' : '제외' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="gpt_summary_status" label="GPT 요약" width="110" />
        <el-table-column prop="gpt_filter_result" label="GPT 필터" width="120" />
        </el-table>
      </div>

      <div class="table-footer">
        <span class="muted">총 {{ totalNewsRows }}건 중 {{ pageStart }}-{{ pageEnd }}건 표시</span>
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          background
          layout="prev, pager, next, sizes"
          :total="totalNewsRows"
          :page-sizes="[50, 100, 200]"
        />
      </div>
    </div>

      </el-tab-pane>

      <el-tab-pane label="GPT 검수 목록" name="review">
        <div class="content-band review-panel">
          <div class="panel-head">
            <div class="panel-head-title">
              <h2 class="section-title">GPT 검수 목록</h2>
          <p class="muted">현재 필터 기준으로 GPT 결과와 알림 후보를 빠르게 검수합니다.</p>
        </div>
      </div>
      <div class="table-shell">
      <el-table v-loading="loading" class="news-table" :data="pagedReviewRows" border height="100%">
        <el-table-column label="발행시각" width="150">
          <template #default="{ row }">{{ formatDateTime(row.published_at) }}</template>
        </el-table-column>
        <el-table-column prop="title" label="제목" min-width="260" show-overflow-tooltip />
        <el-table-column label="관련 종목" min-width="160">
          <template #default="{ row }">{{ row.related_stocks.join(', ') || '-' }}</template>
        </el-table-column>
        <el-table-column prop="importance_score" label="중요도" width="90" />
        <el-table-column prop="gpt_filter_result" label="GPT 필터" width="120" />
        <el-table-column label="알림" width="90">
          <template #default="{ row }">
            <el-tag :type="row.is_alert_target ? 'danger' : 'info'" effect="plain">
              {{ row.is_alert_target ? '후보' : '제외' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="검수" width="90">
          <template #default="{ row }">
            <el-button link type="primary" @click="openReview(row.news_id)">수정</el-button>
          </template>
        </el-table-column>
      </el-table>
      </div>

      <div class="table-footer">
        <span class="muted">총 {{ totalReviewRows }}건 중 {{ reviewPageStart }}-{{ reviewPageEnd }}건 표시</span>
        <el-pagination
          v-model:current-page="reviewPagination.page"
          v-model:page-size="reviewPagination.pageSize"
          background
          layout="prev, pager, next, sizes"
          :total="totalReviewRows"
          :page-sizes="[50, 100, 200]"
        />
      </div>
    </div>

      </el-tab-pane>

      <el-tab-pane label="알림 후보" name="alerts">
        <div class="content-band review-panel">
          <div class="panel-head">
            <div class="panel-head-title">
              <h2 class="section-title">알림 후보</h2>
          <p class="muted">현재 필터 기준으로 이메일 발송 전 단계의 뉴스 알림 후보를 확인합니다.</p>
        </div>
      </div>
      <div class="table-shell">
      <el-table v-loading="loading" class="news-table" :data="pagedAlertRows" border height="100%">
        <el-table-column label="발행시각" width="150">
          <template #default="{ row }">{{ formatDateTime(row.published_at) }}</template>
        </el-table-column>
        <el-table-column prop="title" label="제목" min-width="260" show-overflow-tooltip />
        <el-table-column label="관련 종목" min-width="160">
          <template #default="{ row }">{{ row.related_stocks.join(', ') || '-' }}</template>
        </el-table-column>
        <el-table-column prop="importance_score" label="중요도" width="90" />
        <el-table-column prop="duplicate_count" label="중복" width="80" />
        <el-table-column prop="source_count" label="출처수" width="80" />
        <el-table-column prop="gpt_filter_result" label="GPT 필터" width="120" />
        <el-table-column label="상세" width="90">
          <template #default="{ row }">
            <el-button link type="primary" @click="openReview(row.news_id)">열기</el-button>
          </template>
        </el-table-column>
      </el-table>
      </div>

      <div class="table-footer">
        <span class="muted">총 {{ totalAlertRows }}건 중 {{ alertPageStart }}-{{ alertPageEnd }}건 표시</span>
        <el-pagination
          v-model:current-page="alertPagination.page"
          v-model:page-size="alertPagination.pageSize"
          background
          layout="prev, pager, next, sizes"
          :total="totalAlertRows"
          :page-sizes="[50, 100, 200]"
        />
      </div>
    </div>

      </el-tab-pane>
    </el-tabs>

    <el-drawer v-model="detailOpen" title="뉴스 상세" size="42%">
      <div v-if="selectedNews" class="detail-body">
        <h3>{{ selectedNews.title }}</h3>
        <a :href="selectedNews.url" target="_blank" rel="noreferrer">{{ selectedNews.url }}</a>
        <dl>
          <dt>출처</dt>
          <dd>{{ selectedNews.source ?? '-' }}</dd>
          <dt>발행시각</dt>
          <dd>{{ formatDateTime(selectedNews.published_at) }}</dd>
          <dt>중요도</dt>
          <dd>{{ selectedNews.importance_score }}</dd>
          <dt>중복 정보</dt>
          <dd>{{ selectedNews.duplicate_count }}회 / {{ selectedNews.source_count }}개 출처</dd>
          <dt>관련 종목</dt>
          <dd>
            <el-tag v-for="link in selectedNews.stock_links" :key="link.id" class="stock-tag" effect="plain">
              {{ link.stock_name }}({{ link.stock_code }})
            </el-tag>
            <span v-if="selectedNews.stock_links.length === 0">-</span>
          </dd>
          <dt>매칭 키워드</dt>
          <dd>{{ selectedNews.matched_keywords_json?.join(', ') || '-' }}</dd>
          <dt>요약/preview</dt>
          <dd>{{ selectedNews.original_summary || selectedNews.content_preview || '-' }}</dd>
          <dt>GPT 요약</dt>
          <dd>{{ selectedNews.gpt_summary || '-' }}</dd>
          <dt>요약 모델/시간</dt>
          <dd>{{ selectedNews.gpt_summary_model || '-' }} / {{ formatDateTime(selectedNews.gpt_summary_at) }}</dd>
          <dt>GPT 필터</dt>
          <dd>{{ selectedNews.gpt_filter_result || '-' }}</dd>
          <dt>필터 사유</dt>
          <dd>{{ selectedNews.gpt_filter_reason || '-' }}</dd>
          <dt>필터 모델/시간</dt>
          <dd>{{ selectedNews.gpt_filter_model || '-' }} / {{ formatDateTime(selectedNews.gpt_filter_at) }}</dd>
        </dl>

        <div class="review-editor">
          <h4>수동 검수 보정</h4>
          <el-form label-width="110px">
            <el-form-item label="GPT 필터">
              <el-select v-model="reviewForm.gpt_filter_result" clearable>
                <el-option label="important" value="important" />
                <el-option label="price_impact" value="price_impact" />
                <el-option label="unnecessary" value="unnecessary" />
                <el-option label="failed" value="failed" />
              </el-select>
            </el-form-item>
            <el-form-item label="필터 상태">
              <el-select v-model="reviewForm.filter_status" clearable>
                <el-option label="important_candidate" value="important_candidate" />
                <el-option label="normal_candidate" value="normal_candidate" />
                <el-option label="review_needed" value="review_needed" />
                <el-option label="exclude_candidate" value="exclude_candidate" />
              </el-select>
            </el-form-item>
            <el-form-item label="알림 후보">
              <el-switch v-model="reviewForm.is_alert_target" />
            </el-form-item>
            <el-form-item label="보정 사유">
              <el-input v-model="reviewForm.gpt_filter_reason" type="textarea" :rows="3" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="savingReview" @click="saveReview">검수 저장</el-button>
            </el-form-item>
          </el-form>
        </div>

        <div class="review-editor">
          <h4>관련 거래 연결</h4>
          <div class="link-row">
            <el-select v-model="selectedTradeIdToLink" placeholder="거래 선택" clearable filterable>
              <el-option
                v-for="trade in availableTrades"
                :key="trade.id"
                :label="`${trade.trade_date} / ${trade.stock_name} / ${trade.trade_type}`"
                :value="trade.id"
              />
            </el-select>
            <el-button type="primary" :loading="tradeLinkSubmitting" @click="linkTradeToNews">거래 연결</el-button>
          </div>
          <el-table :data="relatedTrades" size="small" border>
            <el-table-column prop="trade_date" label="거래일" width="110" />
            <el-table-column label="종목" min-width="150">
              <template #default="{ row }">{{ row.stock_name }} ({{ row.stock_code }})</template>
            </el-table-column>
            <el-table-column prop="trade_type" label="구분" width="80" />
            <el-table-column prop="quantity" label="수량" width="80" />
            <el-table-column label="관리" width="90">
              <template #default="{ row }">
                <el-button text size="small" type="danger" @click="unlinkTradeFromNews(row.trade_id)">해제</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="review-editor">
          <h4>뉴스 메모</h4>
          <el-form label-position="top" @submit.prevent>
            <el-form-item label="제목">
              <el-input v-model="newsMemoForm.title" />
            </el-form-item>
            <el-form-item label="내용">
              <el-input v-model="newsMemoForm.content" type="textarea" :rows="3" />
            </el-form-item>
            <div class="link-row">
              <el-button @click="resetNewsMemoForm">초기화</el-button>
              <el-button type="primary" :loading="memoSubmitting" @click="saveNewsMemo">
                {{ newsMemoForm.id ? '메모 수정' : '메모 추가' }}
              </el-button>
            </div>
          </el-form>
          <el-table :data="newsMemos" size="small" border>
            <el-table-column prop="title" label="제목" min-width="140" />
            <el-table-column prop="content" label="내용" min-width="220" show-overflow-tooltip />
            <el-table-column label="관리" width="120">
              <template #default="{ row }">
                <el-button text size="small" @click="editNewsMemo(row)">수정</el-button>
                <el-button text size="small" type="danger" @click="removeNewsMemo(row.id)">삭제</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="review-editor">
          <h4>뉴스 태그</h4>
          <div class="link-row tags-row">
            <el-tag v-for="tag in newsTagLinks" :key="tag.id" closable @close="removeNewsTag(tag.tag_id)">
              {{ tag.tag_name }}
            </el-tag>
            <span v-if="newsTagLinks.length === 0">연결된 태그가 없습니다.</span>
          </div>
          <div class="link-row">
            <el-select v-model="selectedNewsTagId" placeholder="기존 태그 연결" clearable>
              <el-option v-for="tag in availableNewsTags" :key="tag.id" :label="tag.name" :value="tag.id" />
            </el-select>
            <el-button :loading="tagSubmitting" @click="linkExistingNewsTag">기존 태그 연결</el-button>
          </div>
          <div class="link-row">
            <el-input v-model="newNewsTagName" placeholder="새 태그 이름" />
            <el-button type="primary" :loading="tagSubmitting" @click="createAndLinkNewsTag">새 태그 추가</el-button>
          </div>
        </div>
      </div>
    </el-drawer>
  </section>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { computed, onMounted, reactive, ref, watch } from 'vue'

import KpiGrid from '@/shared/components/KpiGrid.vue'

import { memosApi } from '@/pages/main/memos/service/memos.api'
import type { Memo, Tag, TagLink } from '@/pages/main/memos/service/memos.types'
import { tradesApi } from '@/pages/main/trades/service/trades.api'

import { newsApi } from './service/news.api'
import type {
  AlertCandidateItem,
  AlertCandidateSummary,
  GptStatusSummary,
  GptTargetsSummary,
  News,
  NewsCollectJob,
  NewsReviewItem,
  NewsSummary,
  RelatedTrade,
} from './service/news.types'
import { formatDateTime, formatNumber, importanceTagType } from './service/news.utils'

const loading = ref(false)
const collecting = ref(false)
const activeNewsTab = ref('news')
const errorMessage = ref('')
const newsRows = ref<News[]>([])
const summary = ref<NewsSummary | null>(null)
const lastJob = ref<NewsCollectJob | null>(null)
const gptTargets = ref<GptTargetsSummary | null>(null)
const gptStatus = ref<GptStatusSummary | null>(null)
const alertSummary = ref<AlertCandidateSummary | null>(null)
const reviewRows = ref<NewsReviewItem[]>([])
const alertRows = ref<AlertCandidateItem[]>([])
const selectedNews = ref<News | null>(null)
const detailOpen = ref(false)
const relatedTrades = ref<RelatedTrade[]>([])
const newsMemos = ref<Memo[]>([])
const newsTagLinks = ref<TagLink[]>([])
const availableNewsTags = ref<Tag[]>([])
const availableTrades = ref<import('@/pages/main/trades/service/trades.types').Trade[]>([])
const importanceFilter = ref<number | undefined>()
const publishedRange = ref<[string, string] | null>(null)
const gptRunning = ref(false)
const gptTargetFilter = ref('')
const savingReview = ref(false)
const alertRecalculating = ref(false)
const memoSubmitting = ref(false)
const tagSubmitting = ref(false)
const tradeLinkSubmitting = ref(false)
const selectedTradeIdToLink = ref<number | null>(null)
const selectedNewsTagId = ref<number | null>(null)
const newNewsTagName = ref('')

const newsMemoForm = reactive({
  id: null as number | null,
  title: '',
  content: '',
})

const filters = reactive({
  keyword: '',
  stock_code: '',
  market_scope: '',
  gpt_summary_status: '',
  gpt_filter_result: '',
})
const pagination = reactive({
  page: 1,
  pageSize: 50,
})
const reviewPagination = reactive({
  page: 1,
  pageSize: 50,
})
const alertPagination = reactive({
  page: 1,
  pageSize: 50,
})

const collectForm = reactive({
  pages: 1,
  max_items: 50,
})

const gptForm = reactive({
  limit: 5,
})

const reviewForm = reactive({
  gpt_filter_result: '',
  gpt_filter_reason: '',
  is_alert_target: false,
  filter_status: '',
})

const totalNewsRows = computed(() => newsRows.value.length)
const pageStart = computed(() => (totalNewsRows.value === 0 ? 0 : (pagination.page - 1) * pagination.pageSize + 1))
const pageEnd = computed(() => Math.min(pagination.page * pagination.pageSize, totalNewsRows.value))
const pagedNewsRows = computed(() => {
  const start = (pagination.page - 1) * pagination.pageSize
  return newsRows.value.slice(start, start + pagination.pageSize)
})
const totalReviewRows = computed(() => reviewRows.value.length)
const reviewPageStart = computed(() =>
  totalReviewRows.value === 0 ? 0 : (reviewPagination.page - 1) * reviewPagination.pageSize + 1,
)
const reviewPageEnd = computed(() => Math.min(reviewPagination.page * reviewPagination.pageSize, totalReviewRows.value))
const pagedReviewRows = computed(() => {
  const start = (reviewPagination.page - 1) * reviewPagination.pageSize
  return reviewRows.value.slice(start, start + reviewPagination.pageSize)
})
const totalAlertRows = computed(() => alertRows.value.length)
const alertPageStart = computed(() =>
  totalAlertRows.value === 0 ? 0 : (alertPagination.page - 1) * alertPagination.pageSize + 1,
)
const alertPageEnd = computed(() => Math.min(alertPagination.page * alertPagination.pageSize, totalAlertRows.value))
const pagedAlertRows = computed(() => {
  const start = (alertPagination.page - 1) * alertPagination.pageSize
  return alertRows.value.slice(start, start + alertPagination.pageSize)
})

const kpiItems = computed(() => [
  { label: '오늘 수집', value: formatNumber(summary.value?.today_news_count) },
  { label: '요약 대상', value: formatNumber(summary.value?.gpt_summary_target_count) },
  { label: '알림 후보', value: formatNumber(summary.value?.alert_target_count) },
  { label: '평균 중요도', value: summary.value?.avg_importance_score ?? 0 },
])

async function loadData() {
  loading.value = true
  errorMessage.value = ''
  try {
    const gptTargetValue = gptTargetFilter.value === '' ? undefined : gptTargetFilter.value === 'true'
    const reviewFilters = {
      keyword: filters.keyword || undefined,
      stock_code: filters.stock_code || undefined,
      min_importance_score: importanceFilter.value,
      gpt_summary_status: filters.gpt_summary_status || undefined,
      gpt_filter_result: filters.gpt_filter_result || undefined,
      published_from: publishedRange.value?.[0],
      published_to: publishedRange.value?.[1],
    }
    const [rows, summaryData, jobs, targets, status, reviews, alertSummaryData, alertCandidates] = await Promise.all([
      newsApi.list({
        keyword: filters.keyword || undefined,
        stock_code: filters.stock_code || undefined,
        market_scope: filters.market_scope || undefined,
        min_importance_score: importanceFilter.value,
        is_gpt_summary_target: gptTargetValue,
        gpt_summary_status: filters.gpt_summary_status || undefined,
        gpt_filter_result: filters.gpt_filter_result || undefined,
        published_from: publishedRange.value?.[0],
        published_to: publishedRange.value?.[1],
      }),
      newsApi.summary(),
      newsApi.listJobs(),
      newsApi.gptTargets(),
      newsApi.gptStatus(),
      newsApi.review(reviewFilters),
      newsApi.alertSummary(),
      newsApi.alertCandidates(reviewFilters),
    ])
    newsRows.value = rows
    pagination.page = 1
    reviewPagination.page = 1
    alertPagination.page = 1
    summary.value = summaryData
    lastJob.value = jobs[0] ?? null
    gptTargets.value = targets
    gptStatus.value = status
    reviewRows.value = reviews
    alertSummary.value = alertSummaryData
    alertRows.value = alertCandidates
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '뉴스 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

async function loadNewsConnections(newsId: number) {
  const [tradeRows, memoRows, tagRows, tagList, tradeList] = await Promise.all([
    newsApi.relatedTrades(newsId),
    memosApi.list({ news_id: newsId }),
    memosApi.listTagLinks('news', newsId),
    memosApi.listTags({ tag_type: 'news' }),
    tradesApi.list(),
  ])
  relatedTrades.value = tradeRows
  newsMemos.value = memoRows
  newsTagLinks.value = tagRows
  availableNewsTags.value = tagList
  availableTrades.value = tradeList
}

async function collectMarketNews() {
  collecting.value = true
  try {
    lastJob.value = await newsApi.collectMarket({ pages: collectForm.pages, max_items: collectForm.max_items })
    ElMessage.success(`뉴스 수집 완료: 신규 ${lastJob.value.new_count}, 중복 ${lastJob.value.duplicate_count}`)
    await loadData()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '뉴스 수집에 실패했습니다.'
  } finally {
    collecting.value = false
  }
}

async function runGptSummary(dryRun: boolean) {
  gptRunning.value = true
  try {
    const result = await newsApi.runGptSummary({ limit: gptForm.limit, dry_run: dryRun })
    ElMessage.success(`요약 ${dryRun ? 'dry-run' : '실행'}: 대상 ${result.target_count}, 처리 ${result.processed_count}`)
    await loadData()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'GPT 요약 실행에 실패했습니다.'
  } finally {
    gptRunning.value = false
  }
}

async function runGptFilter(dryRun: boolean) {
  gptRunning.value = true
  try {
    const result = await newsApi.runGptFilter({ limit: gptForm.limit, dry_run: dryRun })
    ElMessage.success(`재필터 ${dryRun ? 'dry-run' : '실행'}: 대상 ${result.target_count}, 처리 ${result.processed_count}`)
    await loadData()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'GPT 재필터 실행에 실패했습니다.'
  } finally {
    gptRunning.value = false
  }
}

async function recalculateAlerts() {
  alertRecalculating.value = true
  try {
    const result = await newsApi.recalculateAlertCandidates()
    ElMessage.success(`알림 후보 재계산: 후보 ${result.alert_target_count}, 변경 ${result.changed_count}`)
    await loadData()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '알림 후보 재계산에 실패했습니다.'
  } finally {
    alertRecalculating.value = false
  }
}

function openDetail(row: News) {
  selectedNews.value = row
  reviewForm.gpt_filter_result = row.gpt_filter_result ?? ''
  reviewForm.gpt_filter_reason = row.gpt_filter_reason ?? ''
  reviewForm.is_alert_target = row.is_alert_target
  reviewForm.filter_status = row.filter_status ?? ''
  newsMemoForm.id = null
  newsMemoForm.title = ''
  newsMemoForm.content = ''
  selectedTradeIdToLink.value = null
  selectedNewsTagId.value = null
  newNewsTagName.value = ''
  detailOpen.value = true
  void loadNewsConnections(row.id)
}

async function openReview(newsId: number) {
  const detail = await newsApi.detail(newsId)
  openDetail(detail)
}

function editNewsMemo(item: Memo) {
  newsMemoForm.id = item.id
  newsMemoForm.title = item.title ?? ''
  newsMemoForm.content = item.content
}

function resetNewsMemoForm() {
  newsMemoForm.id = null
  newsMemoForm.title = ''
  newsMemoForm.content = ''
}

async function saveNewsMemo() {
  if (!selectedNews.value || !newsMemoForm.content.trim()) return
  memoSubmitting.value = true
  try {
    if (newsMemoForm.id) {
      await memosApi.update(newsMemoForm.id, {
        title: newsMemoForm.title,
        content: newsMemoForm.content,
      })
    } else {
      await memosApi.create({
        memo_type: 'news',
        news_id: selectedNews.value.id,
        title: newsMemoForm.title,
        content: newsMemoForm.content,
      })
    }
    resetNewsMemoForm()
    await loadNewsConnections(selectedNews.value.id)
  } finally {
    memoSubmitting.value = false
  }
}

async function removeNewsMemo(memoId: number) {
  if (!selectedNews.value) return
  await memosApi.remove(memoId)
  await loadNewsConnections(selectedNews.value.id)
}

async function linkExistingNewsTag() {
  if (!selectedNews.value || !selectedNewsTagId.value) return
  tagSubmitting.value = true
  try {
    await memosApi.createTagLink({
      tag_id: selectedNewsTagId.value,
      target_type: 'news',
      target_id: selectedNews.value.id,
    })
    selectedNewsTagId.value = null
    await loadNewsConnections(selectedNews.value.id)
  } finally {
    tagSubmitting.value = false
  }
}

async function createAndLinkNewsTag() {
  if (!selectedNews.value || !newNewsTagName.value.trim()) return
  tagSubmitting.value = true
  try {
    const tag = await memosApi.createTag({
      name: newNewsTagName.value.trim(),
      tag_type: 'news',
    })
    await memosApi.createTagLink({
      tag_id: tag.id,
      target_type: 'news',
      target_id: selectedNews.value.id,
    })
    newNewsTagName.value = ''
    await loadNewsConnections(selectedNews.value.id)
  } finally {
    tagSubmitting.value = false
  }
}

async function removeNewsTag(tagId: number) {
  if (!selectedNews.value) return
  await memosApi.removeTagLink(tagId, 'news', selectedNews.value.id)
  await loadNewsConnections(selectedNews.value.id)
}

async function linkTradeToNews() {
  if (!selectedNews.value || !selectedTradeIdToLink.value) return
  tradeLinkSubmitting.value = true
  try {
    await tradesApi.linkNews(selectedTradeIdToLink.value, {
      news_id: selectedNews.value.id,
      link_type: 'reference',
    })
    selectedTradeIdToLink.value = null
    await loadNewsConnections(selectedNews.value.id)
  } finally {
    tradeLinkSubmitting.value = false
  }
}

async function unlinkTradeFromNews(tradeId: number) {
  if (!selectedNews.value) return
  await tradesApi.unlinkNews(tradeId, selectedNews.value.id)
  await loadNewsConnections(selectedNews.value.id)
}

async function saveReview() {
  if (!selectedNews.value) return
  savingReview.value = true
  try {
    await newsApi.updateReview(selectedNews.value.id, {
      gpt_filter_result: reviewForm.gpt_filter_result || null,
      gpt_filter_reason: reviewForm.gpt_filter_reason || null,
      is_alert_target: reviewForm.is_alert_target,
      filter_status: reviewForm.filter_status || null,
    })
    ElMessage.success('검수 결과를 저장했습니다.')
    detailOpen.value = false
    await loadData()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '검수 결과 저장에 실패했습니다.'
  } finally {
    savingReview.value = false
  }
}

watch(() => filters.market_scope, loadData)
watch(() => filters.gpt_summary_status, loadData)
watch(() => filters.gpt_filter_result, loadData)
watch(importanceFilter, loadData)
watch(publishedRange, loadData)
watch(gptTargetFilter, loadData)
watch(() => pagination.pageSize, () => {
  pagination.page = 1
})
watch(() => reviewPagination.pageSize, () => {
  reviewPagination.page = 1
})
watch(() => alertPagination.pageSize, () => {
  alertPagination.page = 1
})

onMounted(loadData)
</script>

<style lang="scss" scoped>
.news-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}


.news-tabs {
  min-width: 0;
}

.news-tabs :deep(.el-tabs__content) {
  overflow: visible;
}

.news-panel {
  display: flex;
  flex-direction: column;
  padding: 16px;
}

.review-panel {
  padding: 16px;
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.panel-head-title {
  display: flex;
  gap: 14px;
  align-items: baseline;
  flex-wrap: wrap;
}

.panel-head p {
  margin: 0;
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1.4;
}

.collect-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 0 0 auto;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.gpt-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 14px;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--surface-muted);
}

.gpt-actions > .muted {
  flex: 0 0 auto;
  margin-right: 8px;
  font-weight: 700;
}

.toolbar {
  display: flex;
  align-items: center;
  flex-wrap: nowrap;
  gap: 10px;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: #f5f7f4;
}

.toolbar > :deep(.el-input:first-child) {
  flex: 1 1 260px;
  min-width: 180px;
}

.toolbar > :deep(.el-input:nth-child(2)) {
  flex: 0 0 120px;
}

.toolbar > :deep(.el-select) {
  flex: 0 0 118px;
}

.toolbar > :deep(.el-input-number) {
  flex: 0 0 138px;
}

.toolbar > :deep(.el-date-editor) {
  flex: 1 1 300px;
  min-width: 260px;
}

.toolbar > :deep(.el-button) {
  flex: 0 0 88px;
}

.job-alert {
  margin: 12px 0;
}

.table-shell {
  height: 100%;
  min-height: 420px;
  overflow: hidden;
}

.news-table {
  height: 100%;
}

.table-footer {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 14px;
}

.stock-tag {
  margin: 2px 4px 2px 0;
}

.detail-body h3 {
  margin-top: 0;
}

.detail-body a {
  color: var(--primary);
  word-break: break-all;
}

.detail-body dl {
  display: grid;
  grid-template-columns: 100px 1fr;
  gap: 10px 12px;
  margin-top: 18px;
}

.detail-body dt {
  color: var(--text-muted);
}

.detail-body dd {
  margin: 0;
}

.review-editor {
  border-top: 1px solid var(--border);
  margin-top: 20px;
  padding-top: 16px;
}

.review-editor h4 {
  margin: 0 0 12px;
}

.link-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.link-row > * {
  flex: 1;
}

.tags-row > * {
  flex: 0 0 auto;
}

@media (max-width: 1100px) {
  .news-page,
  .news-panel {
    display: block;
    height: auto;
    overflow: visible;
  }

  .table-shell {
    height: 520px;
    min-height: 420px;
  }

  .panel-head,
  .toolbar,
  .collect-actions,
  .gpt-actions {
    display: block;
  }

  .toolbar > *,
  .collect-actions > *,
  .gpt-actions > * {
    margin-bottom: 8px;
    width: 100%;
  }

  .gpt-actions > .muted {
    display: block;
    margin: 0 0 8px;
  }

  .panel-head-title {
    display: block;
    margin-bottom: 8px;
  }

  .panel-head p {
    margin-top: 6px;
  }

  .table-footer {
    display: block;
  }
}
</style>
