# DEVELOPMENT REPORT

## Work overview

- Latest completed scope: `docs/CODEX_TASK_2.5.md`
- Scope handled in this task: initial portfolio current-price validation, latest KRX price refresh, holdings recalculation, and reporting
- Constraint kept:
  - no new feature
  - no new table
  - no new migration
  - no quantity change
  - no average price change
  - no trade edit or delete
  - no holdings direct edit
  - no Gmail send

## Reference documents

- `docs/CODEX_TASK_2.5.md`
- `docs/DEVELOPMENT_REPORT.md`
- `docs/NON_ETF_INITIAL_PORTFOLIO_INPUT_REPORT.md`
- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

## Completed work

- Reviewed only the immediately required prior reports for this task
- Verified the 4-stock non-ETF initial portfolio remained unchanged in quantity and average price
- Confirmed the holdings calculation path uses `stocks.current_price`
- Verified pre-refresh latest price date was `2025-06-24`
- Verified held-stock latest `stock_prices` rows were also dated `2025-06-24`
- Tested existing KRX daily collection in dry-run mode for multiple dates
- Confirmed `2025-07-03` is the latest date that returned real KRX rows in this run, while `2026-07-03` returned `0`
- Executed existing KRX daily collection for `2025-07-03`
- Re-ran holdings recalculation after the price refresh completed
- Re-verified holdings, holdings summary, portfolio summary, dashboard summary, and price summary
- Compared system-recalculated market values against the user-provided previous reference values
- Ran backend compile and frontend build again
- Performed a limited dev-server browser check for `/portfolio` and `/dashboard`

## Generated files

- `docs/INITIAL_PORTFOLIO_PRICE_VALIDATION_REPORT.md`
- `docs/CODEX_TASK_2.5_REPORT.md`

## Modified files

- `docs/CODEX_PROGRESS.md`
- `docs/DEVELOPMENT_REPORT.md`

## Backend implementation result

- No backend code change
- Existing KRX daily collection API was reused as-is
- Existing holdings recalculation API was reused as-is
- Important sequencing note:
  - a holdings recalculation triggered before the daily collection completed still reflected the older price basis
  - after `2025-07-03` collection completed, running holdings recalculation again updated the persisted holding valuation fields correctly

## Frontend implementation result

- No frontend code change
- `npm run build` passed
- Frontend API base remains `http://127.0.0.1:8000` by default
- Browser validation was partial because the in-app browser still showed `Failed to fetch` during `/portfolio` and `/dashboard`
- Final correctness was therefore confirmed by API and DB validation rather than browser-rendered KPI values

## DB implementation result

- No schema change
- No new table
- No migration
- `stock_prices` summary changed:
  - before refresh: `latest_price_date = 2025-06-24`
  - after refresh: `latest_price_date = 2025-07-03`
- KRX daily collection result for `2025-07-03`:
  - fetched `2758`
  - inserted `2758`
  - updated `0`
  - stock created `1`
- Final held-stock price basis:
  - `006400` latest close `185300`
  - `034020` latest close `61900`
  - `028050` latest close `23200`
  - `035420` latest close `253000`
- Final holdings validation:
  - quantity unchanged
  - average price unchanged
  - current price equals latest `stock_prices.close`
  - `market_value = current_price * quantity`
  - `unrealized_profit_loss = market_value - total_buy_amount`

## Execution method

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
python -m compileall app
```

```bash
cd frontend
npm run build
npm run dev
```

Main API checks:

```text
/api/prices/summary
/api/prices/collect/krx/daily
/api/holdings
/api/holdings/recalculate
/api/holdings/summary
/api/portfolio/summary
/api/dashboard/summary
```

## Test result

- `python -m compileall app`: success
- `npm run build`: success
- dry-run daily collect `2025-06-25`: success
- dry-run daily collect `2025-06-30`: success
- dry-run daily collect `2025-07-03`: success
- dry-run daily collect `2026-07-03`: fetched `0`
- actual daily collect `2025-07-03`: success
- `/api/prices/summary`: 200
  - `total_price_rows = 355185`
  - `latest_price_date = 2025-07-03`
- `/api/holdings`: 200
  - row count `4`
- `/api/holdings/summary`: 200
  - `holding_count = 4`
  - `total_market_value = 2283500.00`
  - `total_unrealized_profit_loss = -2824590.00`
- `/api/portfolio/summary`: 200
  - `total_invested_amount = 5108090.00`
  - `total_market_value = 2283500.00`
  - `total_unrealized_profit_loss = -2824590.00`
- `/api/dashboard/summary`: 200
  - `portfolio_summary.total_market_value = 2283500.00`
  - `holding_summary.total_market_value = 2283500.00`
  - dashboard top holdings reflect the same 4 stocks
- Browser dev check:
  - route shell load: success
  - rendered live values verification: not completed
  - observed issue: `Failed to fetch`

## Incomplete items

- Full browser UI verification with rendered live valuation data was not completed because the in-app browser fetch failed

## Confirmation-needed items

- The system date in this environment is `2026-07-03`, but the latest KRX date that actually returned rows in this run was `2025-07-03`
- This report treats `2025-07-03` as the latest confirmed trade-date basis for valuation because `2026-07-03` dry-run returned `0`

## Next step suggestions

- Continue future validation or input tasks from the refreshed `2025-07-03` price basis
- If browser QA is required in the next task, resolve the current browser fetch failure before relying on UI-level assertions

## Final completion statement

CODEX_TASK_2.5 초기 포트폴리오 현재가 검증 작업 완료했습니다.
DEVELOPMENT_REPORT.md와 INITIAL_PORTFOLIO_PRICE_VALIDATION_REPORT.md를 확인해 주세요.
