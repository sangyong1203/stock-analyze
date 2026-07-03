# PRICE ALERT TEST REGISTRATION REPORT

## 1. 작업 개요

- 작업 기준: `docs/CODEX_TASK_2.8.md`
- 목적: 테스트용 가격 알림 2건을 등록하고, 실제 Gmail 발송 없이 dry-run 결과를 확인
- 결과: 테스트 알림 2건 등록 완료, NAVER는 matched, 삼성SDI는 not matched, 실제 발송 없음

## 2. 등록된 테스트 알림

사전 정리:

- 기존 price alert 1건이 task baseline과 충돌해 먼저 삭제
- 정리 후 기준 상태:
  - `price_alerts row count = 0`
  - `price alert histories row count = 0`

등록한 테스트 알림:

| stock_name | stock_code | alert_name | alert_type | target_price | enabled | memo |
|---|---|---|---|---:|---|---|
| NAVER | `035420` | `TEST_NAVER_즉시매칭_TEST` | `TARGET_PRICE_ABOVE` | 250000 | true | dry-run 매칭 확인용 테스트 알림 |
| 삼성SDI | `006400` | `TEST_삼성SDI_미매칭_TEST` | `TARGET_PRICE_ABOVE` | 400000 | true | dry-run 미매칭 확인용 테스트 알림 |

등록 후 상태:

- `/api/price-alerts` row count: `2`
- `/api/price-alerts/summary.total_count = 2`
- `/api/price-alerts/summary.enabled_count = 2`

## 3. dry-run 검증 결과

호출 API:

- `/api/price-alerts/evaluate/dry-run`

응답 핵심값:

- `evaluated_count = 2`
- `matched_count = 1`
- `sendable_count = 1`
- `sent_count = 0`
- `failed_count = 0`
- `skipped_count = 1`

개별 결과:

- NAVER
  - current price `253000`
  - target price `250000`
  - result: matched
  - status: `would_send`
- 삼성SDI
  - current price `185300`
  - target price `400000`
  - result: not matched
  - status: `skipped`
  - skip reason: `condition_not_met`

## 4. 브라우저 확인 결과

검증 라우트:

- `/alerts`
- `/dashboard`

확인 결과:

- `/alerts`
  - 총 알림 `2`
  - 활성 알림 `2`
  - 두 테스트 알림이 목록에 표시
  - dry-run 버튼 표시
  - 실제 발송 버튼은 보이지만 클릭하지 않음
- `/dashboard`
  - `가격 알림 활성 = 2`
  - `가격 알림 발송 = 0`

## 5. 실제 발송 미실행 확인

- `/api/price-alerts/evaluate` 실제 발송 경로는 호출하지 않음
- `/api/price-alerts/histories` row count: `0`
- `sent_count = 0`
- `failed_count = 0`
- 실제 Gmail 발송 없음

## 6. 다음 단계

- 테스트 목적이 끝나면 이 2건의 테스트 알림을 정리할지 결정
- 실제 알림을 만들 때는 테스트 이름 대신 사용자 조건 기반 이름과 목표가 사용
- 실제 발송 검증은 별도 명시 작업으로 분리하는 것이 안전

## 7. 보류 / 확인 필요 항목

- 현재 등록된 2건은 실사용 알림이 아니라 테스트 알림이다
- 후속 작업에서 유지 또는 삭제 여부를 결정해야 한다
