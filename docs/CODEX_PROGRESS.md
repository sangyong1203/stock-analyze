# CODEX PROGRESS

## Current phase

- Phase: Playwright test-DB integration test — Stage 3
- Task: stocks / collection targets
- Status: completed, awaiting approval before Stage 4

## Playwright Stage 3 completed work

- Added a KOSDAQ non-holding stock and deterministic collection settings to the E2E seed
- Added stock API filter verification for search, market, favorite, and holding state
- Added stock screen KPI, search, market, and favorite-only filter verification
- Added real stock create, update, favorite toggle, and deactivate flow
- Added collection summary and filter API verification
- Added collection screen KPI, keyword, and collect-enabled filter verification
- Added manual include, manual exclude, reset, and recalculate flow
- Added collection rule create, update, disable, and delete flow
- Excluded the live KRX collection button because it calls an external API and mutates collected price data
- Found and fixed a real collection-stock detail lookup error after manual include/exclude

## Playwright Stage 3 verification result

| Item | Result |
|---|---|
| Stock API filters | passed |
| Stock screen filters/KPI | passed |
| Stock create/update | passed |
| Favorite toggle | passed |
| Stock deactivate | passed |
| Collection summary/filters | passed |
| Manual include/exclude | passed |
| Collection recalculate | passed |
| Collection rule CRUD | passed |
| Stage 3 tests | `7 passed` |
| Stage 1-2 regression | `10 passed` |
| Playwright total | `17 passed` |
| Frontend build | passed |
| Python compile check | passed |

## Stage 3 fixed issue

- `get_collection_stock_detail()` iterated the `(rows, total_count)` return value as if it were a row list.
- Manual include/exclude therefore saved the setting and then failed with HTTP 500 while serializing the response.
- Added a direct `get_collection_stock()` repository query and updated the service to use it.

## Stage 3 confirmation-needed items

- None

## Stage 3 next step gate

- Stage 4 news test has not started.
- GPT-related execution and assertions remain excluded.
- Start only after user approval.

## Playwright Stage 2 completed work

- Added deterministic dashboard seed data to the isolated E2E database
- Seeded 6 stocks, holdings, trades, news, memos, tags, one price alert, one alert history, and one successful job log
- Added real `/api/dashboard/summary` aggregate verification
- Verified portfolio totals, holding count, alert counts, memo/tag counts, and recent data
- Verified TOP 5 sorting and exclusion of the sixth item
- Verified dashboard KPI and summary panel rendering
- Verified five dashboard quick-action routes
- Added a dashboard full-page screenshot to the successful Playwright report
- Did not execute or assert GPT processing

## Playwright Stage 2 verification result

| Item | Result |
|---|---|
| Dashboard API aggregate | passed |
| Portfolio KPI rendering | passed |
| Holdings TOP 5 ordering | passed |
| Gainers/losers ordering | passed |
| Recent trades/news limit | passed |
| Alert history and summary | passed |
| Memo/tag summary | passed |
| Quick-action navigation | passed |
| Dashboard tests | `4 passed` |
| Stage 1 regression | `6 passed` |
| Playwright total | `10 passed` |
| Frontend build | passed |

## Stage 2 confirmation-needed items

- None

## Stage 2 next step gate

- Stage 3 stocks / collection test has not started.
- Start only after user approval.

## Playwright Stage 1 completed work

- Reviewed the two required MVP reference documents
- Installed Playwright Test `1.61.1` and Chromium
- Added an isolated SQLite database at `backend/stock_analyze_e2e.db`
- Added automatic E2E DB reset, Alembic migration, and default seed setup
- Connected the actual FastAPI backend on port `8001`
- Connected the actual Vue/Vite frontend on port `5174`
- Added authentication guard, callback, menu navigation, sidebar, and logout tests
- Added a successful authenticated dashboard screenshot to the HTML report
- Added an accessible label to the shared sidebar collapse button
- Excluded GPT execution and real Gmail sending

## Playwright Stage 1 verification result

| Item | Result |
|---|---|
| E2E DB migration | passed (`20260624_0002`) |
| E2E DB table count | passed (`27`) |
| Default seed | passed |
| FastAPI health/auth/dashboard APIs | passed |
| Authentication guard | passed |
| Authentication callback state | passed |
| 10-menu navigation | passed |
| Sidebar collapse/expand | passed |
| Logout | passed |
| Playwright total | `6 passed` |
| Frontend build | passed |

## 확인 필요 항목

- 항목: 실제 Google 계정 OAuth 승인 과정
- 관련 문서: `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md` 인증 방식
- 애매한 이유: Playwright 격리 브라우저에서 실제 개인 Google 계정과 인증 정보를 자동화하면 보안 및 외부 서비스 의존성이 발생함
- 가능한 선택지: 수동 브라우저 확인 / 별도 테스트용 Google 계정 정책 확정 후 제한적 검증
- 추천안: 실제 Google 계정 승인은 수동 점검으로 유지하고 앱 내부 callback, guard, logout만 자동화
- 현재 구현 여부: 보류

## Next step gate

- Stage 1 completed and Stage 2 was approved separately.

## Completed major work

- Reviewed:
  - `docs/CODEX_TASK_2.23.md`
  - `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
  - `docs/MVP_DB_SCHEMA_v1.2.md`
- Verified backend health
- Ran KRX daily collection on live DB
- Confirmed `latest_price_date` updated to `2025-07-07`
- Rechecked holdings, portfolio, and dashboard consistency after refresh
- Ran market news collection
- Confirmed live news count increased to `51`
- Confirmed latest news published time updated to `2026-07-07 14:22:00`
- Checked GPT summary/filter target status
- Ran GPT summary processing for 5 targets
- Confirmed GPT filter execution is currently blocked by OpenAI quota
- Ran:
  - `price alert dry-run`
  - `news alert dry-run`
- Added:
  - `docs/CODEX_TASK_2.23_REPORT.md`

## Verification result

| Item | Result |
|---|---|
| Backend health | passed |
| KRX daily collect | passed |
| Latest price date refresh | passed |
| Holdings/portfolio/dashboard consistency | passed |
| Market news collect | passed |
| Latest news timestamp refresh | passed |
| GPT summary execution | passed |
| GPT filter execution | blocked by external quota |
| Price alert dry-run | passed |
| News alert dry-run | passed |
| Real Gmail sent | no |

## Current validated configuration notes

- Current live DB status:
  - `stock_prices = 357946`
  - `latest_price_date = 2025-07-07`
  - `news = 51`
  - `latest_news_published_at = 2026-07-07 14:22:00`
- Current GPT operation risk:
  - summary pipeline is processable
  - filter pipeline currently returns `OpenAI API insufficient_quota`

## Confirmation-needed items

- None

## Next step suggestions

- Restore OpenAI API quota before live reliance on GPT filter output
- Re-run GPT filter once quota is available
- Keep real alert sending disabled until final live-operation approval
