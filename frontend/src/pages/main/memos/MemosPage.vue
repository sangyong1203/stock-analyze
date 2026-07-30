<template>
  <section class="memos-page">
    <KpiGrid :items="kpiItems" :columns="4" />

    <div class="content-band memos-panel">
      <div class="panel-head">
        <div class="panel-head-title">
          <h2 class="section-title">메모와 태그</h2>
          <p class="muted">종목, 거래, 뉴스, 일반 메모를 태그와 함께 관리합니다.</p>
        </div>
        <div class="panel-actions">
          <el-button @click="openTagDialog()">태그 추가</el-button>
          <el-button type="primary" @click="openMemoDialog()">메모 추가</el-button>
        </div>
      </div>

      <div class="toolbar">
        <el-input v-model="keyword" placeholder="제목, 내용, 태그명 검색" clearable @keyup.enter="applyFilters" @clear="applyFilters" />
        <el-select v-model="memoTypeFilter" placeholder="메모 유형" clearable>
          <el-option label="종목" value="stock" />
          <el-option label="거래" value="trade" />
          <el-option label="뉴스" value="news" />
          <el-option label="일반" value="general" />
        </el-select>
        <el-select v-model="tagTypeFilter" placeholder="태그 유형" clearable>
          <el-option label="종목" value="stock" />
          <el-option label="거래" value="trade" />
          <el-option label="뉴스" value="news" />
          <el-option label="메모" value="memo" />
        </el-select>
        <el-button :loading="loading" @click="loadData">조회</el-button>
      </div>

      <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon :closable="false" />

      <el-tabs v-model="activeTab" class="memos-tabs">
        <el-tab-pane label="메모 목록" name="memos">
          <div class="table-shell">
            <el-table v-loading="loading" class="memos-table" :data="pagedMemos" border height="100%">
              <el-table-column label="제목" min-width="180" show-overflow-tooltip>
                <template #default="{ row }">{{ row.title || '제목 없음' }}</template>
              </el-table-column>
              <el-table-column label="내용" min-width="280" show-overflow-tooltip>
                <template #default="{ row }">{{ row.content || '-' }}</template>
              </el-table-column>
              <el-table-column label="태그" min-width="180">
                <template #default="{ row }">
                  <el-tag v-for="link in memoTagMap.get(row.id) ?? []" :key="link.id" class="tag-chip" effect="plain">
                    {{ link.tag_name }}
                  </el-tag>
                  <span v-if="!(memoTagMap.get(row.id)?.length)" class="muted">-</span>
                </template>
              </el-table-column>
              <el-table-column label="유형" width="100">
                <template #default="{ row }">{{ formatMemoType(row.memo_type) }}</template>
              </el-table-column>
              <el-table-column label="연결 대상" width="130">
                <template #default="{ row }">{{ formatMemoTarget(row) }}</template>
              </el-table-column>
              <el-table-column label="메모일" width="130">
                <template #default="{ row }">{{ formatDate(row.memo_date) }}</template>
              </el-table-column>
              <el-table-column label="관리" width="190" fixed="right">
                <template #default="{ row }">
                  <el-button link type="primary" @click="openMemoDialog(row)">수정</el-button>
                  <el-button link @click="openMemoTags(row)">태그</el-button>
                  <el-button link type="danger" @click="removeMemo(row.id)">삭제</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <div class="table-footer">
            <span class="muted">총 {{ totalFilteredMemos }}건 중 {{ memoPageStart }}-{{ memoPageEnd }}건 표시</span>
            <el-pagination
              v-model:current-page="memoPagination.page"
              v-model:page-size="memoPagination.pageSize"
              background
              layout="prev, pager, next, sizes"
              :total="totalFilteredMemos"
              :page-sizes="[50, 100, 200]"
            />
          </div>
        </el-tab-pane>

        <el-tab-pane label="태그 목록" name="tags">
          <div class="table-shell">
            <el-table v-loading="loading" class="memos-table" :data="pagedTags" border height="100%">
              <el-table-column label="태그명" min-width="220">
                <template #default="{ row }">
                  <el-tag :color="row.color || undefined" effect="plain">{{ row.name }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="유형" width="120">
                <template #default="{ row }">{{ formatTagType(row.tag_type) }}</template>
              </el-table-column>
              <el-table-column label="색상" width="120">
                <template #default="{ row }">{{ row.color || '-' }}</template>
              </el-table-column>
              <el-table-column label="생성일" width="160">
                <template #default="{ row }">{{ formatDateTime(row.created_at) }}</template>
              </el-table-column>
              <el-table-column label="관리" width="130" fixed="right">
                <template #default="{ row }">
                  <el-button link type="primary" @click="openTagDialog(row)">수정</el-button>
                  <el-button link type="danger" @click="removeTag(row.id)">삭제</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <div class="table-footer">
            <span class="muted">총 {{ totalFilteredTags }}건 중 {{ tagPageStart }}-{{ tagPageEnd }}건 표시</span>
            <el-pagination
              v-model:current-page="tagPagination.page"
              v-model:page-size="tagPagination.pageSize"
              background
              layout="prev, pager, next, sizes"
              :total="totalFilteredTags"
              :page-sizes="[50, 100, 200]"
            />
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <el-dialog v-model="memoDialogOpen" :title="editingMemoId ? '메모 수정' : '메모 추가'" width="620px">
      <el-form label-position="top" @submit.prevent>
        <el-form-item label="메모 유형">
          <el-select v-model="memoForm.memo_type">
            <el-option label="종목" value="stock" />
            <el-option label="거래" value="trade" />
            <el-option label="뉴스" value="news" />
            <el-option label="일반" value="general" />
          </el-select>
        </el-form-item>
        <div class="form-grid">
          <el-form-item label="종목 ID">
            <el-input-number v-model="memoForm.stock_id" :min="1" :disabled="memoForm.memo_type !== 'stock'" />
          </el-form-item>
          <el-form-item label="거래 ID">
            <el-input-number v-model="memoForm.trade_id" :min="1" :disabled="memoForm.memo_type !== 'trade'" />
          </el-form-item>
          <el-form-item label="뉴스 ID">
            <el-input-number v-model="memoForm.news_id" :min="1" :disabled="memoForm.memo_type !== 'news'" />
          </el-form-item>
          <el-form-item label="메모일">
            <el-date-picker v-model="memoForm.memo_date" type="date" value-format="YYYY-MM-DD" />
          </el-form-item>
        </div>
        <el-form-item label="제목">
          <el-input v-model="memoForm.title" />
        </el-form-item>
        <el-form-item label="내용">
          <el-input v-model="memoForm.content" type="textarea" :rows="5" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="memoDialogOpen = false">취소</el-button>
        <el-button type="primary" :loading="saving" @click="saveMemo">저장</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="tagDialogOpen" :title="editingTagId ? '태그 수정' : '태그 추가'" width="480px">
      <el-form label-position="top" @submit.prevent>
        <el-form-item label="태그명">
          <el-input v-model="tagForm.name" />
        </el-form-item>
        <el-form-item label="태그 유형">
          <el-select v-model="tagForm.tag_type">
            <el-option label="종목" value="stock" />
            <el-option label="거래" value="trade" />
            <el-option label="뉴스" value="news" />
            <el-option label="메모" value="memo" />
          </el-select>
        </el-form-item>
        <el-form-item label="색상">
          <el-input v-model="tagForm.color" placeholder="#3b82f6" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="tagDialogOpen = false">취소</el-button>
        <el-button type="primary" :loading="saving" @click="saveTag">저장</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="memoTagsDialogOpen" title="메모 태그 관리" width="520px">
      <div v-if="selectedMemo" class="tag-manager">
        <h3>{{ selectedMemo.title || '제목 없음' }}</h3>
        <div class="tag-list">
          <el-tag v-for="link in selectedMemoTagLinks" :key="link.id" closable effect="plain" @close="unlinkMemoTag(link.tag_id)">
            {{ link.tag_name }}
          </el-tag>
          <span v-if="selectedMemoTagLinks.length === 0" class="muted">연결된 태그가 없습니다.</span>
        </div>
        <div class="link-row">
          <el-select v-model="selectedTagId" placeholder="연결할 태그" clearable filterable>
            <el-option v-for="tag in memoTags" :key="tag.id" :label="tag.name" :value="tag.id" />
          </el-select>
          <el-button type="primary" :disabled="!selectedTagId" :loading="saving" @click="linkMemoTag">태그 연결</el-button>
        </div>
      </div>
    </el-dialog>
  </section>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, onMounted, reactive, ref, watch } from 'vue'

