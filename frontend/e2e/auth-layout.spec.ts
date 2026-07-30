import { expect, test, type Page } from '@playwright/test'

const AUTH_STORAGE_KEY = 'stock-analyze-authenticated'

let browserErrors: string[]
let serverErrors: string[]

test.beforeEach(async ({ page }) => {
  browserErrors = []
  serverErrors = []

  page.on('console', (message) => {
    if (message.type() === 'error') {
      browserErrors.push(message.text())
    }
  })
  page.on('pageerror', (error) => browserErrors.push(error.message))
  page.on('response', (response) => {
    if (response.status() >= 500) {
      serverErrors.push(`${response.status()} ${response.url()}`)
    }
  })
})

test.afterEach(() => {
  expect(browserErrors, '예상하지 않은 브라우저 오류').toEqual([])
  expect(serverErrors, '예상하지 않은 서버 오류').toEqual([])
})

async function authenticate(page: Page) {
  await page.goto('/dashboard?auth=success')
  await expect(page).toHaveURL('http://127.0.0.1:5174/dashboard')
  await expect(page.locator('.topbar').getByRole('heading', { name: '대시보드' })).toBeVisible()
}

test('전용 백엔드와 마이그레이션된 테스트 DB가 연결된다', async ({ request }) => {
  const healthResponse = await request.get('http://127.0.0.1:8001/health')
  expect(healthResponse.ok()).toBeTruthy()
  await expect(healthResponse.json()).resolves.toEqual({ status: 'ok' })

  const authResponse = await request.get('http://127.0.0.1:8001/api/auth/status')
  expect(authResponse.ok()).toBeTruthy()
  await expect(authResponse.json()).resolves.toMatchObject({
    success: true,
    data: {
      oauth_configured: false,
      allowed_email_configured: false,
    },
  })

  const dashboardResponse = await request.get('http://127.0.0.1:8001/api/dashboard/summary')
  expect(dashboardResponse.ok()).toBeTruthy()
})

test('보호 화면은 로그인 화면으로 이동하고 원래 경로를 보존한다', async ({ page }) => {
  await page.goto('/dashboard')

  await expect(page).toHaveURL('http://127.0.0.1:5174/login?redirect=/dashboard')
  await expect(page.getByRole('heading', { name: 'Stock Analyze' })).toBeVisible()
  await expect(page.getByText('로그인 후 요청한 화면으로 이동합니다.')).toBeVisible()
  await expect(page.getByRole('button', { name: 'Google 로그인' })).toBeVisible()
})

test('로그인 성공 콜백을 처리하고 인증 상태를 저장한다', async ({ page }, testInfo) => {
  await authenticate(page)

  const authenticated = await page.evaluate((key) => localStorage.getItem(key), AUTH_STORAGE_KEY)
  expect(authenticated).toBe('true')
  await expect(page.getByRole('heading', { name: '투자 현황 요약' })).toBeVisible()

  const screenshotPath = testInfo.outputPath('authenticated-dashboard.png')
  await page.screenshot({ path: screenshotPath, fullPage: true })
  await testInfo.attach('authenticated-dashboard', { path: screenshotPath, contentType: 'image/png' })
})

test('공통 메뉴로 10개 MVP 화면을 이동할 수 있다', async ({ page }) => {
  await authenticate(page)

  const menuCases = [
    { name: '대시보드', path: '/dashboard' },
    { name: '종목', path: '/stocks' },
    { name: '수집 종목 관리', path: '/collection' },
    { name: '뉴스', path: '/news' },
    { name: '포트폴리오', path: '/portfolio' },
    { name: '거래 기록', path: '/trades' },
    { name: '알림 관리', path: '/alerts' },
    { name: '차트', path: '/charts' },
    { name: '메모/태그', path: '/memos' },
    { name: '설정', path: '/settings' },
  ]

  for (const menuCase of menuCases) {
    await page.getByRole('menuitem', { name: menuCase.name, exact: true }).click()
    await expect(page).toHaveURL(`http://127.0.0.1:5174${menuCase.path}`)
    await expect(page.locator('.topbar').getByRole('heading', { name: menuCase.name, exact: true })).toBeVisible()
  }
})

test('사이드 메뉴를 접고 다시 펼칠 수 있다', async ({ page }) => {
  await authenticate(page)

  const sidebar = page.locator('.sidebar')
  await page.getByRole('button', { name: '메뉴 접기' }).click()
  await expect(sidebar).toHaveClass(/is-collapsed/)
  await expect(page.getByRole('button', { name: '메뉴 펼치기' })).toBeVisible()

  await page.getByRole('button', { name: '메뉴 펼치기' }).click()
  await expect(sidebar).not.toHaveClass(/is-collapsed/)
})

test('로그아웃하면 인증 상태가 삭제되고 로그인 화면으로 이동한다', async ({ page }) => {
  await authenticate(page)

  await page.getByRole('button', { name: '로그아웃' }).click()
  await expect(page).toHaveURL('http://127.0.0.1:5174/login')
  await expect(page.getByRole('heading', { name: 'Stock Analyze' })).toBeVisible()

  const authenticated = await page.evaluate((key) => localStorage.getItem(key), AUTH_STORAGE_KEY)
  expect(authenticated).toBeNull()
})
