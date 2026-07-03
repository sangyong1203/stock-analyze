# DEVELOPMENT REPORT

## Work overview

- Latest completed scope: `docs/CODEX_TASK_2.13.md`
- Scope handled in this task: harden news alert send policy so failed or unresolved GPT-filter items do not remain sendable
- Constraint kept:
  - no real Gmail send
  - no real send endpoint execution
  - no news row deletion
  - no alert history deletion
  - no new table
  - no migration
  - minimal backend fix only

## Reference documents

- `docs/CODEX_TASK_2.13.md`
- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

## Completed work

- Reviewed current news alert send planning flow
- Confirmed policy leak:
  - `gpt_filter_result = failed` item could still reach sendable dry-run output
- Applied minimal fix so send candidates are limited to:
  - `important`
  - `price_impact`
- Added defensive skip guard in send planning for non-sendable GPT filter results
- Restarted duplicated backend `uvicorn` processes and relaunched a single backend server
- Re-ran dry-run verification after restart
- Reconfirmed that `news_id = 3` is still an alert review candidate but no longer a sendable item
- Verified no real Gmail send was executed
- Rechecked `/news`, `/dashboard`, `/settings` rendering state
- Updated task report documents

## Generated files

- `docs/NEWS_ALERT_POLICY_FIX_REPORT.md`
- `docs/CODEX_TASK_2.13_REPORT.md`

## Modified files

- `backend/app/domains/news/repository.py`
- `backend/app/domains/news/service.py`
- `docs/CODEX_PROGRESS.md`
- `docs/DEVELOPMENT_REPORT.md`

## Backend implementation result

- Send-candidate query now requires:
  - `News.is_alert_target = true`
  - `News.gpt_filter_result in ("important", "price_impact")`
- Send planning now defensively skips non-sendable GPT filter states even if candidate selection changes later
- Backend server was restarted after the code change

## Frontend implementation result

- No frontend code change
- `/news`, `/dashboard`, `/settings` routes rendered in the browser with current data after backend restart
- A stale browser console fetch error from prior `127.0.0.1:4173` preview context was observed, but current `127.0.0.1:5173` route rendering and API-backed page data were confirmed

## DB implementation result

- No schema change
- No new table
- No migration
- Existing news rows and alert histories preserved
- News alert history rows remain:
  - `2`
  - sent rows `2`

## Execution method

Main validation:

```text
POST /api/news/alerts/send/dry-run
GET /api/news/alerts/candidates
GET /api/dashboard/summary
python -m compileall app
npm run build
Browser check: /news, /dashboard, /settings
```

## Test result

- `POST /api/news/alerts/send/dry-run`: 200
  - before fix: `candidate_count = 3`, `sendable_count = 1`
  - after fix: `candidate_count = 2`, `sendable_count = 0`
  - `skipped_count = 2`
  - skipped reason `already_sent = 2`
- `GET /api/news/alerts/candidates`: 200
  - `news_id = 3` still visible in candidate review data
  - `gpt_filter_result = failed`
  - related stock links `0`
- `GET /api/dashboard/summary`: 200
  - `news_alert_summary.alert_target_count = 2`
  - `news_alert_summary.price_impact_count = 1`
- `python -m compileall app`: passed
- `npm run build`: passed
  - Vite chunk-size warning only
- Browser route check:
  - `/news`: rendered
  - `/dashboard`: rendered
  - `/settings`: rendered
- Real send endpoint execution in this task: none

## Incomplete items

- Broad market news without stock links still remains in alert candidate review data when already marked as alert target

## Confirmation-needed items

- If broad market policy news without linked stocks should also be excluded from alert candidate review lists, that should be handled as a separate policy change later
- This task only fixed real send eligibility, not alert target classification

## Next step suggestions

- Keep real send eligibility restricted to GPT-classified actionable news
- If needed later, define a separate cleanup policy for market-wide alert candidates with no linked stocks

## Final completion statement

CODEX_TASK_2.13 news alert send policy hardening completed.
Real Gmail send was not executed.
Check `DEVELOPMENT_REPORT.md`.