import KpiGrid from '@/shared/components/KpiGrid.vue'

import { memosApi } from './service/memos.api'
import type { Memo, MemoPayload, MemoType, Tag, TagLink, TagPayload } from './service/memos.types'

const loading = ref(false)
const saving = ref(false)
const errorMessage = ref('')
const activeTab = ref('memos')
const keyword = ref('')
const memoTypeFilter = ref<MemoType | ''>('')
const tagTypeFilter = ref('')
const memos = ref<Memo[]>([])
const tags = ref<Tag[]>([])
const tagLinks = ref<TagLink[]>([])
const memoDialogOpen = ref(false)
const tagDialogOpen = ref(false)
const memoTagsDialogOpen = ref(false)
const editingMemoId = ref<number | null>(null)
const editingTagId = ref<number | null>(null)
const selectedMemo = ref<Memo | null>(null)
const selectedTagId = ref<number | null>(null)

const memoPagination = reactive({ page: 1, pageSize: 50 })
const tagPagination = reactive({ page: 1, pageSize: 50 })

const memoForm = reactive<MemoPayload>({
  memo_type: 'general',
  title: '',
  content: '',
  stock_id: null,
  trade_id: null,
  news_id: null,
  memo_date: null,
  context_json: null,
})

const tagForm = reactive<TagPayload>({
  name: '',
  color: '',
  tag_type: 'memo',
})

