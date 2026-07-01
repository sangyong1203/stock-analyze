<template>
  <section class="dashboard-page">
    <div class="hero">
      <div>
        <p class="eyebrow">Dashboard</p>
        <h1>투자 현황 요약</h1>
        <p class="hero-copy">포트폴리오, 보유 종목, 최근 거래와 뉴스, 알림 상태를 한 화면에서 확인합니다.</p>
      </div>
      <div class="quick-actions">
        <el-button @click="goTo('/trades')">거래 기록</el-button>
        <el-button @click="goTo('/portfolio')">포트폴리오</el-button>
        <el-button @click="goTo('/news')">뉴스</el-button>
        <el-button @click="goTo('/alerts')">알림</el-button>
        <el-button @click="goTo('/charts')">차트</el-button>
      </div>
    </div>

    <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon :closable="false" />

    <div v-if="loading" class="loading-block">
      <el-skeleton animated :rows="10" />
    </div>

    <template v-else-if="summary">
      <div class="kpi-grid">
        <article class="kpi-card">
          <span>총 자산</span>
          <strong>{{ formatKrw(summary.portfolio_summary.total_asset_value) }}</strong>
        </article>
        <article class="kpi-card">
          <span>현금 잔고</span>
          <strong>{{ formatKrw(summary.portfolio_summary.total_cash) }}</strong>
        </article>
        <article class="kpi-card">
          <span>평가 손익</span>
          <strong :class="toneClass(summary.portfolio_summary.total_unrealized_profit_loss)">
            {{ formatSignedKrw(summary.portfolio_summary.total_unrealized_profit_loss) }}
          </strong>
        </article>
        <article class="kpi-card">
          <span>평가 손익률</span>
          <strong :class="toneClass(summary.portfolio_summary.total_unrealized_profit_loss)">
            {{ formatPercent(summary.portfolio_summary.total_unrealized_profit_loss_rate) }}
          </strong>
        </article>
        <article class="kpi-card">
          <span>보유 종목</span>
          <strong>{{ summary.portfolio_summary.holding_count }}</strong>
        </article>
        <article class="kpi-card">
          <span>금일 변동</span>
          <strong :class="toneClass(summary.portfolio_summary.today_change_amount)">
            {{ formatSignedKrw(summary.portfolio_summary.today_change_amount) }}
          </strong>
        </article>
      </div>

      <div class="dashboard-grid">
        <section class="panel span-2">
          <div class="panel-head">
            <div>
              <h2>포트폴리오 요약</h2>
              <p class="muted">현재 자산 배분과 실현/평가 손익 상태입니다.</p>
            </div>
          </div>
          <div class="summary-grid">
            <div class="summary-item">
              <span>총 매수금액</span>
              <strong>{{ formatKrw(summary.portfolio_summary.total_invested_amount) }}</strong>
            </div>
            <div class="summary-item">
              <span>총 평가금액</span>
              <strong>{{ formatKrw(summary.portfolio_summary.total_market_value) }}</strong>
            </div>
            <div class="summary-item">
              <span>실현 손익</span>
              <strong :class="toneClass(summary.portfolio_summary.realized_profit_loss)">
                {{ formatSignedKrw(summary.portfolio_summary.realized_profit_loss) }}
              </strong>
            </div>
            <div class="summary-item">
              <span>금일 수익률</span>
              <strong :class="toneClass(summary.portfolio_summary.today_change_amount)">
                {{ formatPercent(summary.portfolio_summary.today_change_rate) }}
              </strong>
            </div>
          </div>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <h2>알림 요약</h2>
              <p class="muted">가격 알림과 뉴스 알림 후보 상태입니다.</p>
            </div>
          </div>
          <ul class="simple-list compact">
            <li>
              <span>가격 알림 활성</span>
              <strong>{{ summary.price_alert_summary.enabled_count }}</strong>
            </li>
            <li>
              <span>가격 알림 발송</span>
              <strong>{{ summary.price_alert_summary.sent_count }}</strong>
            </li>
            <li>
              <span>뉴스 알림 후보</span>
              <strong>{{ summary.news_alert_summary.alert_target_count }}</strong>
            </li>
            <li>
              <span>중요 뉴스</span>
              <strong>{{ summary.news_alert_summary.important_count }}</strong>
            </li>
          </ul>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <h2>메모 / 태그</h2>
              <p class="muted">최근 메모와 많이 사용한 태그입니다.</p>
            </div>
          </div>
          <div class="tag-wrap">
            <el-tag v-for="tag in summary.memo_summary.top_tags" :key="tag.id" :style="tagStyle(tag.color)">
              {{ tag.name }} · {{ tag.usage_count }}
            </el-tag>
            <span v-if="summary.memo_summary.top_tags.length === 0" class="muted">태그가 없습니다.</span>
          </div>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <h2>보유 종목 TOP 5</h2>
              <p class="muted">평가금액 기준 상위 보유 종목입니다.</p>
            </div>
          </div>
          <el-table :data="summary.top_holdings" size="small" border>
            <el-table-column label="종목" min-width="150">
              <template #default="{ row }">
                <div class="stack">
                  <strong>{{ row.stock_name }}</strong>
                  <small>{{ row.stock_code }}</small>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="수량" width="80" />
            <el-table-column label="평가금액" min-width="130">
              <template #default="{ row }">{{ formatKrw(row.market_value) }}</template>
            </el-table-column>
          </el-table>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <h2>수익률 TOP / 하위</h2>
              <p class="muted">보유 종목의 평가손익률 상위와 하위 목록입니다.</p>
            </div>
          </div>
          <div class="dual-list">
            <div>
              <h3>상위 5</h3>
              <ul class="simple-list">
                <li v-for="item in summary.top_gainers" :key="`gain-${item.stock_id}`">
                  <span>{{ item.stock_name }}</span>
                  <strong class="metric-rise">{{ formatPercent(item.unrealized_profit_loss_rate) }}</strong>
                </li>
              </ul>
            </div>
            <div>
              <h3>하위 5</h3>
              <ul class="simple-list">
                <li v-for="item in summary.top_losers" :key="`loss-${item.stock_id}`">
                  <span>{{ item.stock_name }}</span>
                  <strong class="metric-fall">{{ formatPercent(item.unrealized_profit_loss_rate) }}</strong>
                </li>
              </ul>
            </div>
          </div>
        </section>

        <section class="panel span-2">
          <div class="panel-head">
            <div>
              <h2>최근 거래</h2>
              <p class="muted">최근 5건의 매수 / 매도 기록입니다.</p>
            </div>
          </div>
          <el-table :data="summary.recent_trades" size="small" border>
            <el-table-column prop="trade_date" label="거래일" width="110" />
            <el-table-column label="종목" min-width="160">
              <template #default="{ row }">
                <div class="stack">
                  <strong>{{ row.stock_name }}</strong>
                  <small>{{ row.stock_code }}</small>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="trade_type" label="구분" width="80" />
            <el-table-column prop="quantity" label="수량" width="80" />
            <el-table-column label="가격" width="120">
              <template #default="{ row }">{{ formatKrw(row.price) }}</template>
            </el-table-column>
            <el-table-column prop="fund_pool_name" label="자금 풀" min-width="120" />
            <el-table-column prop="memo" label="메모" min-width="180" show-overflow-tooltip />
          </el-table>
        </section>

        <section class="panel span-2">
          <div class="panel-head">
            <div>
              <h2>최근 뉴스</h2>
              <p class="muted">최근 5건의 수집 뉴스와 중요도 상태입니다.</p>
            </div>
          </div>
          <el-table :data="summary.recent_news" size="small" border>
            <el-table-column label="발행시각" width="150">
              <template #default="{ row }">{{ formatDateTime(row.published_at) }}</template>
            </el-table-column>
            <el-table-column prop="title" label="제목" min-width="260" show-overflow-tooltip />
            <el-table-column prop="source" label="출처" width="120" />
            <el-table-column prop="importance_score" label="중요도" width="90" />
            <el-table-column prop="gpt_summary_status" label="GPT 요약" width="110" />
            <el-table-column label="알림 후보" width="100">
              <template #default="{ row }">
                <el-tag :type="row.is_alert_target ? 'danger' : 'info'" effect="plain">
                  {{ row.is_alert_target ? '대상' : '제외' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <h2>최근 알림 이력</h2>
              <p class="muted">가격 / 뉴스 알림 최근 상태입니다.</p>
            </div>
          </div>
          <ul class="simple-list">
            <li v-for="item in summary.recent_alert_histories" :key="item.id">
              <div class="stack">
                <strong>{{ item.title }}</strong>
                <small>{{ item.alert_type }} · {{ item.status }} · {{ formatDateTime(item.created_at) }}</small>
              </div>
            </li>
            <li v-if="summary.recent_alert_histories.length === 0" class="empty-line">알림 이력이 없습니다.</li>
          </ul>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <h2>최근 메모</h2>
              <p class="muted">최신 메모 5건입니다.</p>
            </div>
          </div>
          <ul class="simple-list">
            <li v-for="item in summary.memo_summary.recent_memos" :key="item.id">
              <div class="stack">
                <strong>{{ item.title || item.content.slice(0, 36) }}</strong>
                <small>{{ item.target_type }} · {{ item.target_label || '-' }} · {{ formatDateTime(item.created_at) }}</small>
              </div>
            </li>
            <li v-if="summary.memo_summary.recent_memos.length === 0" class="empty-line">메모가 없습니다.</li>
          </ul>
        </section>
      </div>
    </template>
  </section>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { dashboardApi } from './service/dashboard.api'
import type { DashboardSummary } from './service/dashboard.types'
import { formatDateTime, formatKrw, formatPercent, formatSignedKrw, toNumber } from './service/dashboard.utils'

const router = useRouter()
const loading = ref(false)
const errorMessage = ref('')
const summary = ref<DashboardSummary | null>(null)

function toneClass(value: string | number | null | undefined) {
  const numeric = toNumber(value)
  if (numeric > 0) return 'metric-rise'
  if (numeric < 0) return 'metric-fall'
  return ''
}

function tagStyle(color: string | null | undefined) {
  if (!color) return {}
  return {
    borderColor: color,
    color,
  }
}

function goTo(path: string) {
  void router.push(path)
}

async function loadSummary() {
  loading.value = true
  errorMessage.value = ''
  try {
    summary.value = await dashboardApi.summary()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '대시보드 정보를 불러오지 못했습니다.'
    ElMessage.error('대시보드 로딩에 실패했습니다.')
  } finally {
    loading.value = false
  }
}

onMounted(loadSummary)
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 18px;
}

.hero {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 28px;
  border: 1px solid var(--border);
  background:
    radial-gradient(circle at top right, rgba(37, 99, 235, 0.12), transparent 35%),
    linear-gradient(135deg, rgba(15, 23, 42, 0.04), rgba(148, 163, 184, 0.08)),
    var(--surface);
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #1d4ed8;
}

.hero h1 {
  margin: 0;
  font-size: 30px;
}

.hero-copy {
  margin: 10px 0 0;
  max-width: 640px;
  color: var(--text-muted);
}

.quick-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-content: flex-start;
  justify-content: flex-end;
}

