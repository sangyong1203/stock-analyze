import { expect, test, type Locator, type Page } from '@playwright/test'

let browserErrors: string[]
let serverErrors: string[]

test.beforeEach(async ({ page }) => {
  browserErrors = []
  serverErrors = []
  page.on('console', (message) => {
    if (message.type() === 'error') browserErrors.push(message.text())
  })
  page.on('pageerror', (error) => browserErrors.push(error.message))
  page.on('response', (response) => {
    if (response.status() >= 500) serverErrors.push(`${response.status()} ${response.url()}`)
  })
})

test.afterEach(() => {
  expect(browserErrors, '예상하지 않은 브라우저 오류').toEqual([])
  expect(serverErrors, '예상하지 않은 서버 오류').toEqual([])
})

async function openCollection(page: Page) {
  const stocksPromise = page.waitForResponse(
    (response) => response.url().includes('/api/collection/stocks?') && response.request().method() === 'GET',
  )
  const summaryPromise = page.waitForResponse(
    (response) => response.url().endsWith('/api/collection/stocks/summary') && response.request().method() === 'GET',
  )
  await page.goto('/collection?auth=success')
  expect((await stocksPromise).ok()).toBeTruthy()
  expect((await summaryPromise).ok()).toBeTruthy()
  await expect(page.getByRole('heading', { name: '수집 종목 관리', level: 2 })).toBeVisible()
}

function collectionRows(page: Page) {
  return page.locator('.collection-table tbody tr')
}

function collectionRow(page: Page, name: string) {
  return collectionRows(page).filter({ hasText: name })
}

function kpi(page: Page, label: string) {
  return page.locator('.kpi-card').filter({ has: page.getByText(label, { exact: true }) }).locator('strong')
}

function ruleFormInput(dialog: Locator, label: string) {
  return dialog.getByText(label, { exact: true }).locator('..').locator('input').first()
}

test('수집 API가 실제 설정 요약과 필터 결과를 반환한다', async ({ request }) => {
  const summaryResponse = await request.get('http://127.0.0.1:8001/api/collection/stocks/summary')
  expect(await summaryResponse.json()).toEqual({
    total_candidate_count: 7,
    collect_enabled_count: 4,
    collect_news_count: 4,
    collect_alert_enabled_count: 1,
    manual_include_count: 1,
    manual_exclude_count: 1,
  })

  const highResponse = await request.get('http://127.0.0.1:8001/api/collection/stocks?priority=high&page=1&page_size=50')
  const highData = await highResponse.json()
  expect(highData.items.map((item: { stock_name: string }) => item.stock_name)).toEqual(['SK하이닉스', '현대차', '삼성전자'])

  const excludedResponse = await request.get('http://127.0.0.1:8001/api/collection/stocks?collect_enabled=false&page=1&page_size=50')
  const excludedData = await excludedResponse.json()
  expect(excludedData.items.map((item: { stock_name: string }) => item.stock_name)).toEqual(['NAVER', '셀트리온', '카카오게임즈'])

  const keywordResponse = await request.get('http://127.0.0.1:8001/api/collection/stocks?keyword=게임&page=1&page_size=50')
  expect((await keywordResponse.json()).items).toEqual([expect.objectContaining({ stock_name: '카카오게임즈', sector: '게임' })])
})

test('수집 종목 화면에 요약과 검색·수집 여부 필터가 반영된다', async ({ page }, testInfo) => {
  await openCollection(page)

  await expect(kpi(page, '전체 후보')).toHaveText('7')
  await expect(kpi(page, '수집 활성')).toHaveText('4')
  await expect(kpi(page, '뉴스 수집')).toHaveText('4')
  await expect(kpi(page, '알림 대상')).toHaveText('1')
  await expect(kpi(page, '수동 포함')).toHaveText('1')
  await expect(kpi(page, '수동 제외')).toHaveText('1')

  const keywordInput = page.getByPlaceholder('종목명, 종목코드, 섹터 검색')
  await keywordInput.fill('게임')
  await keywordInput.press('Enter')
  await expect(collectionRows(page)).toHaveCount(1)
  await expect(collectionRows(page).first()).toContainText('카카오게임즈')

  await keywordInput.fill('')
  await keywordInput.press('Enter')
  await page.locator('.collection-panel .toolbar .el-select').nth(1).click()
  await page.getByRole('option', { name: '제외', exact: true }).click()
  await expect(collectionRows(page)).toHaveCount(3)
  await expect(collectionRow(page, 'NAVER')).toBeVisible()
  await expect(collectionRow(page, '셀트리온')).toBeVisible()
  await expect(collectionRow(page, '카카오게임즈')).toBeVisible()

  const screenshotPath = testInfo.outputPath('collection-filters.png')
  await page.screenshot({ path: screenshotPath, fullPage: true })
  await testInfo.attach('collection-filters', { path: screenshotPath, contentType: 'image/png' })
})

