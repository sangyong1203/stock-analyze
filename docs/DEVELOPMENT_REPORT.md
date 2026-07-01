# DEVELOPMENT REPORT

## Work overview

- Latest completed scope: `docs/CODEX_TASK_1.17.md`
- Scope handled in this task: MVP manual QA, sample data flow verification, encoding check, cleanup verification, and documentation update
- Constraint kept:
  - no new feature
  - no new table
  - no new migration
  - existing MVP schema only

## Reference documents

- `docs/CODEX_TASK_1.17.md`
- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

## Completed work

- Attempted browser-based localhost QA using the available browser runtime path
- Confirmed that no browser instance was available in the current Codex session
- Re-checked major backend APIs:
  - `/health`
  - `/api/auth/status`
  - `/api/dashboard/summary`
  - `/api/stocks`
  - `/api/news`
  - `/api/prices/summary`
  - `/api/portfolio/summary`
  - `/api/price-alerts/summary`
  - `/api/jobs/summary`
- Re-checked frontend route entry points:
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
- Executed sample data QA flow on live DB:
  - created test fund pool
  - created deposit
  - created Samsung Electronics buy trade
  - verified holdings summary update
  - verified portfolio summary update
  - created one price alert
  - verified price-alert dry-run
  - executed non-sending evaluate path and recorded one skipped alert history
  - created one trade memo
  - created one trade tag and link
  - created one trade-news link
  - verified dashboard recent trade, memo, and alert reflection
  - cleaned test data
- Re-checked post-cleanup summary values to confirm baseline restoration
- Re-checked API-visible Korean text across stock, news, alert, dashboard, and trade-related responses
- Added task report and manual QA report documents

## Generated files

- `docs/CODEX_TASK_1.17_REPORT.md`
- `docs/MVP_MANUAL_QA_REPORT.md`

## Modified files

- `docs/CODEX_PROGRESS.md`
- `docs/DEVELOPMENT_REPORT.md`

## Backend implementation result

- No backend code change was added in this task
- Major regression APIs responded successfully in the current live DB environment
- Sample data flow verified these connected areas:
  - funds
  - trades
  - holdings
  - portfolio summary
  - price alerts
  - alert histories
  - memos
  - tags
  - trade-news links
  - dashboard summary
- Sample QA values during the run:
  - sample stock: `삼성전자 (005930)`
  - deposit amount: `1000000`
  - buy trade quantity: `2`
  - buy trade price: `60500`
  - buy trade total amount: `121100`
  - post-buy cash: `878900`
  - post-buy holding count: `1`
  - post-buy market value: `121000`
  - post-buy unrealized profit/loss: `-100`
  - sample price alert type: `TARGET_PRICE_ABOVE`
  - sample price alert target: `160500`
  - evaluate result: skipped with `condition_not_met`

## Frontend implementation result

- No frontend code change was added in this task
- Frontend dev server responded successfully for all major route entry points
- Production build completed successfully
- Browser runtime was not available in this Codex session, so visual layout review could not be automated here
- Current frontend verification level for this task was:
  - route entry response
  - API-backed data flow verification
  - production build result

## DB implementation result

- No new table created
- No migration created
- Existing schema only used
- Sample QA data was inserted and then removed successfully
- Post-cleanup summary values returned to baseline:
  - `funds.active_pool_count`: `0`
  - `funds.total_cash`: `0`
  - `holdings.holding_count`: `0`
  - `portfolio.total_asset_value`: `0`
  - `price_alerts.total_count`: `0`
- API-visible encoding samples showed no replacement character in checked values:
  - `stocks.name`
  - `news.title`
  - `news.source`
  - `alert_histories.title`
  - `dashboard.recent_news.title`
  - `dashboard.recent_trades.stock_name`
  - `price_alerts.stock_name`

## Execution method

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

```text
http://127.0.0.1:5173/dashboard
http://127.0.0.1:5173/stocks
http://127.0.0.1:5173/collection
http://127.0.0.1:5173/news
http://127.0.0.1:5173/portfolio
http://127.0.0.1:5173/trades
http://127.0.0.1:5173/alerts
http://127.0.0.1:5173/charts
http://127.0.0.1:5173/memos
http://127.0.0.1:5173/settings
```

## Test result

- `python -m compileall app`: success
- `npm run build`: success
- Major regression APIs: all 200
- Frontend route entry checks: all 200
- Sample fund pool create: success
- Sample deposit create: success
- Sample buy trade create: success
- Holdings summary after buy: success
- Portfolio summary after buy: success
- Price alert create: success
- Price alert dry-run: success
- Price alert evaluate without send: success
- Trade memo create: success
- Trade tag link create: success
- Trade-news link create: success
- Dashboard recent trade reflection: success
- Dashboard recent memo reflection: success
- Dashboard recent alert reflection: success
- Test data cleanup: success

## Incomplete items

- Full visual browser inspection was not completed because no browser instance was available in the session

## Confirmation-needed items

- A short manual browser pass is still needed if true UI-level release confidence is required
- The mojibake concern was not reproduced in checked API and DB-visible paths, but final browser render confirmation was not available here

## Next step suggestions

- Perform a short manual visual pass for dashboard, news, trades, alerts, and settings pages in a real browser
- If mojibake is later reproduced, isolate source ingestion, DB storage, API response encoding, and frontend rendering before modifying data

## Final completion statement

MVP manual QA, data consistency, and encoding verification work is complete.
Please check `DEVELOPMENT_REPORT.md`.
