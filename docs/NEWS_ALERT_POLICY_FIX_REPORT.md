# NEWS ALERT POLICY FIX REPORT

## Scope

- Task: `docs/CODEX_TASK_2.13.md`
- Goal: prevent failed or unresolved GPT-filter news from remaining sendable in news alert dry-run/send planning

## Problem confirmed

- `news_id = 3` had:
  - `is_alert_target = true`
  - `gpt_filter_result = failed`
  - related stock links `0`
- Despite that, it still appeared in dry-run sendable output before the fix

## Applied fix

- Restricted send candidate query to:
  - `gpt_filter_result = important`
  - `gpt_filter_result = price_impact`
- Added defensive skip handling in send planning for non-sendable GPT filter states

## Verification

- Dry-run before fix:
  - `candidate_count = 3`
  - `sendable_count = 1`
- Dry-run after fix:
  - `candidate_count = 2`
  - `sendable_count = 0`
- Existing sent history rows remained unchanged:
  - `2`

## Notes

- No real Gmail send executed
- No schema change
- No migration
- `news_id = 3` remains reviewable in alert candidate data, but is no longer sendable
