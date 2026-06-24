<template>
  <PageScaffold title="투자 현황 요약" description="자금, 보유평가, 중요 뉴스, 목표가 접근 종목을 한 화면에서 확인한다." badge="Dashboard" :metrics="metrics" />
</template>

<script setup lang="ts">
import PageScaffold from '@/shared/components/PageScaffold.vue'

const metrics = [
  { label: '총 투자금', value: '0원' },
  { label: '현금 잔액', value: '0원' },
  { label: '평가손익', value: '+0.00%', tone: 'metric-rise' },
  { label: '알림 후보', value: '0건' },
]
</script>
