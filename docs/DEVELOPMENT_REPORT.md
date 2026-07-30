# DEVELOPMENT REPORT

## Latest task — Playwright Stage 3

### Work overview

- Completed Stage 3 stocks / collection-target integration tests using the actual Vue frontend, FastAPI backend, and isolated SQLite database.
- No API mocks were used.
- Live KRX collection was not executed.
- GPT functionality was not used.

### Reference documents

- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

### Completed work

- Stock search and filter API/UI verification
- Stock create, update, favorite, and deactivate flow
- Collection summary and filter verification
- Manual include/exclude and recalculation flow
- Collection rule create, update, disable, and delete flow
- Full Stage 1-3 regression execution
- Real backend defect fix discovered by Playwright

### Generated files

- `frontend/e2e/stocks.spec.ts`
- `frontend/e2e/collection.spec.ts`
- `docs/PLAYWRIGHT_STAGE_3_REPORT.md`

### Modified files

- `backend/tests/e2e/seed_dashboard.py`
- `backend/app/domains/collection/repository.py`
- `backend/app/domains/collection/service.py`
- `docs/CODEX_TODO.md`
- `docs/CODEX_PROGRESS.md`
- `docs/DEVELOPMENT_REPORT.md`

### Backend implementation result

- Fixed manual include/exclude response failure.
- Added a direct collection-stock detail query instead of incorrectly iterating the paginated list return tuple.
- Stock and collection APIs passed against the actual E2E DB.

### Frontend implementation result

- No production screen change was required for Stage 3.
- Stock and collection screen interactions passed with actual API responses.

### DB implementation result

- Production DB and schema were unchanged.
- E2E seed now includes seven active stocks and six explicit collection settings.
- CRUD test data is deactivated, deleted, or reset during each scenario where appropriate.

### Execution method

```text
cd frontend
npm run test:e2e
npm run build
```

### Test result

- Stage 3 tests: `7 passed`
- Stage 1-2 regression: `10 passed`
- Total Playwright result: `17 passed (28.6s)`
- Frontend build: passed
- Python compile check: passed

### Incomplete items

- Stages 4 through 8 have not started.
- GPT features remain outside the requested test scope.
- Live KRX price collection is not part of deterministic screen integration testing.

### Confirmation-needed items

- None for Stage 3.

### Next step suggestions

- After user approval, proceed only with Stage 4 news integration tests while excluding GPT functionality.

### Final completion statement

- Playwright test-DB integration Stage 3 is complete.
- Waiting for user approval before Stage 4.

## Latest task — Playwright Stage 2

### Work overview

- Completed Stage 2 dashboard integration tests using the actual Vue frontend, FastAPI backend, and isolated SQLite test database.
- No API mocks were used.
- GPT execution and GPT result assertions were excluded.
- Production DB was not used or modified.

### Reference documents

- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

### Completed work

- Dashboard-specific deterministic E2E seed
- Real dashboard aggregate API verification
- KPI and summary panel verification
- TOP 5 ordering and limit verification
- Recent trades, news, alert, memo, and tag verification
- Dashboard quick-action navigation verification
- Full-page dashboard screenshot attachment
- Stage 1 regression execution

### Generated files

- `backend/tests/e2e/seed_dashboard.py`
- `frontend/e2e/dashboard.spec.ts`
- `docs/PLAYWRIGHT_STAGE_2_REPORT.md`

### Modified files

- `frontend/e2e/global-setup.ts`
- `docs/CODEX_TODO.md`
- `docs/CODEX_PROGRESS.md`
- `docs/DEVELOPMENT_REPORT.md`

### Backend implementation result

- No production backend code change.
- Existing dashboard, job-summary, portfolio, holdings, news, alerts, memos, and tags aggregation paths were exercised through the real API.

### Frontend implementation result

- No production dashboard code change was required.
- Dashboard KPI, panels, tables, lists, and quick-action buttons passed against actual API data.

### DB implementation result

- Added E2E-only deterministic seed data.
- Six holdings verify aggregate totals and TOP 5 boundaries.
- Production DB and schema were unchanged.

