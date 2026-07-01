# CODEX TASK 1.16 REPORT

## 1. Work overview

- Task: `docs/CODEX_TASK_1.16.md`
- Scope: MVP integration verification, regression check, DB consistency check, and report cleanup
- Constraint kept:
  - no new feature
  - no new table
  - no new migration
  - existing MVP schema only

## 2. Backend API verification result

| API | Result |
|---|---|
| `/health` | 200 |
| `/api/auth/status` | 200 |
| `/api/settings` | 200 |
| `/api/jobs` | 200 |
| `/api/jobs/summary` | 200 |
| `/api/stocks` | 200 |
| `/api/collection/stocks/summary` | 200 |
| `/api/prices/summary` | 200 |
| `/api/prices/markets/KOSPI/latest?limit=3` | 200 |
| `/api/prices/markets/KOSDAQ/latest?limit=3` | 200 |
| `/api/charts/stocks/2/ohlcv?limit=130` | 200 |
| `/api/news` | 200 |
| `/api/news/summary` | 200 |
| `/api/news/gpt/targets` | 200 |
| `/api/news/gpt/status` | 200 |
| `/api/news/alerts/summary` | 200 |
| `/api/news/alerts/send/dry-run` | 200 |
| `/api/price-alerts` | 200 |
| `/api/price-alerts/summary` | 200 |
| `/api/price-alerts/evaluate/dry-run` | 200 |
| `/api/funds/summary` | 200 |
| `/api/trades` | 200 |
| `/api/holdings/summary` | 200 |
| `/api/portfolio/summary` | 200 |
| `/api/memos` | 200 |
| `/api/tags` | 200 |
| `/api/dashboard/summary` | 200 |

## 3. Key live summary values

- Jobs summary:
  - `total_count`: `8`
  - `enabled_count`: `8`
  - `failed_count`: `0`
  - `never_run_count`: `3`
- Prices summary:
  - `total_price_rows`: `352427`
  - `latest_price_date`: `2025-06-24`
  - `kospi_price_count`: `123090`
  - `kosdaq_price_count`: `229337`
  - `latest_updated_stocks_count`: `2757`
- News summary:
  - `total_news_count`: `18`
  - `today_news_count`: `4`
  - `linked_stock_news_count`: `8`
  - `gpt_summary_target_count`: `2`
  - `alert_target_count`: `2`
- Price alerts summary:
  - `total_count`: `0`
  - `sent_count`: `0`
- Funds summary:
  - `active_pool_count`: `0`
  - `total_cash`: `0`
- Holdings summary:
  - `holding_count`: `0`
- Portfolio summary:
  - `total_asset_value`: `0`
  - `holding_count`: `0`

## 4. Frontend verification result

- Verified route entry success for:
  - `/dashboard`
  - `/stocks`
  - `/collection`
  - `/news`
  - `/portfolio`
  - `/trades`
  - `/alerts`
  - `/charts`
  - `/memos`
  - `/settings`
- Route entry checks returned HTTP 200 from the frontend dev server
- `npm run build` completed successfully

## 5. DB verification result

- `python -m alembic current`: `20260624_0002 (head)`
- Expected MVP tables: `27`
- Actual non-system tables: `27`
- Missing tables: none
- Extra tables: none
- `stock_prices` duplicate groups on `stock_id + date + timeframe`: `0`
- `price_alerts` rows: `0`
- `alert_histories` rows: `2`
- `trades` rows: `0`
- `holdings` rows: `0`
- `fund_transactions` rows: `0`
- `tag_links` orphan rows: `0`
- `trade_news_links` orphan rows: `0`

## 6. Confirmation-needed items

- Browser-based visual inspection was not available in the current Codex session, so frontend verification stayed at route-entry and build level
- Some Korean text had previously appeared mojibake in tool output, but this task did not confirm a DB-side corruption case

## 7. Final assessment

- MVP integration verification passed within the current task scope
- No schema drift was found
- No duplicate stock price groups were found
- No orphan link rows were found
- No code change was required for this task

## 8. Next step suggestion

- If release confidence needs a UI-level pass, run a short manual browser check for dashboard, charts, alerts, and settings
- If encoding issues are reproduced later, isolate source ingestion, DB storage, and response rendering before changing live data
