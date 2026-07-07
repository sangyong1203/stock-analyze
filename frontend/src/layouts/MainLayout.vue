<template>
  <div class="page-shell">
    <aside class="sidebar" :class="{ 'is-collapsed': isMenuCollapsed }">
      <div class="brand">
        <div class="brand-copy" :class="{ 'is-collapsed': isMenuCollapsed }">
          <div v-show="!isMenuCollapsed" class="brand-text">
            <span class="brand-mark">SA</span>
            <strong>Stock Analyze</strong>
            <span>Private Workspace</span>
          </div>
        </div>
        <el-button
          class="collapse-button"
          circle
          plain
          :icon="isMenuCollapsed ? Expand : Fold"
          @click="toggleMenu"
        />
      </div>

      <el-menu
        class="sidebar-menu"
        :default-active="activeMenu"
        :collapse="isMenuCollapsed"
        :collapse-transition="false"
        router
      >
        <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path">
          <el-icon><component :is="item.icon" /></el-icon>
          <template #title>{{ item.label }}</template>
        </el-menu-item>
      </el-menu>
    </aside>

    <main class="page-content">
      <header class="topbar">
        <div>
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

      <section class="content-scroll">
        <RouterView />
      </section>
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
  Expand,
  Fold,
  Histogram,
  Money,
  Operation,
  Setting,
  Tickets,
} from '@element-plus/icons-vue'
import { computed, ref } from 'vue'
import { RouterView, useRoute, useRouter } from 'vue-router'

import { clearAuthenticated } from '@/shared/utils/auth'

const route = useRoute()
const router = useRouter()
const isMenuCollapsed = ref(false)

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
const activeMenu = computed(() => route.path)

function toggleMenu() {
  isMenuCollapsed.value = !isMenuCollapsed.value
}

function logout() {
  clearAuthenticated()
  void router.replace('/login')
}
</script>

<style scoped>
.sidebar {
  width: 272px;
  height: 100vh;
  padding: 18px 14px;
  overflow-y: auto;
  color: #eff6ef;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0)),
    var(--sidebar);
  transition: width 0.24s ease;
  scrollbar-color: rgba(238, 246, 233, 0.34) transparent;
  scrollbar-width: thin;
}

.sidebar.is-collapsed {
  width: 94px;
}

.sidebar.is-collapsed .brand {
  flex-direction: column;
  justify-content: flex-start;
  gap: 10px;
}

.brand {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  padding: 8px 8px 18px;
}

.brand-copy {
  display: flex;
  gap: 12px;
  align-items: center;
  flex: 1;
  min-width: 0;
}

.brand-copy.is-collapsed {
  justify-content: center;
  flex: 0 0 38px;
}

.brand-mark {
  display: grid;
  width: 38px;
  height: 38px;
  flex: 0 0 38px;
  place-items: center;
  border: 1px solid rgba(255, 255, 255, 0.22);
  background: #254d38;
  font-weight: 800;
}

.brand-text {
  min-width: 0;
  white-space: nowrap;
}

.brand strong,
.brand span {
  display: block;
}

.brand span {
  color: var(--sidebar-muted);
  font-size: 12px;
}

.collapse-button {
  align-self: flex-end;
  flex: 0 0 auto;
  border-color: rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.04);
  color: #eff6ef;
}

.sidebar.is-collapsed .collapse-button {
  align-self: center;
}

.sidebar-menu {
  border-right: 0;
  background: transparent;
}

.sidebar-menu :deep(.el-menu) {
  border-right: 0;
}

.sidebar-menu :deep(.el-menu-item) {
  margin-bottom: 4px;
  border-radius: 10px;
  color: #dfe9df;
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: #eef6e9;
  color: var(--accent-strong);
  font-weight: 700;
}

.sidebar-menu :deep(.el-menu-item .el-icon) {
  font-size: 18px;
}

.topbar {
  flex: 0 0 auto;
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

.content-scroll {
  min-height: 0;
  flex: 1;
  overflow: auto;
  padding-right: 4px;
  margin-right: -14px;
  margin-top: 16px;
}

@media (max-width: 900px) {
  .sidebar,
  .sidebar.is-collapsed {
    width: 100%;
    height: auto;
    min-height: auto;
    overflow: visible;
  }

  .brand {
    align-items: center;
  }

  .brand-copy.is-collapsed {
    justify-content: flex-start;
  }

  .brand-text {
    display: block !important;
  }

  .sidebar-menu :deep(.el-menu) {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
  }

  .sidebar-menu :deep(.el-menu-item) {
    margin-bottom: 0;
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

  .content-scroll {
    overflow: visible;
    padding-top: 14px;
    padding-right: 0;
  }
}
</style>
