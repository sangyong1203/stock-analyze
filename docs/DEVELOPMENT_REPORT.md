# DEVELOPMENT REPORT

## Work overview

- Latest completed scope: `docs/CODEX_TASK_2.14.md`
- Scope handled in this task: organize GPT filter failure handling for OpenAI quota failures and restore normal dry-run retry visibility for failed items
- Constraint kept:
  - no real Gmail send
  - no news row deletion
  - no alert history deletion
  - no new table
  - no migration
  - minimal backend fix only
  - no API key exposure

## Reference documents

- `docs/CODEX_TASK_2.14.md`
- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

## Completed work

- Reviewed GPT summary/filter current state
- Confirmed one failed GPT filter item remains in live DB:
  - `news_id = 3`
  - failure reason includes OpenAI quota `429 insufficient_quota`
- Confirmed the existing failure-management gap:
  - failed filter items were not included in the normal filter run target query
- Applied minimal fix so failed filter rows re-enter the existing filter reprocess queue
- Restarted backend server
- Re-ran GPT filter dry-run and confirmed failed row is now included in the retryable target list
- Reconfirmed failed filter item does not become a sendable news alert candidate
- Updated task report documents

## Generated files

- `docs/GPT_FILTER_FAILURE_POLICY_REPORT.md`
- `docs/CODEX_TASK_2.14_REPORT.md`

## Modified files

- `backend/app/domains/news/repository.py`
- `docs/CODEX_PROGRESS.md`
- `docs/DEVELOPMENT_REPORT.md`

## Backend implementation result

- `list_filter_targets(...)` now includes:
  - `gpt_filter_result IS NULL`
  - `gpt_filter_result = failed`
- `gpt_targets_counts(...)` pending-filter count now uses the same retryable condition
- This keeps failure handling aligned with the existing summary retry pattern
- No router change
- No schema change

## Frontend implementation result

- No frontend code change
- Frontend production build passed

## DB implementation result

- No schema change
- No new table
- No migration
- Existing failed GPT filter row preserved for retry
- Existing alert histories preserved

## Execution method

Main validation:

```text
GET /api/news/gpt/targets
GET /api/news/gpt/review?gpt_filter_result=failed
POST /api/news/gpt/filter/run
POST /api/news/alerts/send/dry-run
python -m compileall app
npm run build
```

## Test result

- `GET /api/news/gpt/targets`: 200
  - before fix:
    - `filter_pending_count = 16`
    - `filter_failed_count = 1`
  - after fix:
    - `filter_pending_count = 17`
    - `filter_failed_count = 1`
- `GET /api/news/gpt/review?gpt_filter_result=failed`: 200
  - failed row count `1`
  - failure reason confirmed as OpenAI quota `429 insufficient_quota`
- `POST /api/news/gpt/filter/run` dry-run: 200
  - before fix: `target_count = 16`
  - after fix: `target_count = 17`
  - `news_id = 3` included with `status = failed`
- `POST /api/news/alerts/send/dry-run`: 200
  - `sendable_count = 0`
  - failed filter item did not become sendable
- `python -m compileall app`: passed
- `npm run build`: passed
  - Vite chunk-size warning only
- Real Gmail send in this task: none
- Real GPT rerun in this task: none

## Incomplete items

- The failed GPT filter row remains failed until a real retry is executed after quota recovery

## Confirmation-needed items

- If the user wants automatic retry scheduling for quota failures later, that would be a separate scope
- This task only restored retry visibility in the existing manual/API path

## Next step suggestions

- After OpenAI quota recovery, run the existing GPT filter API again and verify `news_id = 3` leaves failed state
- Recheck alert candidate review classification after that retry

## Final completion statement

CODEX_TASK_2.14 GPT filter failure handling policy cleanup completed.
Real Gmail send was not executed.
Check `DEVELOPMENT_REPORT.md`.
