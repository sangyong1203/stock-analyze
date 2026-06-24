<template>
  <PageScaffold title="자금 및 보유현황" description="투자금 풀, 현금 흐름, 평균단가 방식 보유현황을 확인한다." badge="Portfolio" :metrics="metrics" />
</template>

<script setup lang="ts">
import PageScaffold from '@/shared/components/PageScaffold.vue'

const metrics = [
  { label: '현금 잔액', value: '0원' },
  { label: '평가금액', value: '0원' },
  { label: '평가손익', value: '+0원', tone: 'metric-rise' },
  { label: '실현손익', value: '0원' },
]
</script>
