<template>
  <PageScaffold title="거래 기록" description="매수/매도 가격, 수량, 판단 사유, 관련 뉴스, 메모와 태그를 기록한다." badge="Trades" :metrics="metrics" />
</template>

<script setup lang="ts">
import PageScaffold from '@/shared/components/PageScaffold.vue'

const metrics = [
  { label: '매수 기록', value: '0건' },
  { label: '매도 기록', value: '0건' },
  { label: '뉴스 연결', value: '0건' },
  { label: '손익 계산', value: '대기' },
]
</script>
