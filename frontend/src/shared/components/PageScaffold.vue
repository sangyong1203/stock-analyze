<template>
  <section>
    <div class="kpi-grid">
      <article v-for="item in metrics" :key="item.label" class="kpi-item">
        <span>{{ item.label }}</span>
        <strong :class="item.tone">{{ item.value }}</strong>
      </article>
    </div>

    <div class="content-band toolbar">
      <el-input v-model="keyword" placeholder="검색어" clearable />
      <el-select v-model="status" placeholder="상태">
        <el-option label="전체" value="all" />
        <el-option label="활성" value="active" />
        <el-option label="확인 필요" value="review" />
      </el-select>
      <el-button type="primary">조회</el-button>
    </div>

    <div class="content-band table-band">
      <div class="band-head">
        <div>
          <h2 class="section-title">{{ title }}</h2>
          <p class="muted">{{ description }}</p>
        </div>
        <el-tag effect="plain">{{ badge }}</el-tag>
      </div>

      <el-table :data="rows" border>
        <el-table-column prop="name" label="항목" min-width="160" />
        <el-table-column prop="status" label="상태" width="130" />
        <el-table-column prop="value" label="값" min-width="140" />
        <el-table-column prop="change" label="변동" width="120">
          <template #default="{ row }">
            <span :class="row.change.startsWith('-') ? 'metric-fall' : 'metric-rise'">{{ row.change }}</span>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  title: string
  description: string
  badge: string
  metrics: Array<{ label: string; value: string; tone?: string }>
}>()

const keyword = ref('')
const status = ref('all')

const rows = [
  { name: '삼성전자', status: '관찰', value: '79,000', change: '+1.24%' },
  { name: 'SK하이닉스', status: '보유', value: '221,500', change: '-0.82%' },
  { name: '시장 뉴스', status: '검토', value: 'importance 7', change: '+3건' },
]
</script>

<style scoped>
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin-top: 18px;
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

.toolbar {
  display: grid;
  grid-template-columns: minmax(160px, 1fr) 160px auto;
  gap: 10px;
  padding: 12px;
}

.table-band {
  padding: 16px;
}

.band-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.band-head p {
  margin: 6px 0 0;
}

@media (max-width: 900px) {
  .kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .toolbar {
    grid-template-columns: 1fr;
  }
}
</style>
