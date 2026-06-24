<template>
  <PageScaffold title="메모와 태그" description="종목, 거래, 뉴스, 차트, 일반 메모를 태그와 함께 관리한다." badge="Memos" :metrics="metrics" />
</template>

<script setup lang="ts">
import PageScaffold from '@/shared/components/PageScaffold.vue'

const metrics = [
  { label: '메모', value: '0건' },
  { label: '태그', value: '0개' },
  { label: '차트 메모', value: '0건' },
  { label: '일반 메모', value: '0건' },
]
</script>
