# DEVELOPMENT REPORT

## Work overview

- Latest completed scope: `docs/CODEX_TASK_1.12.md`
- Implemented price alert CRUD, evaluation, Gmail send flow, and alerts page refresh.
- Prior 1.11 trade / holdings / portfolio work remains intact.

## Reference documents

- `docs/CODEX_TASK_1.12.md`
- `docs/CODEX_TASK_1.11.md`
- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

## Completed work

- Added `GET /api/price-alerts`
- Added `POST /api/price-alerts`
- Added `GET /api/price-alerts/{alert_id}`
- Added `PATCH /api/price-alerts/{alert_id}`
- Added `DELETE /api/price-alerts/{alert_id}`
- Added `POST /api/price-alerts/evaluate/dry-run`
- Added `POST /api/price-alerts/evaluate`
- Added `GET /api/price-alerts/summary`
- Added `GET /api/price-alerts/histories`
- Implemented alert conditions:
  - `TARGET_PRICE_ABOVE`
  - `TARGET_PRICE_BELOW`
  - `DROP_FROM_HIGH`
  - `RISE_FROM_LOW`
- Connected Gmail SMTP send
- Recorded `alert_histories` with `sent`, `failed`, `skipped`
- Applied same-day duplicate prevention
- Rebuilt frontend alerts page for CRUD, stock search, dry-run, actual send, and history view

## Generated files

- `docs/CODEX_TASK_1.12_REPORT.md`

## Modified files

- `backend/app/domains/alerts/schemas.py`
- `backend/app/domains/alerts/repository.py`
- `backend/app/domains/alerts/service.py`
- `backend/app/domains/alerts/router.py`
- `backend/app/main.py`
- `frontend/src/pages/main/alerts/AlertsPage.vue`
- `frontend/src/pages/main/alerts/service/alerts.api.ts`
- `frontend/src/pages/main/alerts/service/alerts.types.ts`
- `frontend/src/pages/main/alerts/service/alerts.constants.ts`
- `frontend/src/pages/main/alerts/service/alerts.mapper.ts`
- `frontend/src/pages/main/alerts/service/alerts.store.ts`
- `frontend/src/pages/main/alerts/service/alerts.utils.ts`
- `docs/CODEX_PROGRESS.md`

## Backend implementation result

- Backend API prefix changed from placeholder alerts menu route to `/api/price-alerts`.
- Current price is read from `stocks.current_price`.
- Recent high / low is read from `stock_prices` with `timeframe = "daily"`.
- Duplicate prevention is based on same-day `sent` history by `price_alert_id + stock_id + alert_type`.
- Actual evaluate persists `sent`, `failed`, and `skipped` histories.

## Frontend implementation result

- Alerts page now includes:
  - price alert list
  - create / edit / delete form
  - remote stock search
  - condition selector
  - dry-run button
  - actual send button
  - evaluation result table
  - history table

## DB implementation result

- No new table created
- No migration created
- Existing schema only used
- `price_alerts.base_price` is reused to store `lookback_days` because the current schema has no dedicated column

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
http://localhost:5173/alerts
```

## Test result

- `python -m compileall backend/app`: success
- `npm run build`: success
- CRUD validation: success
- `TARGET_PRICE_ABOVE`: success
- `TARGET_PRICE_BELOW`: success
- `DROP_FROM_HIGH`: success
- `RISE_FROM_LOW`: success
- dry-run validation: success
- actual Gmail send validation: 1 sent
- duplicate send validation: skipped with `already_sent_today`
- `/api/price-alerts/summary`: 200
- `/api/price-alerts/histories`: 200
- Regression checks:
  - `/health`: 200
  - `/api/auth/status`: 200
  - `/api/prices/summary`: 200
  - `/api/charts/stocks/2/ohlcv?limit=130`: 200
  - `/api/portfolio/summary`: 200
  - `/api/news/alerts/send/dry-run`: 200

## Incomplete items

- Stocks / portfolio quick-entry button into alerts page is not added.

## Confirmation-needed items

- Some stock names are already broken in DB encoding, so alert subject / body inherits that value.

## Next step suggestions

- Add quick-entry navigation into alerts from stocks / portfolio pages
- Run a separate stock master data cleanup for broken names

## Final completion statement

가격 알림 조건과 발송 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.

## CODEX_TASK_1.12 Fix Note

- Removed `lookback_days` storage from `price_alerts.base_price`.
- `DROP_FROM_HIGH` and `RISE_FROM_LOW` now use fixed recent 60-day high / low logic only.
- Alerts frontend now shows `최근 60일 기준` instead of editable `lookback_days`.
- Verified there were no remaining non-null `base_price` rows in live DB.
- Revalidated:
  - dry-run success
  - actual evaluate success
  - Gmail send success
  - duplicate send skip response success
