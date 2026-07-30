import { expect, test, type Page } from '@playwright/test'

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

async function openDashboard(page: Page) {
  const responsePromise = page.waitForResponse(
    (response) => response.url().endsWith('/api/dashboard/summary') && response.request().method() === 'GET',
  )
  await page.goto('/dashboard?auth=success')
  const response = await responsePromise
  expect(response.ok()).toBeTruthy()
  await expect(page).toHaveURL('http://127.0.0.1:5174/dashboard')
  await expect(page.getByRole('heading', { name: '투자 현황 요약' })).toBeVisible()
  return response
}

function panel(page: Page, heading: string) {
  return page.locator('section.panel').filter({ has: page.getByRole('heading', { name: heading, exact: true }) })
}

function kpi(page: Page, label: string) {
  return page.locator('.kpi-card').filter({ has: page.getByText(label, { exact: true }) })
}

test('대시보드 API가 테스트 DB의 실제 집계와 TOP 5 정렬을 반환한다', async ({ request }) => {
  const response = await request.get('http://127.0.0.1:8001/api/dashboard/summary')
  expect(response.ok()).toBeTruthy()
  const summary = await response.json()

  expect(summary.portfolio_summary).toMatchObject({
    total_cash: '5000000.00',
    total_invested_amount: '3980000.00',
    total_market_value: '4000000.00',
    total_unrealized_profit_loss: '20000.00',
    realized_profit_loss: '25000.00',
    total_asset_value: '9000000.00',
    holding_count: 6,
  })
  expect(summary.top_holdings.map((item: { stock_name: string }) => item.stock_name)).toEqual([
    'SK하이닉스',
    'LG화학',
    '현대차',
    '삼성전자',
    'NAVER',
  ])
  expect(summary.top_gainers.map((item: { stock_name: string }) => item.stock_name)).toEqual([
    '삼성전자',
    'NAVER',
    '현대차',
    'LG화학',
    '셀트리온',
  ])
  expect(summary.top_losers.map((item: { stock_name: string }) => item.stock_name)).toEqual([
    'SK하이닉스',
    '셀트리온',
    'LG화학',
    'NAVER',
    '현대차',
  ])
  expect(summary.recent_trades).toHaveLength(5)
  expect(summary.recent_trades[0].stock_name).toBe('셀트리온')
  expect(summary.recent_trades.map((item: { stock_name: string }) => item.stock_name)).not.toContain('삼성전자')
  expect(summary.recent_news).toHaveLength(5)
  expect(summary.recent_news[0].title).toContain('셀트리온 E2E 주요 뉴스')
  expect(summary.recent_news.map((item: { title: string }) => item.title).join(' ')).not.toContain('삼성전자 E2E 주요 뉴스')
  expect(summary.recent_alert_histories[0]).toMatchObject({
    title: '삼성전자 목표가 접근',
    status: 'sent',
  })
  expect(summary.price_alert_summary).toMatchObject({
    total_count: 1,
    enabled_count: 1,
    triggered_count: 1,
    sent_count: 1,
  })
  expect(summary.news_alert_summary).toMatchObject({
    alert_target_count: 1,
    high_importance_count: 1,
  })
  expect(summary.memo_summary.recent_memos).toHaveLength(5)
  expect(summary.memo_summary.top_tags).toEqual(
    expect.arrayContaining([
      expect.objectContaining({ name: '장기투자', usage_count: 3 }),
      expect.objectContaining({ name: '실적검토', usage_count: 1 }),
    ]),
  )
})

