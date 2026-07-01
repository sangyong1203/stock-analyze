# DEVELOPMENT REPORT

## Work overview

- Latest completed scope: `docs/CODEX_TASK_1.15.md`
- Implemented scheduled job runner APIs and settings-page job management UI
- Prior dashboard, memo/tag, and alert work remains intact

## Reference documents

- `docs/CODEX_TASK_1.15.md`
- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

## Completed work

- Added `GET /api/jobs`
- Added `GET /api/jobs/{job_id}`
- Added `POST /api/jobs/{job_id}/run`
- Added `POST /api/jobs/run`
- Added `GET /api/jobs/summary`
- Added job runner support for:
  - `krx_price_daily`
  - `krx_price_range`
  - `naver_news_collect`
  - `gpt_news_summary`
  - `gpt_news_filter`
  - `news_alert_candidate`
  - `news_alert_send`
  - `price_alert_evaluate`
- Added `system_logs`-based status tracking for job runs
- Updated default scheduled job seed definitions
- Updated settings page to show:
  - job list
  - enabled state
  - last status
  - last run timestamp
  - last message
  - run buttons
  - recent run history
- Added job summary card to dashboard page

## Generated files

- `docs/CODEX_TASK_1.15_REPORT.md`
- `docs/SCHEDULED_JOB_REPORT.md`

## Modified files

- `backend/app/db/init_db.py`
- `backend/app/domains/jobs/__init__.py`
- `backend/app/domains/jobs/repository.py`
- `backend/app/domains/jobs/router.py`
- `backend/app/domains/jobs/schemas.py`
- `backend/app/domains/jobs/service.py`
- `backend/app/main.py`
- `frontend/src/pages/main/dashboard/DashboardPage.vue`
- `frontend/src/pages/main/settings/SettingsPage.vue`
- `frontend/src/pages/main/settings/service/settings.api.ts`
- `frontend/src/pages/main/settings/service/settings.types.ts`
- `docs/CODEX_PROGRESS.md`

## Backend implementation result

- Jobs API is exposed at `/api/jobs`
- Supported job rows are ensured in `scheduled_jobs` without adding new tables
- Legacy seed rows are ignored in jobs API when a newer supported key already exists
- `last_status` and `last_message` are derived from `system_logs` because the table has no dedicated columns
- Job execution is synchronous manual runner scope only; no OS cron or background daemon was added

## Frontend implementation result

- Settings page now serves as the manual job runner UI
- Dashboard page now shows current job summary counts
- Loading, error, and recent-result states are handled for the jobs section

## DB implementation result

- No new table created
- No migration created
- Existing schema only used
- Used existing tables: `scheduled_jobs`, `system_logs`, `stock_prices`, `news_collect_jobs`, `news_collect_job_items`, `news`, `price_alerts`, `alert_histories`

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
http://localhost:5173/settings
http://localhost:5173/dashboard
```

## Test result

- `python -m compileall backend/app`: success
- `npm run build`: success
- `/api/jobs`: 200
- `/api/jobs/{job_id}`: 200
- `/api/jobs/summary`: 200
- `krx_price_daily` dry-run: success
  - `bas_date`: `20250624`
  - `fetched_count`: `2757`
- `naver_news_collect` manual run: success
  - `new_count`: `1`
  - `duplicate_count`: `2`
- `news_alert_candidate` manual run: success
  - `processed_count`: `18`
- `price_alert_evaluate` dry-run: success
  - `evaluated_count`: `0`
- `POST /api/jobs/run` batch run: success
- `gpt_news_summary` run returned success in current environment, so quota failure was not reproduced
- Regression checks:
  - `/health`: 200
  - `/api/auth/status`: 200
  - `/api/prices/summary`: 200
  - `/api/dashboard/summary`: 200
  - `/api/portfolio/summary`: 200
  - `/api/price-alerts/summary`: 200
  - `/api/news/alerts/send/dry-run`: 200

## Incomplete items

- OpenAI quota failure was not reproduced in this run, so quota-specific failed log output was not observed directly

## Confirmation-needed items

- `scheduled_jobs` has no `last_status` or `last_message` columns, so those fields are currently derived from `system_logs`
- Existing legacy scheduled job rows remain in the table, but unsupported duplicates are hidden from the jobs API

## Next step suggestions

- Add dedicated per-job config editing UI only if the next task requires richer manual overrides
- Re-check GPT failed-job logging when an actual upstream quota or provider error occurs

## Final completion statement

수동 수집 / scheduled_jobs 기반 실행 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
