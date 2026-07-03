# PRICE ALERT READY REPORT

## 1. 작업 개요

- 작업 기준: `docs/CODEX_TASK_2.7.md`
- 목적: 실사용 가격 알림 기능이 현재 포트폴리오 기준으로 준비 상태인지 확인하고, 실제 발송 없이 dry-run과 입력 가이드를 정리
- 결과: 알림은 아직 등록되지 않았고, dry-run 0건 응답과 UI 상태를 확인했으며 입력 가이드를 작성했다

## 2. 현재 알림 상태

API/DB 확인 결과:

- `price_alerts` row count: `0`
- price alert history row count: `0`
- `alert_settings` row exists: yes
- `alert_settings.enabled = true`
- `alert_settings.price_alert_enabled = true`
- `alert_settings.send_email = true`

요약 API:

- `/api/price-alerts/summary`
  - `total_count = 0`
  - `enabled_count = 0`
  - `disabled_count = 0`
  - `triggered_count = 0`
  - `sent_count = 0`
  - `failed_count = 0`
  - `skipped_count = 0`
  - `today_sent_count = 0`
  - `hourly_sent_count = 0`

## 3. dry-run 검증 결과

호출 API:

- `/api/price-alerts/evaluate/dry-run`

요청:

```json
{
  "force": false
}
```

응답 결과:

- `evaluated_count = 0`
- `matched_count = 0`
- `sendable_count = 0`
- `sent_count = 0`
- `failed_count = 0`
- `skipped_count = 0`
- `items = []`

검증 결론:

- alert row가 없을 때 dry-run은 정상적으로 0건 응답
- 실제 Gmail 발송 없음
- price alert history 추가 없음

## 4. 브라우저 확인 결과

검증 라우트:

- `/alerts`
- `/dashboard`

확인 결과:

- `/alerts`
  - 총 알림 `0`
  - 활성 알림 `0`
  - 오늘 발송 `0`
  - 최근 1시간 발송 `0`
  - 가격 알림 추가 폼 표시
  - dry-run 버튼 표시
  - 실제 발송 버튼은 보이지만 클릭하지 않음
- `/dashboard`
  - 가격 알림 활성 `0`
  - 가격 알림 발송 `0`
  - 포트폴리오 수치는 기존 검증값 유지

## 5. PRICE_ALERT_INPUT_GUIDE 작성 결과

작성 문서:

- `docs/PRICE_ALERT_INPUT_GUIDE.md`

포함 내용:

- 현재 보유 종목
- 지원 alert type 설명
- CSV 입력 형식
- 예시
- dry-run 확인 순서
- 실제 Gmail 발송 전 체크리스트
- 중복 발송 방지 기준
- 주의사항

## 6. 실제 발송 전 체크리스트

- 사용자가 목표가/기준값을 명시적으로 제공했는가
- 등록하려는 종목 코드가 정확한가
- 먼저 dry-run 결과를 확인했는가
- 실제 발송이 정말 필요한지 사용자가 다시 확인했는가
- Gmail 설정과 수신 이메일이 준비되어 있는가
- 일일/시간당 발송 한도를 넘지 않는가

## 7. 보류 / 확인 필요 항목

- 이번 작업에서는 사용자가 명시한 알림 조건이 없어서 실제 price alert를 생성하지 않았다
- 실제 알림 생성 작업은 `PRICE_ALERT_INPUT_GUIDE.md` 형식으로 사용자 조건이 주어진 뒤 진행하는 것이 맞다
