# DEVELOPMENT REPORT

## Work overview

- Latest completed scope: `docs/CODEX_TASK_2.4.md`
- Scope handled in this task: non-ETF initial portfolio input, live DB validation, and reporting
- Constraint kept:
  - no new feature
  - no new table
  - no new migration
  - no ETF stock master insertion
  - no ETF trade insertion
  - no holdings direct edit
  - no Gmail send

## Reference documents

- `docs/CODEX_TASK_2.4.md`
- `docs/DEVELOPMENT_REPORT.md`
- `docs/INITIAL_PORTFOLIO_INPUT_REPORT.md`
- `docs/FIRST_OPERATION_DATA_INPUT_GUIDE.md`
- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

## Completed work

- Reviewed the prior blocked-input context from `CODEX_TASK_2.3`
- Kept ETF inputs excluded per task decision
- Verified the live DB baseline was still empty before insertion:
  - fund pools: 0
  - fund transactions: 0
  - trades: 0
  - holdings: 0
- Verified the four non-ETF target stocks already exist in `stocks`
- Verified task-specific backup file exists for the non-ETF input run
- Created fund pool `기본 투자계좌`
- Inserted initial deposit `5,108,090`
- Inserted four initial BUY trades dated `2026-07-03`
- Verified holdings recalculation, portfolio summary, dashboard summary, and trade list by API
- Verified no ETF trades and no ETF holdings were created
- Ran backend compile and frontend build
- Performed a limited browser preview check for `/portfolio`, `/trades`, `/dashboard`

## Generated files

- `docs/NON_ETF_INITIAL_PORTFOLIO_INPUT_REPORT.md`
- `docs/CODEX_TASK_2.4_REPORT.md`

## Modified files

- `docs/CODEX_PROGRESS.md`
- `docs/DEVELOPMENT_REPORT.md`

## Backend implementation result

- No backend code change
- Live DB input completed through existing funds and trades APIs
- Inserted objects:
  - fund pools: 1
  - deposit transactions: 1
  - BUY trades: 4
- API validations succeeded for:
  - `/api/funds/summary`
  - `/api/trades`
  - `/api/holdings`
  - `/api/holdings/summary`
  - `/api/portfolio/summary`
  - `/api/dashboard/summary`

## Frontend implementation result

- No frontend code change
- `npm run build` passed
- Frontend routes confirmed:
  - `/portfolio`
  - `/trades`
  - `/dashboard`
- Browser preview opened the route shells successfully
- Preview-mode browser validation was partial because page-level `/api/*` fetch failed during `vite preview`, so final data correctness was validated by API responses rather than preview rendering

## DB implementation result

- No schema change
- No new table
- No migration
- Backup file used for this task:
  - `storage/backups/stock_analyze_before_non_etf_initial_input_20260703_111724.db`
- Inserted non-ETF holdings only:
  - `006400` quantity `5`, average price `596970`
  - `034020` quantity `10`, average price `105215`
  - `028050` quantity `10`, average price `55809`
  - `035420` quantity `2`, average price `256500`
- Explicitly excluded ETF codes:
  - `368590`
  - `411060`
  - `442320`
  - `422420`
  - `487240`
- ETF validation result:
  - ETF trade rows: `0`
  - ETF holding rows: `0`

## Execution method

```bash
cd backend
python -m compileall app
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```bash
cd frontend
npm run build
npm run preview --host 0.0.0.0
```

Checked APIs:

```text
/health
/api/funds/summary
/api/trades
/api/holdings
/api/holdings/summary
/api/portfolio/summary
/api/dashboard/summary
```

## Test result

- `python -m compileall app`: success
- `npm run build`: success
- `/health`: 200
- `/api/funds/summary`: 200
  - `active_pool_count = 1`
  - `total_cash = 0`
  - `total_deposit_amount = 5108090.00`
  - `transaction_count = 5`
- `/api/trades`: 200
  - row count `4`
- `/api/holdings/summary`: 200
  - `holding_count = 4`
  - `closed_holding_count = 0`
- `/api/portfolio/summary`: 200
  - `holding_count = 4`
  - `total_invested_amount = 5108090.00`
  - `total_cash = 0`
- `/api/dashboard/summary`: 200
  - portfolio summary and holding summary aligned with API totals
  - recent trades included the 4 inserted BUY rows
- Browser preview:
  - route shell load: success
  - console error-free data rendering: not confirmed in preview mode

## Incomplete items

- Full browser UI verification with live API-connected rendering was not completed in this task

## Confirmation-needed items

- Preview-mode `/api/*` fetch failure should be rechecked only if the user wants browser-level QA beyond the validated API results

## Next step suggestions

- Continue future operational tasks from the current four-stock non-ETF baseline
- If visual QA is required, rerun browser validation on the actual frontend runtime configuration that resolves API requests correctly

## Final completion statement

CODEX_TASK_2.4 ETF 제외 초기 포트폴리오 입력 작업 완료했습니다.
DEVELOPMENT_REPORT.md와 NON_ETF_INITIAL_PORTFOLIO_INPUT_REPORT.md를 확인해 주세요.
