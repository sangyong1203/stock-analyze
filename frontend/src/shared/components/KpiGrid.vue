<template>
  <div class="kpi-grid" :class="{ 'is-spaced': spaced }" :style="gridStyle">
    <article v-for="item in items" :key="item.key ?? item.label" class="kpi-card" :class="item.cardClass">
      <span>{{ item.label }}</span>
      <strong :class="item.tone">{{ item.value }}</strong>
    </article>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

export type KpiGridItem = {
  key?: string
  label: string
  value: string | number
  tone?: string
  cardClass?: string
}

const props = withDefaults(
  defineProps<{
    items: KpiGridItem[]
    columns?: number
    spaced?: boolean
  }>(),
  {
    columns: 4,
    spaced: false,
  },
)

const gridStyle = computed(() => ({
  '--kpi-columns': props.columns,
}))
</script>

<style scoped>
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(var(--kpi-columns), minmax(0, 1fr));
  gap: 12px;
}

.kpi-grid.is-spaced {
  margin-bottom: 16px;
}

.kpi-card {
  padding: 16px;
  border: 1px solid var(--border);
  background: var(--surface);
}

.kpi-card span {
  display: block;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
}

.kpi-card strong {
  display: block;
  margin-top: 8px;
  color: var(--text);
  font-size: 22px;
}

@media (max-width: 900px) {
  .kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