test('수동 포함·제외와 재계산이 실제 수집 설정에 반영된다', async ({ page, request }) => {
  await openCollection(page)
  let row = collectionRow(page, '카카오게임즈')

  const includePromise = page.waitForResponse(
    (response) => /\/api\/collection\/stocks\/\d+\/include$/.test(response.url()) && response.request().method() === 'POST',
  )
  await row.getByRole('button', { name: '포함' }).click()
  const included = await (await includePromise).json()
  expect(included).toMatchObject({ stock_name: '카카오게임즈', collect_enabled: true, manual_include: true, manual_exclude: false })
  await expect(collectionRow(page, '카카오게임즈')).toContainText('수동 포함')

  row = collectionRow(page, '카카오게임즈')
  const excludePromise = page.waitForResponse(
    (response) => /\/api\/collection\/stocks\/\d+\/exclude$/.test(response.url()) && response.request().method() === 'POST',
  )
  await row.getByRole('button', { name: '제외' }).click()
  const excluded = await (await excludePromise).json()
  expect(excluded).toMatchObject({ stock_name: '카카오게임즈', collect_enabled: false, manual_include: false, manual_exclude: true })
  await expect(collectionRow(page, '카카오게임즈')).toContainText('수동 제외')

  const resetResponse = await request.patch(`http://127.0.0.1:8001/api/collection/stocks/${excluded.stock_id}`, {
    data: {
      collect_enabled: false,
      collect_news: false,
      collect_price_snapshot: false,
      collect_alert_enabled: false,
      priority: 'low',
      collect_reason: null,
      manual_override: false,
      manual_include: false,
      manual_exclude: false,
    },
  })
  expect(resetResponse.ok()).toBeTruthy()

  await page.reload()
  await expect(page.getByRole('heading', { name: '수집 종목 관리', level: 2 })).toBeVisible()
  const recalculatePromise = page.waitForResponse(
    (response) => response.url().endsWith('/api/collection/stocks/recalculate') && response.request().method() === 'POST',
  )
  await page.getByRole('button', { name: '재계산' }).click()
  const recalculated = await (await recalculatePromise).json()
  expect(recalculated).toEqual({ processed_count: 7, collect_enabled_count: 5, manual_exclude_count: 1 })
  await expect(kpi(page, '수집 활성')).toHaveText('5')
})

test('수집 규칙을 화면에서 등록·수정·비활성화·삭제한다', async ({ page }) => {
  await openCollection(page)
  await page.getByRole('button', { name: '수집 조건 규칙' }).click()
  const dialog = page.getByRole('dialog', { name: '수집 조건 규칙 설정' })
  await dialog.getByRole('button', { name: '새 규칙' }).click()

  await ruleFormInput(dialog, '규칙명').fill('E2E 게임 섹터 규칙')
  await dialog.getByText('유형', { exact: true }).locator('..').locator('.el-select').click()
  await page.getByRole('option', { name: 'sector', exact: true }).click()
  await ruleFormInput(dialog, '우선순위').fill('77')
  await dialog.getByPlaceholder('예: {"market_cap_min":1000000000000}').fill('{"sectors":["게임"]}')

  const createPromise = page.waitForResponse(
    (response) => response.url().endsWith('/api/collection/rules') && response.request().method() === 'POST',
  )
  await dialog.getByRole('button', { name: '저장' }).click()
  const created = await (await createPromise).json()
  expect(created).toMatchObject({ name: 'E2E 게임 섹터 규칙', rule_type: 'sector', priority: 77, enabled: true })
  await expect(dialog.locator('tbody tr').filter({ hasText: 'E2E 게임 섹터 규칙' })).toBeVisible()

  let ruleRow = dialog.locator('tbody tr').filter({ hasText: 'E2E 게임 섹터 규칙' })
  await ruleRow.getByRole('button', { name: '수정' }).click()
  await ruleFormInput(dialog, '규칙명').fill('E2E 게임 섹터 규칙 수정')
  await ruleFormInput(dialog, '우선순위').fill('78')
  const updatePromise = page.waitForResponse(
    (response) => response.url().endsWith(`/api/collection/rules/${created.id}`) && response.request().method() === 'PATCH',
  )
  await dialog.getByRole('button', { name: '저장' }).click()
  const updated = await (await updatePromise).json()
  expect(updated).toMatchObject({ name: 'E2E 게임 섹터 규칙 수정', priority: 78 })

  ruleRow = dialog.locator('tbody tr').filter({ hasText: 'E2E 게임 섹터 규칙 수정' })
  const togglePromise = page.waitForResponse(
    (response) => response.url().endsWith(`/api/collection/rules/${created.id}`) && response.request().method() === 'PATCH',
  )
  await ruleRow.locator('.el-switch').click()
  expect(await (await togglePromise).json()).toMatchObject({ enabled: false })

  const deletePromise = page.waitForResponse(
    (response) => response.url().endsWith(`/api/collection/rules/${created.id}`) && response.request().method() === 'DELETE',
  )
  await ruleRow.getByRole('button', { name: '삭제' }).click()
  await page.getByRole('dialog', { name: '규칙 삭제' }).getByRole('button', { name: '삭제' }).click()
  expect((await deletePromise).status()).toBe(204)
  await expect(dialog.locator('tbody tr').filter({ hasText: 'E2E 게임 섹터 규칙 수정' })).toHaveCount(0)
})