const memoTagMap = computed(() => {
  const map = new Map<number, TagLink[]>()
  for (const link of tagLinks.value) {
    if (link.target_type !== 'memo') continue
    const links = map.get(link.target_id) ?? []
    links.push(link)
    map.set(link.target_id, links)
  }
  return map
})

const selectedMemoTagLinks = computed(() => (selectedMemo.value ? memoTagMap.value.get(selectedMemo.value.id) ?? [] : []))
const memoTags = computed(() => tags.value.filter((tag) => tag.tag_type === 'memo'))

const filteredMemos = computed(() => {
  const normalizedKeyword = keyword.value.trim().toLowerCase()
  return memos.value.filter((memo) => {
    const tagNames = memoTagMap.value.get(memo.id)?.map((link) => link.tag_name).join(' ') ?? ''
    const matchesKeyword =
      !normalizedKeyword ||
      [memo.title, memo.content, tagNames].some((value) => String(value ?? '').toLowerCase().includes(normalizedKeyword))
    const matchesType = !memoTypeFilter.value || memo.memo_type === memoTypeFilter.value
    return matchesKeyword && matchesType
  })
})

const filteredTags = computed(() => {
  const normalizedKeyword = keyword.value.trim().toLowerCase()
  return tags.value.filter((tag) => {
    const matchesKeyword = !normalizedKeyword || tag.name.toLowerCase().includes(normalizedKeyword)
    const matchesType = !tagTypeFilter.value || tag.tag_type === tagTypeFilter.value
    return matchesKeyword && matchesType
  })
})

const totalFilteredMemos = computed(() => filteredMemos.value.length)
const memoPageStart = computed(() =>
  totalFilteredMemos.value === 0 ? 0 : (memoPagination.page - 1) * memoPagination.pageSize + 1,
)
const memoPageEnd = computed(() => Math.min(memoPagination.page * memoPagination.pageSize, totalFilteredMemos.value))
const pagedMemos = computed(() => {
  const start = (memoPagination.page - 1) * memoPagination.pageSize
  return filteredMemos.value.slice(start, start + memoPagination.pageSize)
})

const totalFilteredTags = computed(() => filteredTags.value.length)
const tagPageStart = computed(() =>
  totalFilteredTags.value === 0 ? 0 : (tagPagination.page - 1) * tagPagination.pageSize + 1,
)
const tagPageEnd = computed(() => Math.min(tagPagination.page * tagPagination.pageSize, totalFilteredTags.value))
const pagedTags = computed(() => {
  const start = (tagPagination.page - 1) * tagPagination.pageSize
  return filteredTags.value.slice(start, start + tagPagination.pageSize)
})

