<template>
  <section class="page-scaffold">
    <KpiGrid :items="metrics" :columns="4" />

    <div class="content-band toolbar">
      <el-input v-model="keyword" placeholder="검색어" clearable @clear="applyFilters" @keyup.enter="applyFilters" />
      <el-select v-model="status" placeholder="상태" @change="applyFilters">
        <el-option label="전체" value="all" />
        <el-option label="활성" value="active" />
        <el-option label="확인 필요" value="review" />
      </el-select>
      <el-button type="primary" @click="applyFilters">조회</el-button>
    </div>

    <div class="content-band table-band">
      <div class="band-head">
        <div class="band-head-title">
          <h2 class="section-title">{{ title }}</h2>
          <p class="panel-description">{{ description }}</p>
        </div>
        <el-tag effect="plain">{{ badge }}</el-tag>
      </div>

      <div class="table-shell">
        <el-table class="scaffold-table" :data="pagedRows" border height="100%">
          <el-table-column prop="name" label="항목" min-width="160" />
          <el-table-column prop="status" label="상태" width="130" />
          <el-table-column prop="value" label="값" min-width="140" />
          <el-table-column prop="change" label="변화" width="120">
            <template #default="{ row }">
              <span :class="row.change.startsWith('-') ? 'metric-fall' : 'metric-rise'">{{ row.change }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="table-footer">
        <span class="muted">총 {{ totalRows }}건 중 {{ pageStart }}-{{ pageEnd }}건 표시</span>
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          background
          layout="prev, pager, next, sizes"
          :total="totalRows"
          :page-sizes="[10, 20, 50]"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'

import KpiGrid from './KpiGrid.vue'

defineProps<{
  title: string
  description: string
  badge: string
  metrics: Array<{ label: string; value: string; tone?: string }>
}>()

const keyword = ref('')
const status = ref('all')
const pagination = reactive({
  page: 1,
  pageSize: 10,
})

const rows = [
  { name: '삼성전자', status: '관찰', value: '79,000', change: '+1.24%' },
  { name: 'SK하이닉스', status: '보유', value: '221,500', change: '-0.82%' },
  { name: '시장 뉴스', status: '검토', value: 'importance 7', change: '+3건' },
]

const totalRows = computed(() => rows.length)
const pageStart = computed(() => (totalRows.value === 0 ? 0 : (pagination.page - 1) * pagination.pageSize + 1))
const pageEnd = computed(() => Math.min(pagination.page * pagination.pageSize, totalRows.value))
const pagedRows = computed(() => {
  const start = (pagination.page - 1) * pagination.pageSize
  return rows.slice(start, start + pagination.pageSize)
})

function applyFilters() {
  pagination.page = 1
}
</script>

<style lang="scss" scoped>
.page-scaffold {
  display: flex;
  min-height: 0;
  height: 100%;
  flex-direction: column;
  gap: 16px;
}

.toolbar {
  display: grid;
  grid-template-columns: minmax(160px, 1fr) 160px auto;
  gap: 10px;
  padding: 12px;
}

.table-band {
  display: flex;
  min-height: 0;
  flex: 1;
  flex-direction: column;
  overflow: hidden;
  padding: 16px;
}

.band-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.band-head-title {
  display: flex;
  gap: 14px;
  align-items: baseline;
  flex-wrap: wrap;
}

.panel-description {
  margin: 0;
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1.4;
}

.table-shell {
  min-height: 260px;
  flex: 1;
  overflow: hidden;
}

.scaffold-table {
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

@media (max-width: 900px) {
  .page-scaffold,
  .table-band {
    display: block;
    height: auto;
    overflow: visible;
  }

  .toolbar {
    grid-template-columns: 1fr;
  }

  .table-shell {
    height: 520px;
    min-height: 420px;
  }

  .band-head,
  .table-footer {
    display: block;
  }

  .band-head-title {
    display: block;
    margin-bottom: 8px;
  }

  .panel-description {
    margin-top: 6px;
  }
}
</style>
