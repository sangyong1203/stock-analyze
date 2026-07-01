# CODEX PROGRESS

## Current phase

- Phase: scheduled job runner and manual job execution UI
- Task document: `docs/CODEX_TASK_1.15.md`
- Status: implementation and verification complete

## Completed major work

- Added `jobs` backend domain
- Added `GET /api/jobs`
- Added `GET /api/jobs/{job_id}`
- Added `POST /api/jobs/{job_id}/run`
- Added `POST /api/jobs/run`
- Added `GET /api/jobs/summary`
- Added supported job types:
  - `krx_price_daily`
  - `krx_price_range`
  - `naver_news_collect`
  - `gpt_news_summary`
  - `gpt_news_filter`
  - `news_alert_candidate`
  - `news_alert_send`
  - `price_alert_evaluate`
- Reused existing prices, news, GPT, and alert services through job runner dispatch
- Recorded job run status and messages into `system_logs`
- Derived `last_status` and `last_message` from job logs because `scheduled_jobs` has no dedicated columns
- Updated settings page with job list, recent status, and run buttons
- Added job summary card to dashboard
- Backend compile passed
- Frontend build passed

## Verification result

| Item | Result |
|---|---|
| `GET /api/jobs` | 200 |
| `GET /api/jobs/{job_id}` | 200 |
| `GET /api/jobs/summary` | 200 |
| `POST /api/jobs/{job_id}/run` | success |
| `POST /api/jobs/run` | success |
| `krx_price_daily` dry-run | success |
| `naver_news_collect` manual run | success |
| `news_alert_candidate` manual run | success |
| `price_alert_evaluate` dry-run | success |
| `python -m compileall backend/app` | success |
| `npm run build` | success |
| Regression API | all 200 |

## Confirmation-needed items

- Item: `scheduled_jobs` has no `last_status` or `last_message` columns
- Related document: `docs/CODEX_TASK_1.15.md`
- Reason: task asked to expose those values, but current schema only stores `last_run_at` and `next_run_at`
- Possible options: derive from `system_logs`, or add schema fields later
- Recommendation: keep current derived approach and avoid schema change in MVP
- Current implementation status: derived from `system_logs`

- Item: OpenAI quota failure was not reproduced during this verification run
- Related document: `docs/CODEX_TASK_1.15.md`
- Reason: current `gpt_news_summary` run completed without quota error
- Possible options: accept implementation review only, or reproduce later in a constrained environment
- Recommendation: keep the exception-to-failed logging path and re-check only if a real quota incident occurs
- Current implementation status: failure path implemented, quota-specific incident not reproduced

## Next step suggestions

- If needed later, add dedicated job edit fields for run-specific config presets in the settings UI
- Re-check GPT failure logging when a real quota or upstream API failure occurs