const kpiItems = computed(() => [
  { label: '전체 메모', value: memos.value.length },
  { label: '전체 태그', value: tags.value.length },
  { label: '메모 태그', value: memoTags.value.length },
  { label: '태그 연결', value: tagLinks.value.length },
])

async function loadData() {
  loading.value = true
  errorMessage.value = ''
  try {
    const [memoRows, tagRows, linkRows] = await Promise.all([
      memosApi.list({}),
      memosApi.listTags(),
      memosApi.listTagLinks('memo'),
    ])
    memos.value = memoRows
    tags.value = tagRows
    tagLinks.value = linkRows
    memoPagination.page = 1
    tagPagination.page = 1
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '메모와 태그 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

function applyFilters() {
  memoPagination.page = 1
  tagPagination.page = 1
}

function resetMemoForm() {
  editingMemoId.value = null
  Object.assign(memoForm, {
    memo_type: 'general',
    title: '',
    content: '',
    stock_id: null,
    trade_id: null,
    news_id: null,
    memo_date: null,
    context_json: null,
  })
}

function resetTagForm() {
  editingTagId.value = null
  Object.assign(tagForm, {
    name: '',
    color: '',
    tag_type: 'memo',
  })
}

function openMemoDialog(memo?: Memo) {
  resetMemoForm()
  if (memo) {
    editingMemoId.value = memo.id
    Object.assign(memoForm, {
      memo_type: memo.memo_type,
      title: memo.title ?? '',
      content: memo.content,
      stock_id: memo.stock_id ?? null,
      trade_id: memo.trade_id ?? null,
      news_id: memo.news_id ?? null,
      memo_date: memo.memo_date ?? null,
      context_json: memo.context_json ?? null,
    })
  }
  memoDialogOpen.value = true
}

function openTagDialog(tag?: Tag) {
  resetTagForm()
  if (tag) {
    editingTagId.value = tag.id
    Object.assign(tagForm, {
      name: tag.name,
      color: tag.color ?? '',
      tag_type: tag.tag_type,
    })
  }
  tagDialogOpen.value = true
}

function toMemoPayload(): MemoPayload {
  return {
    memo_type: memoForm.memo_type,
    title: memoForm.title?.trim() || null,
    content: memoForm.content.trim(),
    stock_id: memoForm.memo_type === 'stock' ? memoForm.stock_id : null,
    trade_id: memoForm.memo_type === 'trade' ? memoForm.trade_id : null,
    news_id: memoForm.memo_type === 'news' ? memoForm.news_id : null,
    memo_date: memoForm.memo_date || null,
    context_json: memoForm.context_json ?? null,
  }
}

async function saveMemo() {
  const payload = toMemoPayload()
  if (!payload.content) {
    ElMessage.warning('메모 내용을 입력해 주세요.')
    return
  }
  saving.value = true
  try {
    if (editingMemoId.value) {
      await memosApi.update(editingMemoId.value, payload)
      ElMessage.success('메모를 수정했습니다.')
    } else {
      await memosApi.create(payload)
      ElMessage.success('메모를 추가했습니다.')
    }
    memoDialogOpen.value = false
    await loadData()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '메모 저장에 실패했습니다.'
  } finally {
    saving.value = false
  }
}

async function removeMemo(memoId: number) {
  try {
    await ElMessageBox.confirm('메모를 삭제할까요?', '메모 삭제', { type: 'warning' })
  } catch {
    return
  }
  await memosApi.remove(memoId)
  ElMessage.success('메모를 삭제했습니다.')
  await loadData()
}

async function saveTag() {
  const payload = {
    name: tagForm.name.trim(),
    color: tagForm.color?.trim() || null,
    tag_type: tagForm.tag_type,
  }
  if (!payload.name) {
    ElMessage.warning('태그명을 입력해 주세요.')
    return
  }
  saving.value = true
  try {
    if (editingTagId.value) {
      await memosApi.updateTag(editingTagId.value, payload)
      ElMessage.success('태그를 수정했습니다.')
    } else {
      await memosApi.createTag(payload)
      ElMessage.success('태그를 추가했습니다.')
    }
    tagDialogOpen.value = false
    await loadData()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '태그 저장에 실패했습니다.'
  } finally {
    saving.value = false
  }
}

async function removeTag(tagId: number) {
  try {
    await ElMessageBox.confirm('태그를 삭제할까요? 연결된 태그 링크도 영향을 받을 수 있습니다.', '태그 삭제', { type: 'warning' })
  } catch {
    return
  }
  await memosApi.removeTag(tagId)
  ElMessage.success('태그를 삭제했습니다.')
  await loadData()
}

function openMemoTags(memo: Memo) {
  selectedMemo.value = memo
  selectedTagId.value = null
  memoTagsDialogOpen.value = true
}

async function linkMemoTag() {
  if (!selectedMemo.value || !selectedTagId.value) return
  if (selectedMemoTagLinks.value.some((link) => link.tag_id === selectedTagId.value)) {
    ElMessage.warning('이미 연결된 태그입니다.')
    return
  }
  saving.value = true
  try {
    await memosApi.createTagLink({
      tag_id: selectedTagId.value,
      target_type: 'memo',
      target_id: selectedMemo.value.id,
    })
    selectedTagId.value = null
    await loadData()
  } finally {
    saving.value = false
  }
}

async function unlinkMemoTag(tagId: number) {
  if (!selectedMemo.value) return
  await memosApi.removeTagLink(tagId, 'memo', selectedMemo.value.id)
  await loadData()
}

function formatMemoType(type: string) {
  const labels: Record<string, string> = { stock: '종목', trade: '거래', news: '뉴스', general: '일반' }
  return labels[type] ?? type
}

function formatTagType(type: string) {
  const labels: Record<string, string> = { stock: '종목', trade: '거래', news: '뉴스', memo: '메모' }
  return labels[type] ?? type
}

function formatMemoTarget(memo: Memo) {
  if (memo.stock_id) return `종목 #${memo.stock_id}`
  if (memo.trade_id) return `거래 #${memo.trade_id}`
  if (memo.news_id) return `뉴스 #${memo.news_id}`
  return '-'
}

function formatDate(value?: string | null) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleDateString('ko-KR')
}

function formatDateTime(value?: string | null) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString('ko-KR')
}

