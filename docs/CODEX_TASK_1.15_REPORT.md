# CODEX TASK 1.15 REPORT

## 1. Work overview

- Task: `docs/CODEX_TASK_1.15.md`
- Scope: scheduled job runner API and frontend manual job execution UI
- Constraint kept:
  - no new table
  - no new migration
  - existing MVP schema only

## 2. Implemented API

| API | Result |
|---|---|
| `GET /api/jobs` | implemented |
| `GET /api/jobs/{job_id}` | implemented |
| `POST /api/jobs/{job_id}/run` | implemented |
| `POST /api/jobs/run` | implemented |
| `GET /api/jobs/summary` | implemented |

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

- Job rows are read from `scheduled_jobs`
- Manual run merges row `config_json` with request overrides
- Existing price, news, GPT, and alert domain services are reused for execution
- Job status and message are recorded into `system_logs`
- `last_status` and `last_message` are derived from the latest related log entry

## 5. Frontend connection result

- Settings page now shows job status, last message, and manual run buttons
- Dashboard page now shows job summary counts

## 6. Test result

- `python -m compileall backend/app`: success
- `npm run build`: success
- `/api/jobs`: 200
- `/api/jobs/summary`: 200
- `krx_price_daily` dry-run: success
- `naver_news_collect` manual run: success
- `news_alert_candidate` manual run: success
- `price_alert_evaluate` dry-run: success
- `POST /api/jobs/run`: success
- Regression APIs: all 200

## 7. Confirmation-needed items

- `scheduled_jobs` lacks dedicated status/message columns, so the UI uses derived values from `system_logs`
- OpenAI quota failure was not reproduced in the current environment

## 8. Next step suggestion

- Add richer job config editing only if a follow-up task requires per-run tuning from UI
- Re-check GPT failed logging on a real upstream quota or provider error
