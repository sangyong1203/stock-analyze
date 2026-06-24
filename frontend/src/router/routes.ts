import type { RouteRecordRaw } from 'vue-router'

import MainLayout from '@/layouts/MainLayout.vue'
import LoginPage from '@/pages/login/LoginPage.vue'
import AlertsPage from '@/pages/main/alerts/AlertsPage.vue'
import ChartsPage from '@/pages/main/charts/ChartsPage.vue'
import CollectionPage from '@/pages/main/collection/CollectionPage.vue'
import DashboardPage from '@/pages/main/dashboard/DashboardPage.vue'
import MemosPage from '@/pages/main/memos/MemosPage.vue'
import NewsPage from '@/pages/main/news/NewsPage.vue'
import PortfolioPage from '@/pages/main/portfolio/PortfolioPage.vue'
import SettingsPage from '@/pages/main/settings/SettingsPage.vue'
import StocksPage from '@/pages/main/stocks/StocksPage.vue'
import TradesPage from '@/pages/main/trades/TradesPage.vue'

export const routes: RouteRecordRaw[] = [
  { path: '/login', component: LoginPage },
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'dashboard', component: DashboardPage, meta: { title: '대시보드' } },
      { path: 'stocks', name: 'stocks', component: StocksPage, meta: { title: '종목' } },
      { path: 'collection', name: 'collection', component: CollectionPage, meta: { title: '수집 종목 관리' } },
      { path: 'news', name: 'news', component: NewsPage, meta: { title: '뉴스' } },
      { path: 'portfolio', name: 'portfolio', component: PortfolioPage, meta: { title: '포트폴리오' } },
      { path: 'trades', name: 'trades', component: TradesPage, meta: { title: '거래 기록' } },
      { path: 'alerts', name: 'alerts', component: AlertsPage, meta: { title: '알림 관리' } },
      { path: 'charts', name: 'charts', component: ChartsPage, meta: { title: '차트' } },
      { path: 'memos', name: 'memos', component: MemosPage, meta: { title: '메모/태그' } },
      { path: 'settings', name: 'settings', component: SettingsPage, meta: { title: '설정' } },
    ],
  },
]
