# SCHEDULED JOB REPORT

## 1. Work overview

- Implemented manual scheduled job runner structure on top of existing `scheduled_jobs`
- Reused current domain services for price, news, GPT, and alert-related execution

## 2. Implemented API

- `GET /api/jobs`
- `GET /api/jobs/{job_id}`
- `POST /api/jobs/{job_id}/run`
- `POST /api/jobs/run`
- `GET /api/jobs/summary`

## 3. Supported job type

- `krx_price_daily`
- `krx_price_range`
- `naver_news_collect`
- `gpt_news_summary`
- `gpt_news_filter`
- `news_alert_candidate`
- `news_alert_send`
- `price_alert_evaluate`

## 4. Job execution method

- Reads config from `scheduled_jobs.config_json`
- Allows request-time override for `dry_run` and config values
- Writes run result logs into `system_logs`
- Updates `scheduled_jobs.last_run_at`
- Derives latest status/message from the newest related log

## 5. Frontend connection result

- Settings page now shows job rows with run controls
- Dashboard page shows job summary counts
- Recent run results are displayed in the settings page

## 6. Test result

- `python -m compileall backend/app`: success
- `npm run build`: success
- `/api/jobs`: 200
- `/api/jobs/summary`: 200
- `krx_price_daily` dry-run: success
- `naver_news_collect`: success
- `news_alert_candidate`: success
- `price_alert_evaluate` dry-run: success
- `POST /api/jobs/run`: success

## 7. Confirmation-needed items

- Current schema has no dedicated status/message columns for `scheduled_jobs`
- GPT quota failure path was implemented but not triggered in this run

## 8. Next step suggestion

- Add richer config editing only if future manual-ops workflows demand it
- Re-verify failed logging during a real upstream API failure
