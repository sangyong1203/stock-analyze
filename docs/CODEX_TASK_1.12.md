# CODEX_TASK_1.12

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

거래 기록 / 보유 종목 / 손익 계산 구조는 완료됐습니다.

이번 작업은 **가격 알림 조건 / 목표가 알림 / Gmail 발송 연결**입니다.

## 작업 목표

1. `price_alerts` CRUD를 구현한다.
2. 현재가 기준 목표가 도달 알림을 구현한다.
3. 고점 대비 하락률 알림을 구현한다.
4. 저점 대비 상승률 알림을 구현한다.
5. 가격 알림 후보 평가 dry-run을 구현한다.
6. 실제 가격 알림 발송을 Gmail 알림 구조와 연결한다.
7. 중복 발송 방지와 `alert_histories` 기록을 구현한다.
8. 새 DB 테이블과 마이그레이션은 만들지 않는다.

## 작업 전 확인

직전 `DEVELOPMENT_REPORT.md`의 완료/미완료/확인 필요 항목만 확인한다.

이번 작업에서 필요한 기존 구조만 확인한다.

```text id="3ev2kz"
price_alerts
alert_settings
alert_histories
stocks
stock_prices
holdings
backend/app/domains/news/
backend/app/external/gmail/
frontend/src/pages/main/alerts/
```

주의:

```text id="qjmar2"
- 기준 문서를 반복해서 다시 읽지 않는다.
- 새 DB 테이블을 만들지 않는다.
- 새 마이그레이션을 만들지 않는다.
- 기존 price_alerts 필드 안에서 구현한다.
- 기존 필드로 표현하기 어려운 조건은 임의 추가하지 말고 확인 필요 항목에 기록한다.
```

## Backend 작업 항목

대상 후보:

```text id="7f8mwl"
backend/app/domains/alerts/
backend/app/domains/price_alerts/
backend/app/domains/news/
backend/app/external/gmail/
backend/app/main.py
```

필요한 API를 구현한다.

## 1. 가격 알림 CRUD

권장 API:

```text id="s4n1j7"
GET    /api/price-alerts
POST   /api/price-alerts
GET    /api/price-alerts/{alert_id}
PATCH  /api/price-alerts/{alert_id}
DELETE /api/price-alerts/{alert_id}
```

필수 개념:

```text id="66f7pz"
stock_id
alert_type
target_price
threshold_percent
lookback_days
is_enabled
memo
```

기존 모델 필드명이 다르면 기존 필드명에 맞춘다.

## 2. 지원할 알림 조건

기본 지원 조건:

```text id="h68ybp"
TARGET_PRICE_ABOVE
TARGET_PRICE_BELOW
DROP_FROM_HIGH
RISE_FROM_LOW
```

계산 기준:

```text id="7votwb"
TARGET_PRICE_ABOVE:
current_price >= target_price

TARGET_PRICE_BELOW:
current_price <= target_price

DROP_FROM_HIGH:
current_price <= recent_high * (1 - threshold_percent / 100)

RISE_FROM_LOW:
current_price >= recent_low * (1 + threshold_percent / 100)
```

`recent_high`, `recent_low`는 `stock_prices`에서 `lookback_days` 기간 기준으로 계산한다.

기본값:

```text id="zqun44"
lookback_days = 60
```

현재가가 없거나 가격 데이터가 부족하면 안전하게 skip 처리한다.

## 3. 가격 알림 평가 API

권장 API:

```text id="led1n7"
POST /api/price-alerts/evaluate/dry-run
POST /api/price-alerts/evaluate
GET  /api/price-alerts/summary
```

dry-run:

```text id="emj7eo"
- 실제 발송하지 않는다.
- 발송 대상 후보만 계산한다.
- 조건 충족 여부와 skip reason을 반환한다.
```

실제 evaluate:

```text id="40i4nd"
- 조건 충족 알림을 Gmail로 발송한다.
- alert_histories에 sent / failed / skipped 기록을 남긴다.
- 기존 Gmail SMTP client를 재사용한다.
```