.loading-block {
  padding: 20px;
  border: 1px solid var(--border);
  background: var(--surface);
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 12px;
}

.kpi-card,
.panel {
  border: 1px solid var(--border);
  background: var(--surface);
}

.kpi-card {
  padding: 18px;
}

.kpi-card span,
.summary-item span {
  display: block;
  color: var(--text-muted);
  font-size: 12px;
}

.kpi-card strong,
.summary-item strong {
  display: block;
  margin-top: 8px;
  font-size: 24px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.panel {
  padding: 18px;
}

.span-2 {
  grid-column: span 2;
}

.panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.panel-head h2 {
  margin: 0;
  font-size: 18px;
}

.muted {
  color: var(--text-muted);
}

.panel-head .muted {
  margin: 4px 0 0;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.summary-item {
  padding: 14px;
  border: 1px solid rgba(148, 163, 184, 0.18);
  background: rgba(248, 250, 252, 0.8);
}

.simple-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 0;
  margin: 0;
  list-style: none;
}

.simple-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.16);
}

.simple-list li:last-child {
  border-bottom: 0;
  padding-bottom: 0;
}

.compact li strong {
  font-size: 18px;
}

.stack {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stack small {
  color: var(--text-muted);
}

.tag-wrap {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.dual-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.dual-list h3 {
  margin: 0 0 10px;
  font-size: 14px;
}

.metric-rise {
  color: #b91c1c;
}

.metric-fall {
  color: #1d4ed8;
}

.empty-line {
  color: var(--text-muted);
  justify-content: flex-start;
}

@media (max-width: 1200px) {
  .kpi-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .dashboard-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .span-2 {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .hero {
    flex-direction: column;
  }

  .quick-actions {
    justify-content: flex-start;
  }

  .kpi-grid,
  .dashboard-grid,
  .summary-grid,
  .dual-list {
    grid-template-columns: 1fr;
  }

  .span-2 {
    grid-column: span 1;
  }
}
</style>