test('대시보드 화면에 실제 포트폴리오 KPI와 요약 집계가 표시된다', async ({ page }, testInfo) => {
  await openDashboard(page)

  await expect(kpi(page, '총 자산').locator('strong')).toHaveText('9,000,000원')
  await expect(kpi(page, '현금 잔고').locator('strong')).toHaveText('5,000,000원')
  await expect(kpi(page, '평가 손익').locator('strong')).toHaveText('+20,000원')
  await expect(kpi(page, '평가 손익률').locator('strong')).toHaveText('+0.50%')
  await expect(kpi(page, '보유 종목').locator('strong')).toHaveText('6')

  const portfolioPanel = panel(page, '포트폴리오 요약')
  await expect(portfolioPanel).toContainText('총 매수금액')
  await expect(portfolioPanel).toContainText('3,980,000원')
  await expect(portfolioPanel).toContainText('총 평가금액')
  await expect(portfolioPanel).toContainText('4,000,000원')
  await expect(portfolioPanel).toContainText('실현 손익')
  await expect(portfolioPanel).toContainText('+25,000원')

  const jobPanel = panel(page, '작업 상태')
  await expect(jobPanel.getByText('활성 작업', { exact: true }).locator('..').locator('strong')).toHaveText('8')
  await expect(jobPanel.getByText('성공', { exact: true }).locator('..').locator('strong')).toHaveText('1')
  await expect(jobPanel.getByText('실패', { exact: true }).locator('..').locator('strong')).toHaveText('0')
  await expect(jobPanel.getByText('미실행', { exact: true }).locator('..').locator('strong')).toHaveText('7')

  const alertPanel = panel(page, '알림 요약')
  await expect(alertPanel).toContainText('가격 알림 활성1')
  await expect(alertPanel).toContainText('가격 알림 발송1')
  await expect(alertPanel).toContainText('뉴스 알림 후보1')

  const screenshotPath = testInfo.outputPath('dashboard-summary.png')
  await page.screenshot({ path: screenshotPath, fullPage: true })
  await testInfo.attach('dashboard-summary', { path: screenshotPath, contentType: 'image/png' })
})

test('대시보드 목록이 최근 데이터와 TOP 5 제한을 화면에 반영한다', async ({ page }) => {
  await openDashboard(page)

  const holdingsPanel = panel(page, '보유 종목 TOP 5')
  await expect(holdingsPanel.locator('tbody tr')).toHaveCount(5)
  await expect(holdingsPanel.locator('tbody tr').first()).toContainText('SK하이닉스')
  await expect(holdingsPanel).not.toContainText('셀트리온')

  const tradesPanel = panel(page, '최근 거래')
  await expect(tradesPanel.locator('tbody tr')).toHaveCount(5)
  await expect(tradesPanel.locator('tbody tr').first()).toContainText('셀트리온')
  await expect(tradesPanel).not.toContainText('삼성전자')

  const newsPanel = panel(page, '최근 뉴스')
  await expect(newsPanel.locator('tbody tr')).toHaveCount(5)
  await expect(newsPanel.locator('tbody tr').first()).toContainText('셀트리온 E2E 주요 뉴스 6')
  await expect(newsPanel).not.toContainText('삼성전자 E2E 주요 뉴스 1')

  const alertHistoryPanel = panel(page, '최근 알림 이력')
  await expect(alertHistoryPanel).toContainText('삼성전자 목표가 접근')
  await expect(alertHistoryPanel).toContainText('price · sent')

  const memoPanel = panel(page, '최근 메모')
  await expect(memoPanel.locator('li')).toHaveCount(5)
  await expect(memoPanel).toContainText('셀트리온 E2E 메모')
  await expect(memoPanel).not.toContainText('삼성전자 E2E 메모')

  const tagPanel = panel(page, '메모 / 태그')
  await expect(tagPanel).toContainText('장기투자 · 3')
  await expect(tagPanel).toContainText('실적검토 · 1')
})

test('대시보드 빠른 이동 버튼이 대상 화면으로 이동한다', async ({ page }) => {
  await openDashboard(page)

  const quickActions = [
    { name: '거래 기록', path: '/trades' },
    { name: '포트폴리오', path: '/portfolio' },
    { name: '뉴스', path: '/news' },
    { name: '알림', path: '/alerts' },
    { name: '차트', path: '/charts' },
  ]

  for (const action of quickActions) {
    await page.locator('.quick-actions').getByRole('button', { name: action.name, exact: true }).click()
    await expect(page).toHaveURL(`http://127.0.0.1:5174${action.path}`)
    await page.goto('/dashboard')
    await expect(page.getByRole('heading', { name: '투자 현황 요약' })).toBeVisible()
  }
})
