# PRICE ALERT TEST CLEANUP REPORT

## 1. Work overview

- Task basis: `docs/CODEX_TASK_2.10.md`
- Goal: remove the two test price alerts while preserving the Gmail send verification histories and restore a clean registration state
- Constraint kept:
  - no real Gmail send
  - no real-send endpoint call
  - no alert-history deletion
  - no portfolio/trade/holdings change
  - no new table
  - no migration

## 2. Pre-cleanup state

- Registered test alerts: `2`
- Enabled alerts: `2`
- Pre-cleanup summary:
  - `total_count = 2`
  - `enabled_count = 2`
  - `sent_count = 1`
  - `skipped_count = 1`
- Pre-cleanup histories:
  - price alert history rows `2`
  - NAVER `sent`
  - Samsung SDI `skipped`

## 3. Deleted test price alerts

- Removed:
  - NAVER `035420` test alert
  - Samsung SDI `006400` test alert
- Deleted scope:
  - only price-alert rows
  - no alert-history deletion
  - no related portfolio/trade/holdings change

## 4. Post-cleanup state

- `/api/price-alerts`
  - row count `0`
- `/api/price-alerts/summary`
  - `total_count = 0`
  - `enabled_count = 0`
  - `disabled_count = 0`
  - `triggered_count = 0`
  - `sent_count = 1`
  - `failed_count = 0`
  - `skipped_count = 1`
  - `today_sent_count = 1`
  - `hourly_sent_count = 1`
- `/api/dashboard/summary.price_alert_summary`
  - `total_count = 0`
  - `enabled_count = 0`
  - `sent_count = 1`

## 5. alert_histories preservation check

- `/api/price-alerts/histories` remained at row count `2`
- Preserved rows:
  - NAVER history
    - status: `sent`
    - `price_alert_id = 1`
    - `stock_id = 17`
  - Samsung SDI history
    - status: `skipped`
    - `price_alert_id = 2`
    - `stock_id = 16`
    - error/skip: `condition_not_met`
- Conclusion:
  - send verification evidence remained intact after alert cleanup

## 6. Dry-run verification result

- Executed:
  - `POST /api/price-alerts/evaluate/dry-run`
  - body: `{"force": false}`
- Result:
  - `evaluated_count = 0`
  - `matched_count = 0`
  - `sendable_count = 0`
  - `sent_count = 0`
  - `failed_count = 0`
  - `skipped_count = 0`
- Conclusion:
  - no active test price alert remains
  - registration state is restored to clean baseline

## 7. Browser verification result

- Browser `/alerts`:
  - shows `전체 알림 0`
  - shows `활성 알림 0`
  - shows `오늘 발송 1`
  - alert list area shows no data
  - sent/skipped history rows still visible
- Browser `/dashboard`:
  - shows `가격 알림 활성 0`
  - shows `가격 알림 발송 1`
  - recent alert history still includes NAVER `sent` and Samsung SDI `skipped`
- Browser console note:
  - no current `5173` error log found

## 8. Next step

- Register only real user alerts from the cleaned state
- Keep history retention unchanged unless a later explicit task requests cleanup policy changes
