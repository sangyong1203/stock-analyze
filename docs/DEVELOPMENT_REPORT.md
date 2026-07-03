# DEVELOPMENT REPORT

## Work overview

- Latest completed scope: `docs/CODEX_TASK_2.6.md`
- Scope handled in this task: browser `Failed to fetch` root-cause isolation, minimal fix, and portfolio UI validation
- Constraint kept:
  - no portfolio data change
  - no quantity change
  - no average price change
  - no trade edit or delete
  - no holdings direct edit
  - no new table
  - no migration
  - no Gmail send

## Reference documents

- `docs/CODEX_TASK_2.6.md`
- `docs/DEVELOPMENT_REPORT.md`
- `docs/INITIAL_PORTFOLIO_PRICE_VALIDATION_REPORT.md`
- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

## Completed work

- Reviewed only the immediately required prior reports for this task
- Confirmed the validated portfolio target values from `CODEX_TASK_2.5`
- Checked frontend API base URL handling
- Checked backend CORS middleware and local-origin settings
- Identified the root cause of browser `Failed to fetch`
- Applied a minimal backend CORS fix so localhost and `127.0.0.1` with varying local ports are accepted
- Re-verified CORS preflight for:
  - `http://127.0.0.1:5174`
  - `http://127.0.0.1:4173`
  - `http://localhost:5173`
- Rechecked direct API responses to confirm portfolio data remained unchanged
- Launched the frontend dev server on `http://127.0.0.1:5173`
- Verified `/portfolio`, `/dashboard`, and `/trades` render actual data in the browser
- Re-ran backend compile and frontend build

## Generated files

- `docs/PORTFOLIO_BROWSER_FETCH_FIX_REPORT.md`
- `docs/CODEX_TASK_2.6_REPORT.md`

## Modified files

- `backend/app/core/config.py`
- `backend/app/main.py`
- `docs/CODEX_PROGRESS.md`
- `docs/DEVELOPMENT_REPORT.md`

## Backend implementation result

- Backend code changed only in CORS configuration
- Root cause:
  - frontend used the backend directly at `http://127.0.0.1:8000`
  - backend allowed-origins were pinned to `5173`
  - when Vite dev or preview ran on another local port such as `5174` or `4173`, preflight requests were rejected
- Applied fix:
  - preserved the explicit configured origins
  - added `allowed_origin_regex = ^https?://(localhost|127\.0\.0\.1)(:\d+)?$`
  - wired that regex into `CORSMiddleware`
- No API behavior change beyond allowing local-browser origins on alternate ports

## Frontend implementation result

- No frontend code change
- `npm run build` passed
- Frontend default API base remains `http://127.0.0.1:8000`
- Browser UI validation succeeded on the dev server after the backend CORS fix
- Visible pages now render live portfolio and trade data instead of staying in the failed-fetch state

## DB implementation result

- No schema change
- No new table
- No migration
- No data mutation was performed for portfolio/trades/funds/holdings in this task
- Verified target values remained unchanged:
  - `total_cash = 0`
  - `total_invested_amount = 5108090.00`
  - `total_market_value = 2283500.00`
  - `total_unrealized_profit_loss = -2824590.00`
  - `holding_count = 4`

## Execution method

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
python -m compileall app
```

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
npm run build
```

Main validation:

```text
CORS preflight to /api/portfolio/summary
/health
/api/portfolio/summary
/api/holdings
/api/holdings/summary
/api/dashboard/summary
/portfolio
/dashboard
/trades
```

## Test result

- `python -m compileall app`: success
- `npm run build`: success
- preflight from `http://127.0.0.1:5174`: 200
- preflight from `http://127.0.0.1:4173`: 200
- preflight from `http://localhost:5173`: 200
- `/health`: 200
- `/api/portfolio/summary`: 200
  - `total_market_value = 2283500.00`
  - `total_unrealized_profit_loss = -2824590.00`
- `/api/holdings/summary`: 200
  - `holding_count = 4`
- `/api/dashboard/summary`: 200
  - `portfolio_summary.total_market_value = 2283500.00`
- Browser `/portfolio`:
  - 4 holdings visible
  - `총 자산 2,283,500원`
  - `평가금액 2,283,500원`
  - `평가손익 -2,824,590원`
  - `현금 잔고 0원`
- Browser `/dashboard`:
  - `총 자산 2,283,500원`
  - `평가 손익 -2,824,590원`
  - `보유 종목 4`
  - `총 매수금액 5,108,090원`
- Browser `/trades`:
  - 4 trade rows visible
  - `삼성SDI`, `두산에너빌리티`, `삼성E&A`, `NAVER` rendered

## Incomplete items

- A stale older `4173` browser log entry still appeared in the shared in-app browser log buffer, even though the current `5173` pages rendered correctly after the fix

## Confirmation-needed items

- If a fully clean console-log audit is required, it should be rerun in a fresh browser session
- For this task scope, the visible UI state and current CORS preflight/API behavior are sufficient to confirm the active fetch path is working

## Next step suggestions

- Continue local browser QA with `127.0.0.1` consistently for frontend and backend
- If preview-mode QA is used later, the backend now also accepts alternate local preview ports

## Final completion statement

CODEX_TASK_2.6 브라우저 Failed to fetch 수정 및 포트폴리오 UI 검증 작업 완료했습니다.
DEVELOPMENT_REPORT.md와 PORTFOLIO_BROWSER_FETCH_FIX_REPORT.md를 확인해 주세요.
