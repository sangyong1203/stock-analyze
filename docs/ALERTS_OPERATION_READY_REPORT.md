# ALERTS OPERATION READY REPORT

## 1. Work overview

- Task basis: `docs/CODEX_TASK_2.11.md`
- Goal: verify operation readiness for both price alerts and news alerts without executing real Gmail send
- Constraint kept:
  - no real Gmail send
  - no real-send endpoint call
  - no new alert registration
  - no new table
  - no migration

## 2. Price-alert state

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
- `/api/price-alerts/histories`
  - row count `2`
  - NAVER `sent`
  - Samsung SDI `skipped`
- Conclusion:
  - active price alerts are currently empty
  - prior verification history remains preserved

## 3. Price-alert dry-run result

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
  - no current price-alert candidate exists
  - dry-run completed normally without creating send history

## 4. News-alert state

- `/api/news/summary`
  - `total_news_count = 18`
  - `linked_stock_news_count = 8`
  - `gpt_summary_target_count = 2`
  - `alert_target_count = 2`
  - `avg_importance_score = 1.17`
- `/api/news/gpt/targets`
  - `summary_pending_count = 0`
  - `summary_done_count = 2`
  - `summary_failed_count = 0`
  - `filter_pending_count = 16`
  - `filter_done_count = 1`
  - `filter_failed_count = 1`
- `/api/news/gpt/status`
  - `gpt_summary_done_count = 2`
  - `gpt_filter_done_count = 1`
  - `price_impact_count = 1`
- `/api/news/alerts/summary`
  - `alert_target_count = 2`
  - `important_count = 0`
  - `price_impact_count = 1`
  - `high_importance_count = 1`
- `/api/news/alerts/histories`
  - row count `2`
  - both existing rows remain `sent`

## 5. News-alert dry-run result

- Executed:
  - `POST /api/news/alerts/send/dry-run`
  - body: `{"limit": 20, "force": false}`
- Result:
  - `candidate_count = 3`
  - `sendable_count = 1`
  - `sent_count = 0`
  - `failed_count = 0`
  - `skipped_count = 2`
  - skipped reason:
    - `already_sent = 2`
- Dry-run sendable item:
  - `news_id = 3`
  - `stock_id = null`
  - recipient present
  - status `would_send`
- Conclusion:
  - one news candidate is currently sendable
  - two candidates are blocked by duplicate-send protection
  - no new history row was created during dry-run

## 6. Screen verification result

- Browser `/alerts`
  - shows `전체 알림 0`
  - shows `활성 알림 0`
  - shows `오늘 발송 1`
  - current alert list is empty
  - preserved price-alert history rows remain visible
- Browser `/dashboard`
  - shows `가격 알림 활성 0`
  - shows `가격 알림 발송 1`
  - shows `뉴스 알림 후보 2`
- Browser `/news`
  - shows `전체 뉴스 18`
  - shows `요약 대상 2`
  - shows `알림 후보 2`
  - news rows and recent collection job summary are visible
- Browser `/settings`
  - alert and job-related settings are visible
- Browser console note:
  - no current `5173` error log found

## 7. Real send not executed check

- No `POST /api/price-alerts/evaluate` call was executed
- No `POST /api/news/alerts/send` call was executed
- Price-alert history count remained `2`
- News-alert history count remained `2`
- This task only verified readiness via dry-run and UI checks

## 8. Pending / next step

- One news-alert dry-run sendable item still exists and should be reviewed before any actual send
- Price-alert registration remains empty and ready for future user-provided real conditions
- Any real-send validation should be handled in a separate explicit task
