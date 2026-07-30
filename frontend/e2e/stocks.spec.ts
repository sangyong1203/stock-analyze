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

async function openStocks(page: Page) {
  const responsePromise = page.waitForResponse(
    (response) => response.url().includes('/api/stocks?') && response.request().method() === 'GET',
  )
  await page.goto('/stocks?auth=success')
  expect((await responsePromise).ok()).toBeTruthy()
  await expect(page.getByRole('heading', { name: '종목 기본정보' })).toBeVisible()
}

function stockRows(page: Page) {
  return page.locator('.stocks-panel tbody tr')
}

function stockRow(page: Page, name: string) {
  return stockRows(page).filter({ hasText: name })
}

function formInput(dialog: Locator, label: string) {
  return dialog.getByText(label, { exact: true }).locator('..').locator('input').first()
}

test('종목 API가 검색·시장·관심·보유 필터를 실제 DB에 적용한다', async ({ request }) => {
  const allResponse = await request.get('http://127.0.0.1:8001/api/stocks?is_active=true')
  expect(allResponse.ok()).toBeTruthy()
  const allStocks = await allResponse.json()
  expect(allStocks).toHaveLength(7)

  const searchResponse = await request.get('http://127.0.0.1:8001/api/stocks?search=005930&is_active=true')
  expect(await searchResponse.json()).toEqual([expect.objectContaining({ code: '005930', name: '삼성전자', is_holding: true })])

  const kosdaqResponse = await request.get('http://127.0.0.1:8001/api/stocks?market=KOSDAQ&is_active=true')
  expect(await kosdaqResponse.json()).toEqual([expect.objectContaining({ code: '293490', name: '카카오게임즈', is_holding: false })])

  const favoriteResponse = await request.get('http://127.0.0.1:8001/api/stocks?is_favorite=true&is_active=true')
  expect((await favoriteResponse.json()).map((item: { name: string }) => item.name)).toEqual(['SK하이닉스', '삼성전자'])

  const holdingResponse = await request.get('http://127.0.0.1:8001/api/stocks?is_holding=true&is_active=true')
  expect(await holdingResponse.json()).toHaveLength(6)
})

test('종목 화면에서 검색·시장·관심 필터와 KPI를 확인한다', async ({ page }, testInfo) => {
  await openStocks(page)

  await expect(page.locator('.kpi-card').filter({ has: page.getByText('표시 종목', { exact: true }) }).locator('strong')).toHaveText('7')
  await expect(page.locator('.kpi-card').filter({ has: page.getByText('관심 종목', { exact: true }) }).locator('strong')).toHaveText('2')
  await expect(page.locator('.kpi-card').filter({ has: page.getByText('보유 종목', { exact: true }) }).locator('strong')).toHaveText('6')

  const searchInput = page.getByPlaceholder('종목명 또는 코드 검색')
  await searchInput.fill('삼성전자')
  await searchInput.press('Enter')
  await expect(stockRows(page)).toHaveCount(1)
  await expect(stockRows(page).first()).toContainText('005930')

  await searchInput.fill('')
  await searchInput.press('Enter')
  await page.locator('.stocks-panel .toolbar .el-select').click()
  await page.getByRole('option', { name: 'KOSDAQ', exact: true }).click()
  await expect(stockRows(page)).toHaveCount(1)
  await expect(stockRows(page).first()).toContainText('카카오게임즈')

  await openStocks(page)
  await page.getByText('관심종목만', { exact: true }).click()
  await expect(stockRows(page)).toHaveCount(2)
  await expect(stockRow(page, '삼성전자')).toBeVisible()
  await expect(stockRow(page, 'SK하이닉스')).toBeVisible()

  const screenshotPath = testInfo.outputPath('stocks-filters.png')
  await page.screenshot({ path: screenshotPath, fullPage: true })
  await testInfo.attach('stocks-filters', { path: screenshotPath, contentType: 'image/png' })
})

test('종목 화면에서 등록·수정·관심 설정·비활성화를 실제 DB에 반영한다', async ({ page, request }) => {
  await openStocks(page)
  await page.getByRole('button', { name: '종목 추가' }).click()

  let dialog = page.getByRole('dialog', { name: '종목 추가' })
  await formInput(dialog, '종목 코드').fill('1234')
  await formInput(dialog, '종목명').fill('E2E테스트종목')
  await dialog.getByText('시장', { exact: true }).locator('..').locator('.el-select').click()
  await page.getByRole('option', { name: 'KOSDAQ', exact: true }).click()
  await formInput(dialog, '섹터').fill('테스트섹터')
  await formInput(dialog, '업종').fill('테스트업종')
  await formInput(dialog, '현재가').fill('12345')
  await formInput(dialog, '시가총액').fill('987654321')
  await formInput(dialog, '뉴스 매칭 별칭').fill('E2E별칭, 테스트별칭')
  await dialog.getByText('관심종목', { exact: true }).click()

  const createResponsePromise = page.waitForResponse(
    (response) => response.url().endsWith('/api/stocks') && response.request().method() === 'POST',
  )
  await dialog.getByRole('button', { name: '저장' }).click()
  expect((await createResponsePromise).status()).toBe(201)
  await expect(stockRow(page, 'E2E테스트종목')).toContainText('001234')

  let row = stockRow(page, 'E2E테스트종목')
  await row.getByRole('button', { name: '수정' }).click()
  dialog = page.getByRole('dialog', { name: '종목 수정' })
  await formInput(dialog, '종목명').fill('E2E수정종목')
  await formInput(dialog, '뉴스 매칭 별칭').fill('수정별칭, 두번째별칭')
  const updateResponsePromise = page.waitForResponse(
    (response) => /\/api\/stocks\/\d+$/.test(response.url()) && response.request().method() === 'PUT',
  )
  await dialog.getByRole('button', { name: '저장' }).click()
  const updateResponse = await updateResponsePromise
  expect(updateResponse.ok()).toBeTruthy()
  const updated = await updateResponse.json()
  expect(updated).toMatchObject({ name: 'E2E수정종목', aliases_json: ['수정별칭', '두번째별칭'], is_favorite: true })

  row = stockRow(page, 'E2E수정종목')
  const favoriteOffPromise = page.waitForResponse(
    (response) => response.url().endsWith(`/api/stocks/${updated.id}/favorite`) && response.request().method() === 'PATCH',
  )
  await row.getByRole('button', { name: '해제' }).click()
  expect((await favoriteOffPromise).ok()).toBeTruthy()
  await expect(stockRow(page, 'E2E수정종목').getByRole('button', { name: '설정' })).toBeVisible()

  const deactivatePromise = page.waitForResponse(
    (response) => response.url().endsWith(`/api/stocks/${updated.id}`) && response.request().method() === 'DELETE',
  )
  await stockRow(page, 'E2E수정종목').getByRole('button', { name: '비활성화' }).click()
  expect((await deactivatePromise).ok()).toBeTruthy()
  await expect(stockRow(page, 'E2E수정종목')).toHaveCount(0)

  const detailResponse = await request.get(`http://127.0.0.1:8001/api/stocks/${updated.id}`)
  expect(await detailResponse.json()).toMatchObject({ code: '001234', name: 'E2E수정종목', is_active: false, is_favorite: false })
})
