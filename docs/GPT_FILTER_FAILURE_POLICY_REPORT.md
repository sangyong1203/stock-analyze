# GPT FILTER FAILURE POLICY REPORT

## Scope

- Task: `docs/CODEX_TASK_2.14.md`
- Goal: clarify handling of GPT filter failures caused by OpenAI quota issues and restore normal retry visibility through the existing API path

## Confirmed live state

- Failed GPT filter rows: `1`
- Failed row:
  - `news_id = 3`
  - `gpt_filter_result = failed`
  - failure reason: OpenAI quota `429 insufficient_quota`

## Problem

- Failed filter rows remained visible in review data
- But the existing filter run target query only selected `gpt_filter_result IS NULL`
- Therefore failed rows could not re-enter the standard filter run queue through the existing dry-run/manual path

## Applied policy fix

- Treat failed GPT filter rows as retryable filter targets
- Preserve the failed row and failure reason
- Do not delete the row
- Do not mark it sendable
- Retry later through the existing GPT filter run API after quota recovery

## Verification

- Filter dry-run target count changed:
  - before: `16`
  - after: `17`
- Failed `news_id = 3` now appears in dry-run retry target items
- News alert dry-run still reports:
  - `sendable_count = 0`

## Notes

- No real Gmail send executed
- No real GPT retry executed
- No schema change
- No migration
