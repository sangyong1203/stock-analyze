<template>
  <section class="login-page">
    <div class="login-panel">
      <p class="muted">Private Workspace</p>
      <h1>Stock Analyze</h1>
      <el-button type="primary">Google 로그인</el-button>
    </div>
  </section>
</template>

<style scoped>
.login-page {
  display: grid;
  min-height: 100vh;
  place-items: center;
  background: var(--app-bg);
}

.login-panel {
  width: min(420px, calc(100vw - 32px));
  border: 1px solid var(--border);
  background: var(--surface);
  padding: 28px;
  box-shadow: var(--shadow);
}
</style>
