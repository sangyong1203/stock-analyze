<template>
  <PageScaffold title="가격 차트" description="일봉/주봉/월봉, 이동평균, 보조지표, 매수/매도 지점을 함께 확인한다." badge="Charts" :metrics="metrics" />
</template>

<script setup lang="ts">
import PageScaffold from '@/shared/components/PageScaffold.vue'

const metrics = [
  { label: '차트 종목', value: '0개' },
  { label: '일봉 데이터', value: '0건' },
  { label: '거래 마커', value: '0건' },
  { label: '기업 이벤트', value: '0건' },
]
</script>