## 4. 중복 발송 방지

중복 기준:

```text id="9yqol5"
price_alert_id + stock_id + alert_type
```

같은 가격 알림은 같은 날 중복 발송하지 않는다.

권장:

```text id="pmcg8h"
오늘 이미 sent 이력이 있으면 skip
failed 이력은 force=true일 때만 재시도
```

`alert_histories.price_alert_id`가 있으면 사용한다.
기존 필드가 부족하면 확인 필요 항목에 기록한다.

## 5. 발송 제한

기존 `alert_settings`를 사용한다.

```text id="heqgti"
enabled
price_alert_enabled
send_email
max_daily_alerts
max_hourly_alerts
```

뉴스 알림과 동일하게 일별/시간별 제한을 적용한다.

## Frontend 작업 항목

대상:

```text id="nqvrdc"
frontend/src/pages/main/alerts/
frontend/src/pages/main/stocks/
frontend/src/pages/main/portfolio/
```

구현 항목:

1. 가격 알림 목록 표시
2. 가격 알림 생성/수정/삭제 폼
3. 종목 검색 후 알림 생성
4. 알림 조건 선택

```text id="qy9jz9"
목표가 이상
목표가 이하
고점 대비 하락률
저점 대비 상승률
```

5. dry-run 버튼
6. 실제 발송 버튼
7. 발송 이력 표시
8. 조건 충족/미충족/스킵 사유 표시
9. 로딩/오류/빈 데이터 상태 처리

가능하면 종목 화면 또는 보유 종목 화면에서 “가격 알림 추가” 진입 버튼도 추가한다.

## 검증 항목

Backend:

```text id="b5ir6c"
- python -m compileall app 성공
- price_alert 생성/조회/수정/삭제 성공
- TARGET_PRICE_ABOVE 조건 충족 검증
- TARGET_PRICE_BELOW 조건 충족 검증
- DROP_FROM_HIGH 조건 충족 검증
- RISE_FROM_LOW 조건 충족 검증
- dry-run 결과 확인
- 실제 발송 limit 1 또는 테스트 알림 1건 확인
- alert_histories sent 기록 확인
- 같은 알림 중복 발송 skip 확인
- /api/price-alerts/summary 확인
```

Frontend:

```text id="jp7s2k"
- 알림 관리 화면 표시
- 가격 알림 생성 폼 동작
- dry-run 결과 표시
- 발송 이력 표시
- npm run build 성공
```

Regression:

```text id="wv7e7z"
/health
/api/auth/status
/api/prices/summary
/api/charts/stocks/2/ohlcv?limit=130
/api/portfolio/summary
/api/news/alerts/send/dry-run
```

## 문서 갱신

작업 완료 후 다음 문서를 짧게 갱신한다.

```text id="h46nv9"
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 새 문서를 작성한다.

```text id="fgaff2"
docs/PRICE_ALERT_REPORT.md
```

포함 내용:

```markdown id="w6a7no"
# PRICE ALERT REPORT

## 1. 작업 개요

## 2. 구현한 API

## 3. 가격 알림 조건

## 4. 중복 발송 방지 방식

## 5. Gmail 발송 연결 결과

## 6. Frontend 연결 결과

## 7. 테스트 결과

## 8. 확인 필요 항목

## 9. 다음 단계 제안
```

## 완료 조건

```text id="um1kzv"
- price_alerts CRUD 구현
- 목표가 이상/이하 조건 구현
- 고점 대비 하락률 조건 구현
- 저점 대비 상승률 조건 구현
- 가격 알림 dry-run 구현
- 가격 알림 실제 발송 구현
- alert_histories 기록 구현
- 중복 발송 방지 구현
- 알림 관리 화면 연결
- Backend compile 성공
- Frontend build 성공
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 다음과 같이 보고하세요.

```text id="r1lyhk"
가격 알림 조건과 발송 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