### Execution method

```text
cd frontend
npm run test:e2e
npm run build
```

### Test result

- Dashboard tests: `4 passed`
- Stage 1 regression: `6 passed`
- Total Playwright result: `10 passed (18.0s)`
- Frontend build: passed
- HTML report: `frontend/playwright-report/index.html`
- Dashboard screenshot: attached to the successful test result

### Incomplete items

- Stages 3 through 8 have not started.
- GPT features remain outside the requested test scope.

### Confirmation-needed items

- None for Stage 2.

### Next step suggestions

- After user approval, proceed only with Stage 3 stocks / collection integration tests.

### Final completion statement

- Playwright test-DB integration Stage 2 is complete.
- Waiting for user approval before Stage 3.

## Latest task — Playwright Stage 1

### Work overview

- Implemented Playwright integration testing with an isolated SQLite test database.
- Completed only Stage 1: authentication and shared layout.
- No API mocks were used.
- GPT execution and real Gmail sending were excluded.

### Reference documents

- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

### Completed work

- Playwright Test and Chromium setup
- Automatic E2E DB reset, migration, and seed
- Actual FastAPI/Vue server orchestration
- Six authentication/shared-layout integration tests
- HTML report and authenticated dashboard screenshot
- Shared sidebar collapse button accessibility label

### Generated files

- `frontend/playwright.config.ts`
- `frontend/e2e/global-setup.ts`
- `frontend/e2e/auth-layout.spec.ts`
- `docs/PLAYWRIGHT_STAGE_1_REPORT.md`

### Modified files

