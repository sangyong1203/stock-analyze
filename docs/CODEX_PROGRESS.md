# CODEX PROGRESS

## Current phase

- Phase: news alert send policy hardening
- Task document: `docs/CODEX_TASK_2.13.md`
- Status: send candidate policy tightened, dry-run revalidated, no real send executed

## Completed major work

- Reviewed:
  - `docs/CODEX_TASK_2.13.md`
  - `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
  - `docs/MVP_DB_SCHEMA_v1.2.md`
- Confirmed the leakage point:
  - `is_alert_target = true` news could enter send planning even when `gpt_filter_result = failed`
  - unresolved GPT-filter state was therefore still reaching dry-run sendable output
- Applied minimal backend fix only for send policy:
  - `backend/app/domains/news/repository.py`
  - `backend/app/domains/news/service.py`
- Tightened send candidate policy to allow only:
  - `gpt_filter_result = important`
  - `gpt_filter_result = price_impact`
- Added defensive skip handling in send planning for non-sendable GPT filter states
- Restarted duplicated backend `uvicorn` processes and relaunched a single backend server on `127.0.0.1:8000`
- Revalidated news alert dry-run after restart:
  - before: `candidate_count = 3`, `sendable_count = 1`
  - after: `candidate_count = 2`, `sendable_count = 0`
- Reconfirmed `news_id = 3` remains visible in alert candidate review data but is no longer sendable because:
  - `gpt_filter_result = failed`
  - related stock links `0`
  - broad market/policy article
- Confirmed no real Gmail send endpoint was executed
- Added:
  - `docs/NEWS_ALERT_POLICY_FIX_REPORT.md`
  - `docs/CODEX_TASK_2.13_REPORT.md`

## Verification result

| Item | Result |
|---|---|
| `POST /api/news/alerts/send/dry-run` | 200 |
| `GET /api/news/alerts/candidates` | 200 |
| `GET /api/dashboard/summary` | 200 |
| `python -m compileall app` | passed |
| `npm run build` | passed |

## Current validated alert state

- news-alert dry-run candidate items: `2`
- news-alert dry-run sendable items: `0`
- skipped reason `already_sent = 2`
- news-alert history rows preserved: `2`
- current-turn real sends executed: `0`

## Confirmation-needed items

- Item: whether broad market news without stock links should remain in alert candidate review lists
- Reason: current task only tightened send policy, not alert target classification policy
- Recommendation: keep such items reviewable but not sendable unless a later rule is explicitly confirmed
- Current implementation status: send policy fixed, broader alert-target policy unchanged

## Next step suggestions

- If needed later, split “alert candidate review list” policy from “real send” policy more explicitly in the UI copy
- Keep real send limited to GPT-classified actionable items unless a wider market-alert policy is confirmed