watch([keyword, memoTypeFilter, tagTypeFilter], applyFilters)
watch(() => memoForm.memo_type, (type) => {
  if (type !== 'stock') memoForm.stock_id = null
  if (type !== 'trade') memoForm.trade_id = null
  if (type !== 'news') memoForm.news_id = null
})
watch(() => memoPagination.pageSize, () => {
  memoPagination.page = 1
})
watch(() => tagPagination.pageSize, () => {
  tagPagination.page = 1
})

onMounted(loadData)
</script>

<style lang="scss" scoped>
.memos-page {
  display: flex;
  min-height: 0;
  flex-direction: column;
  gap: 16px;
}

.memos-panel {
  display: flex;
  min-height: 0;
  flex: 1;
  flex-direction: column;
  padding: 16px;
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
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

.panel-actions,
.toolbar,
.link-row,
.tag-list {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.toolbar {
  margin-bottom: 14px;
}

.toolbar > :deep(.el-input) {
  flex: 1 1 320px;
}

.toolbar > :deep(.el-select) {
  flex: 0 0 150px;
}

.toolbar > :deep(.el-button) {
  flex: 0 0 88px;
}

.memos-tabs {
  min-width: 0;
}

.memos-tabs :deep(.el-tabs__content) {
  overflow: visible;
}

.table-shell {
  height: 520px;
  min-height: 420px;
  overflow: hidden;
}

.memos-table {
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

.tag-chip {
  margin: 2px 4px 2px 0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.tag-manager h3 {
  margin: 0 0 12px;
}

.tag-list {
  min-height: 34px;
  margin-bottom: 14px;
}

.link-row > :deep(.el-select) {
  flex: 1;
}

@media (max-width: 900px) {
  .memos-page,
  .memos-panel {
    display: block;
    height: auto;
    overflow: visible;
  }

  .panel-head,
  .panel-head-title,
  .toolbar,
  .table-footer,
  .form-grid {
    display: block;
  }

  .toolbar > *,
  .panel-actions > *,
  .link-row > * {
    width: 100%;
    margin-bottom: 8px;
  }

  .table-shell {
    height: 520px;
    min-height: 420px;
  }
}
</style>
