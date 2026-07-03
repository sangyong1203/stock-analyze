# CODEX PROGRESS

## Current phase

- Phase: GPT filter failure handling policy cleanup
- Task document: `docs/CODEX_TASK_2.14.md`
- Status: failed filter item reprocess path restored, sendable block revalidated, no real Gmail send executed

## Completed major work

- Reviewed:
  - `docs/CODEX_TASK_2.14.md`
  - `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
  - `docs/MVP_DB_SCHEMA_v1.2.md`
- Confirmed current GPT state:
  - `summary_failed_count = 0`
  - `filter_failed_count = 1`
- Confirmed the failed filter news:
  - `news_id = 3`
  - `gpt_filter_result = failed`
  - failure reason contains OpenAI quota `429 insufficient_quota`
- Confirmed the policy gap:
  - failed filter items were visible in review
  - but existing `POST /api/news/gpt/filter/run` target selection only included `gpt_filter_result IS NULL`
  - therefore failed items were not re-entering the normal reprocess queue
- Applied minimal backend fix:
  - `backend/app/domains/news/repository.py`
  - filter target query now includes `gpt_filter_result = failed`
  - filter pending count now reflects retryable failed items
- Restarted backend server on `127.0.0.1:8000`
- Revalidated with live API:
  - filter dry-run target count changed from `16` to `17`
  - failed `news_id = 3` now appears in filter dry-run items with `status = failed`
- Reconfirmed failed filter items are still not sendable:
  - news alert dry-run `sendable_count = 0`
  - no real send executed
- Added:
  - `docs/GPT_FILTER_FAILURE_POLICY_REPORT.md`
  - `docs/CODEX_TASK_2.14_REPORT.md`

## Verification result

| Item | Result |
|---|---|
| `GET /api/news/gpt/targets` | 200 |
| `GET /api/news/gpt/review?gpt_filter_result=failed` | 200 |
| `POST /api/news/gpt/filter/run` dry-run | 200 |
| `POST /api/news/alerts/send/dry-run` | 200 |
| `python -m compileall app` | passed |
| `npm run build` | passed |

## Current validated GPT failure state

- failed filter rows: `1`
- failed filter review rows: `1`
- filter dry-run target count: `17`
- failed row included in reprocess dry-run: yes
- news alert dry-run sendable count: `0`

## Confirmation-needed items

- Item: whether a real GPT filter rerun should be attempted later after OpenAI quota recovery
- Reason: this task restored the queueing path only; actual retry execution was not forced because quota failure was already recorded
- Recommendation: rerun manually later through the existing GPT filter run API after quota/billing is restored
- Current implementation status: retry path restored, real retry not executed

## Next step suggestions

- Keep failed GPT filter rows for manual retry rather than deleting or manually rewriting them
- Use existing filter run API after quota recovery and then re-check alert candidate classification
