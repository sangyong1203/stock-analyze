<template>
  <PageScaffold title="알림 관리" description="가격 알림, 뉴스 알림 기준, 발송 이력과 실패 이력을 관리한다." badge="Alerts" :metrics="metrics" />
</template>

<script setup lang="ts">
import PageScaffold from '@/shared/components/PageScaffold.vue'

const metrics = [
  { label: '가격 알림', value: '0개' },
  { label: '뉴스 알림', value: 'ON' },
  { label: '오늘 발송', value: '0건' },
  { label: '실패 이력', value: '0건' },
]
</script>
