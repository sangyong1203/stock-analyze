# CODEX TASK 1.12 REPORT

## 1. 작업 개요

- 작업명: 가격 알림 조건 / Gmail 발송 연결 / Alerts 화면 정리
- 대상: `price_alerts`, `alert_settings`, `alert_histories`, `stocks`, `stock_prices`
- 범위 제한:
  - 새 기능 확장 없음
  - 새 테이블 없음
  - 새 마이그레이션 없음
  - 기존 1.11 작업 훼손 없음

## 2. 구현된 API

| API | 결과 |
|---|---|
| `GET /api/price-alerts` | 구현 |
| `POST /api/price-alerts` | 구현 |
| `GET /api/price-alerts/{alert_id}` | 구현 |
| `PATCH /api/price-alerts/{alert_id}` | 구현 |
| `DELETE /api/price-alerts/{alert_id}` | 구현 |
| `POST /api/price-alerts/evaluate/dry-run` | 구현 |
| `POST /api/price-alerts/evaluate` | 구현 |
| `GET /api/price-alerts/summary` | 구현 |
| `GET /api/price-alerts/histories` | 구현 |

## 3. 가격 알림 조건

- `TARGET_PRICE_ABOVE`
  - `current_price >= target_price`
- `TARGET_PRICE_BELOW`
  - `current_price <= target_price`
- `DROP_FROM_HIGH`
  - `current_price <= recent_high * (1 - threshold_percent / 100)`
- `RISE_FROM_LOW`
  - `current_price >= recent_low * (1 + threshold_percent / 100)`

구현 기준:

- 현재가는 `stocks.current_price` 우선 사용
- 최근 고가 / 저가는 `stock_prices.timeframe = "daily"` 기준 조회
- 기본 `lookback_days`는 60

## 4. 중복 발송 방지 방식

- 기준 키: `price_alert_id + stock_id + alert_type`
- 같은 날 이미 `sent` 이력이 있으면 `already_sent_today`로 skip
- 같은 날 `failed` 이력이 있으면 `force=true`가 아니면 skip
- 실제 evaluate는 skip도 `alert_histories`에 기록

## 5. Gmail 발송 연결 결과

- 기존 SMTP 설정 재사용
- 실제 검증:
  - `stock_id=2` 알림 1건 실제 발송 성공
  - 같은 알림 재실행 시 `already_sent_today`로 skip 확인

## 6. Frontend 연결 결과

- Alerts 화면을 가격 알림 관리 화면으로 교체
- 지원 항목:
  - 목록 조회
  - 생성 / 수정 / 삭제
  - 종목 원격 검색
  - 조건 선택
  - dry-run
  - 실제 발송
  - 발송 이력 조회
  - skip 사유 / 오류 표시

## 7. 테스트 결과

### CRUD

- 생성: 성공
- 조회: 성공
- 수정: 성공
- 삭제: 성공

### 조건 검증

- `TARGET_PRICE_ABOVE`: 성공
- `TARGET_PRICE_BELOW`: 성공
- `DROP_FROM_HIGH`: 성공
- `RISE_FROM_LOW`: 성공

### dry-run

- 평가 대상 4건
- 조건 충족 4건
- 발송 가능 4건

### 실제 발송

- sent: 1
- failed: 0

### duplicate skip

- 동일 알림 재실행 시 `already_sent_today` 확인

### summary / histories

검증 중간 결과:

- `total_count`: 4
- `enabled_count`: 4
- `triggered_count`: 1
- `sent_count`: 1
- `skipped_count`: 1

검증 후 정리 결과:

- 테스트용 `CODEX_TASK_1.12*` 알림 4건 삭제
- price alert history 0건 복원
- `/api/price-alerts/summary` 0 상태 복원

### compile / build / regression

- `python -m compileall backend/app`: 성공
- `npm run build`: 성공
- `/health`: 200
- `/api/auth/status`: 200
- `/api/prices/summary`: 200
- `/api/charts/stocks/2/ohlcv?limit=130`: 200
- `/api/portfolio/summary`: 200
- `/api/news/alerts/send/dry-run`: 200

## 8. 확인 필요 항목

- `lookback_days` 전용 컬럼이 없어 이번 작업에서는 `price_alerts.base_price`를 재사용
- 일부 종목명은 DB 인코딩이 이미 깨져 있어 알림 제목/본문에도 그대로 반영됨

## 9. 다음 단계 제안

- stocks / portfolio 화면에서 alerts 화면으로 바로 진입하는 버튼 추가
- 종목명 인코딩 정리 작업 분리
