# CODEX PROGRESS

## Current phase

- Phase: multiple price-alert condition registration and dry-run verification
- Task document: `docs/CODEX_TASK_2.17.md`
- Status: seven target-below alerts registered, duplicate-free creation confirmed, dry-run verified, no real Gmail send executed

## Completed major work

- Reviewed:
  - `docs/CODEX_TASK_2.17.md`
  - `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
  - `docs/MVP_DB_SCHEMA_v1.2.md`
- Confirmed current price-alert list before work:
  - existing alert rows `0`
- Resolved stock mappings for requested targets:
  - NAVER `035420` -> stock id `17`
  - LG에너지솔루션 `373220` -> stock id `27`
  - 현대모비스 `012330` -> stock id `14`
  - LG `003550` -> stock id `47`
  - 현대차 `005380` -> stock id `6`
  - LG전자 `066570` -> stock id `21`
  - 삼성SDI `006400` -> stock id `16`
- Created 7 `TARGET_PRICE_BELOW` alerts with requested target prices
- Confirmed duplicate-creation avoidance was satisfied because the list was empty before registration
- Verified final price-alert summary:
  - `total_count = 7`
  - `enabled_count = 7`
- Executed dry-run only:
  - `evaluated_count = 7`
  - `matched_count = 6`
  - `sendable_count = 6`
  - `skipped_count = 1`
  - skipped reason `condition_not_met = 1`
- Confirmed the one non-matching alert:
  - NAVER `253000 > 190000`
- Confirmed six alerts would currently send because current price is already below target:
  - LG에너지솔루션
  - 현대모비스
  - LG
  - 현대차
  - LG전자
  - 삼성SDI
- Added:
  - `docs/CODEX_TASK_2.17_REPORT.md`

## Verification result

| Item | Result |
|---|---|
| `GET /api/price-alerts` before registration | 200 |
| `POST /api/price-alerts` x7 | 201 |
| `GET /api/price-alerts/summary` | 200 |
| `POST /api/price-alerts/evaluate/dry-run` | 200 |

## Current validated alert state

- total alert rows: `7`
- enabled alert rows: `7`
- dry-run evaluated count: `7`
- dry-run sendable count: `6`
- dry-run skipped reason:
  - `condition_not_met = 1`
- real Gmail sends executed in this task: `0`

## Confirmation-needed items

- Item: most newly registered thresholds are already above the current live price, so they immediately become sendable in dry-run
- Reason: this follows the requested registration values and current market data
- Recommendation: keep as-is unless the target prices should be adjusted to future entry levels
- Current implementation status: registration complete, dry-run only

## Next step suggestions

- If needed later, narrow target prices so only intended near-entry alerts become sendable
- Keep using dry-run first before any real alert evaluation/send