- `.gitignore`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/src/layouts/MainLayout.vue`
- `docs/CODEX_TODO.md`
- `docs/CODEX_PROGRESS.md`
- `docs/DEVELOPMENT_REPORT.md`

### Backend implementation result

- No production backend code change.
- Test execution starts the actual FastAPI application on port `8001`.
- `/health`, `/api/auth/status`, and `/api/dashboard/summary` passed against the test DB.

### Frontend implementation result

- Playwright integration configuration added.
- Sidebar collapse button now exposes `메뉴 접기` / `메뉴 펼치기` accessible names.
- Production frontend build passed.

### DB implementation result

- Production DB was not used or modified.
- `backend/stock_analyze_e2e.db` is recreated for every Playwright run.
- 27 MVP tables and Alembic version `20260624_0002` were verified.

### Execution method

```text
cd frontend
npm run test:e2e
npm run build
```

### Test result

- Playwright: `6 passed`
- Frontend build: passed
- HTML report: `frontend/playwright-report/index.html`
- Screenshot: authenticated dashboard attached to the successful test result

### Incomplete items

- Stages 2 through 8 have not started.
- Actual Google account approval was not automated.

### Confirmation-needed items

- Actual Google OAuth approval should remain a manual check unless a separate test-account policy is confirmed.

### Next step suggestions

- After user approval, proceed only with Stage 2 dashboard integration tests.

### Final completion statement

- Playwright test-DB integration Stage 1 is complete.
- Waiting for user approval before Stage 2.

## Work overview

- Latest completed scope: `docs/CODEX_TASK_2.23.md`
- Scope handled in this task: pre-operation price/news refresh and alert/GPT readiness verification
- Constraint kept:
  - no new feature
  - no new table
  - no new migration
  - no real Gmail sending

## Reference documents

- `docs/CODEX_TASK_2.23.md`
- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

## Completed work

- Ran KRX daily price collection for live DB and updated latest price data to `2025-07-07`
- Rechecked holdings, portfolio, and dashboard consistency after price refresh
- Ran market news collection and confirmed latest news data was inserted into live DB
- Rechecked GPT summary/filter target status and execution readiness
- Ran GPT summary processing for 5 targets
- Confirmed GPT filter execution currently fails due OpenAI API quota
- Ran price alert dry-run and news alert dry-run only
- Updated task report documents for the latest pre-operation verification result

## Generated files

- `docs/CODEX_TASK_2.23_REPORT.md`

## Modified files

- `docs/CODEX_PROGRESS.md`
- `docs/DEVELOPMENT_REPORT.md`

## Backend implementation result

- No backend code change
- Existing APIs used for live verification:
  - `/health`
  - `/api/prices/collect/krx/daily`
  - `/api/prices/summary`
  - `/api/holdings/summary`
  - `/api/portfolio/summary`
  - `/api/dashboard/summary`
  - `/api/news/collect/market`
  - `/api/news/summary`
  - `/api/news/gpt/targets`
  - `/api/news/gpt/status`
  - `/api/news/gpt/summary/run`
  - `/api/news/gpt/filter/run`
  - `/api/price-alerts/evaluate/dry-run`
  - `/api/news/alerts/send/dry-run`

## Frontend implementation result

- No frontend code change

## DB implementation result

- No schema change
- No new table
- No migration
- Live DB current state:
  - `stock_prices`: `357946`
  - `latest_price_date`: `2025-07-07`
  - `news`: `51`
  - `latest_news_published_at`: `2026-07-07 14:22:00`

## Execution method

Main verification:

```text
Run KRX daily price collect on live DB
Recheck prices/holdings/portfolio/dashboard summaries
Run market news collect
Check news/GPT status APIs
Run GPT summary/filter execution readiness check
Run price alert and news alert dry-run only
Update report documents
```

## Test result

- Backend health: passed
- KRX daily dry-run check: passed
  - `20250707` fetched `2761`
  - `20250704` fetched `2760`
- KRX daily live collect: passed
  - bas_date = `20250707`
  - fetched_count = `2761`
  - inserted_count = `2761`
  - updated_count = `0`
  - stock_created_count = `3`
  - error_count = `0`
- Price summary after refresh: checked
  - total_price_rows = `357946`
  - latest_price_date = `2025-07-07`
  - latest_updated_stocks_count = `2761`
- Holdings summary after refresh: checked
  - holding_count = `4`
  - total_market_value = `2263500.00`
  - total_unrealized_profit_loss = `-2844590.00`
- Portfolio summary after refresh: checked
  - total_cash = `0`
  - total_asset_value = `2263500.00`
  - holding_count = `4`
- Dashboard summary after refresh: checked
  - holdings/portfolio totals remain consistent
- News collect: passed
  - total_fetched_count = `36`
  - new_count = `33`
  - duplicate_count = `3`
  - gpt_target_count = `10`
  - alert_target_count = `6`
- News DB latest state: checked
  - total_news_count = `51`
  - latest_news_published_at = `2026-07-07 14:22:00`
- GPT targets/status after refresh: checked
  - summary_pending_count = `5`
  - summary_done_count = `7`
  - filter_pending_count = `48`
  - filter_done_count = `1`
  - filter_failed_count = `5`
- GPT summary run: passed
  - dry_run = `false`
  - processed_count = `5`
  - model = `gpt-5.4-mini`
- GPT filter run: blocked by external quota
  - dry_run = `false`
  - processed_count = `0`
  - model = `gpt-5.4`
  - OpenAI API error = `insufficient_quota`
- Price alert dry-run: passed
  - evaluated_count = `7`
  - matched_count = `6`
  - sendable_count = `6`
  - sent_count = `0`
- News alert dry-run: passed
  - candidate_count = `2`
  - sendable_count = `0`
  - skipped_count = `2`
  - skipped_reasons = `already_sent: 2`
- Real Gmail sending: not executed

## Incomplete items

- GPT filter processing is not fully available in the current environment because the OpenAI API returned `insufficient_quota`
- 48 news items still remain in filter pending state

## Confirmation-needed items

- None

## Next step suggestions

- Resolve OpenAI API quota before depending on GPT filter results for live operation
- Re-run `/api/news/gpt/filter/run` after quota recovery
- Keep alert sending in dry-run until GPT filter and final recipient policy are reconfirmed

## Final completion statement

CODEX_TASK_2.23 실운영 시작 전 가격/뉴스 최신화 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
