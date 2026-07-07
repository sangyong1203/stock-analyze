import { createRouter, createWebHistory } from 'vue-router'

import { isAuthenticated, setAuthenticated } from '@/shared/utils/auth'

import { routes } from './routes'

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  if (to.query.auth === 'success') {
    setAuthenticated(true)

    const nextQuery = { ...to.query }
    delete nextQuery.auth

    return {
      path: to.path,
      hash: to.hash,
      query: nextQuery,
      replace: true,
    }
  }

  if (to.name === 'login' && isAuthenticated()) {
    const redirectTarget = typeof to.query.redirect === 'string' ? to.query.redirect : '/dashboard'
    return redirectTarget
  }

  if (to.matched.some((record) => record.meta.requiresAuth) && !isAuthenticated()) {
    return {
      path: '/login',
      query: { redirect: to.fullPath },
    }
  }

  return true
})

export default router
