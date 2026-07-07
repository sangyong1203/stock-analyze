<template>
  <div class="page-shell">
    <aside class="sidebar">
      <div class="brand">
        <span class="brand-mark">SA</span>
        <div>
          <strong>Stock Analyze</strong>
          <span>Private Workspace</span>
        </div>
      </div>

      <nav class="nav-list">
        <RouterLink v-for="item in menuItems" :key="item.path" :to="item.path" class="nav-item">
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>
    </aside>

    <main class="page-content">
      <header class="topbar">
        <div>
          <p class="eyebrow">Korean Equity Analysis</p>
          <h1>{{ currentTitle }}</h1>
        </div>
        <div class="topbar-actions">
          <div class="status-strip">
            <span>KRX 대기</span>
            <span>뉴스 수집 대기</span>
            <span>알림 ON</span>
          </div>
          <el-button plain @click="logout">로그아웃</el-button>
        </div>
      </header>

      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import {
  Bell,
  Collection,
  DataAnalysis,
  Document,
  EditPen,
  Histogram,
  Money,
  Operation,
  Setting,
  Tickets,
} from '@element-plus/icons-vue'
import { computed } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'

import { clearAuthenticated } from '@/shared/utils/auth'

const route = useRoute()
const router = useRouter()

const menuItems = [
  { path: '/dashboard', label: '대시보드', icon: DataAnalysis },
  { path: '/stocks', label: '종목', icon: Collection },
  { path: '/collection', label: '수집 종목 관리', icon: Operation },
  { path: '/news', label: '뉴스', icon: Document },
  { path: '/portfolio', label: '포트폴리오', icon: Money },
  { path: '/trades', label: '거래 기록', icon: Tickets },
  { path: '/alerts', label: '알림 관리', icon: Bell },
  { path: '/charts', label: '차트', icon: Histogram },
  { path: '/memos', label: '메모/태그', icon: EditPen },
  { path: '/settings', label: '설정', icon: Setting },
]

const currentTitle = computed(() => route.meta.title ?? '대시보드')

function logout() {
  clearAuthenticated()
  void router.replace('/login')
}
</script>

<style scoped>
.sidebar {
  width: 248px;
  min-height: 100vh;
  padding: 18px 14px;
  color: #eff6ef;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0)),
    var(--sidebar);
}

.brand {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 8px 8px 22px;
}

.brand-mark {
  display: grid;
  width: 38px;
  height: 38px;
  place-items: center;
  border: 1px solid rgba(255, 255, 255, 0.22);
  background: #254d38;
  font-weight: 800;
}

.brand strong,
.brand span {
  display: block;
}

.brand span {
  color: var(--sidebar-muted);
  font-size: 12px;
}

.nav-list {
  display: grid;
  gap: 4px;
}

.nav-item {
  display: flex;
  gap: 10px;
  align-items: center;
  min-height: 40px;
  padding: 0 10px;
  border-radius: 6px;
  color: #dfe9df;
  font-size: 14px;
}

.nav-item.router-link-active {
  background: #eef6e9;
  color: var(--accent-strong);
  font-weight: 700;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border);
}

.topbar-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.eyebrow {
  margin: 0 0 4px;
  color: var(--accent);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  font-size: 26px;
  letter-spacing: 0;
}

.status-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: flex-end;
}

.status-strip span {
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
  padding: 7px 10px;
  color: var(--text-muted);
  font-size: 12px;
}

@media (max-width: 900px) {
  .sidebar {
    width: 100%;
    min-height: auto;
  }

  .nav-list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .topbar {
    display: block;
  }

  .topbar-actions {
    display: block;
  }

  .status-strip {
    justify-content: flex-start;
    margin-top: 12px;
    margin-bottom: 12px;
  }
}
</style>
