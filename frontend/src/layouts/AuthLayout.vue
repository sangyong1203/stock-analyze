<template>
  <main class="auth-layout">
    <slot />
  </main>
</template>

<style scoped>
.auth-layout {
  display: grid;
  min-height: 100vh;
  place-items: center;
  background: var(--app-bg);
}
</style>
