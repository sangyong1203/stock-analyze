# PRICE ALERT GMAIL SEND TEST REPORT

## 1. Work overview

- Task basis: `docs/CODEX_TASK_2.9.md`
- Goal: execute the real Gmail send path exactly once for the matched NAVER test alert, confirm Samsung SDI is not sent, and verify history and duplicate-send prevention
- Constraint kept:
  - no `force=true`
  - no repeated real-send call
  - no portfolio/trade/holdings change
  - no new table
  - no migration

## 2. Pre-send alert state

- Registered test alerts: `2`
- Enabled alerts: `2`
- Price alert histories before send: `0`
- Pre-send dry-run baseline:
  - `evaluated_count = 2`
  - `matched_count = 1`
  - `sendable_count = 1`
  - NAVER: `would_send`
  - Samsung SDI: `skipped / condition_not_met`

## 3. Gmail configuration check result

- Checked only configured or missing status, without exposing values
- Confirmed configured:
  - `GMAIL_SMTP_HOST`
  - `GMAIL_SMTP_PORT`
  - `GMAIL_SMTP_USERNAME`
  - `GMAIL_SMTP_APP_PASSWORD`
  - `ALERT_RECIPIENT_EMAIL`

## 4. Real send execution result

- Executed endpoint once:
  - `POST /api/price-alerts/evaluate`
  - body: `{"force": false}`
- Response summary:
  - `evaluated_count = 2`
  - `matched_count = 1`
  - `sendable_count = 1`
  - `sent_count = 1`
  - `failed_count = 0`
  - `skipped_count = 1`
- Per-alert result:
  - NAVER `035420`
    - matched: `true`
    - status: `sent`
    - subject: `[Price Alert] NAVER TARGET_PRICE_ABOVE`
  - Samsung SDI `006400`
    - matched: `false`
    - status: `skipped`
    - skip reason: `condition_not_met`

## 5. alert_histories verification result

- `/api/price-alerts/histories` after send returned two price-alert rows:
  - NAVER history
    - status: `sent`
    - `price_alert_id = 1`
    - `stock_id = 17`
  - Samsung SDI history
    - status: `skipped`
    - `price_alert_id = 2`
    - `stock_id = 16`
    - error/skip: `condition_not_met`
- `/api/price-alerts/summary` after send:
  - `sent_count = 1`
  - `failed_count = 0`
  - `skipped_count = 1`
  - `today_sent_count = 1`
  - `hourly_sent_count = 1`
- `/api/dashboard/summary.price_alert_summary` after send:
  - `total_count = 2`
  - `enabled_count = 2`
  - `sent_count = 1`
  - `today_sent_count = 1`

## 6. Dashboard / alerts screen verification result

- Browser `/dashboard`:
  - shows `가격 알림 활성 2`
  - shows `가격 알림 발송 1`
  - recent alert history includes:
    - Samsung SDI `skipped`
    - NAVER `sent`
- Browser `/alerts`:
  - shows `전체 알림 2`
  - shows `활성 알림 2`
  - shows `오늘 발송 1`
  - shows both test alerts in the list
  - shows one `sent` history for NAVER
  - shows one `skipped` history for Samsung SDI
- Browser console note:
  - no current `5173` error log found
  - one stale previous-session `4173` `Failed to fetch` log remains in the browser log history

## 7. Duplicate-send prevention check

- No second real-send call was executed
- Validation method:
  - confirmed same-day `sent` history for NAVER exists
  - executed only dry-run after the real send
- Dry-run after send result:
  - `evaluated_count = 2`
  - `matched_count = 1`
  - `sendable_count = 0`
  - `sent_count = 0`
  - `skipped_count = 2`
  - skipped reasons:
    - `already_sent_today = 1`
    - `condition_not_met = 1`
- Conclusion:
  - NAVER duplicate send is blocked for today
  - Samsung SDI remains correctly non-sendable

## 8. Pending / confirmation-needed items

- The two alerts currently stored are test alerts and remain in the database after this verification
- Cleanup or replacement of those alerts should be handled in a separate explicit task
