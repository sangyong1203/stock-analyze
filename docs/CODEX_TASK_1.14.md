# CODEX_TASK_1.14

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

CODEX_TASK_1.13 거래-뉴스 연결 / 메모 / 태그 구조는 완료됐습니다.

이번 작업은 **대시보드 / 투자 리포트 화면 구현**입니다.

## 작업 목표

1. 투자 현황을 한 화면에서 볼 수 있는 대시보드를 구현한다.
2. 포트폴리오 요약, 보유 종목, 최근 거래, 최근 뉴스, 알림 상태를 연결한다.
3. 기존 API와 기존 DB 테이블을 최대한 재사용한다.
4. 필요한 경우 최소 범위의 dashboard summary API만 추가한다.
5. 새 DB 테이블과 마이그레이션은 만들지 않는다.

## 작업 전 확인

직전 `DEVELOPMENT_REPORT.md`의 완료/미완료/확인 필요 항목만 확인한다.

이번 작업에서 필요한 기존 구조만 확인한다.

```text
portfolio
holdings
trades
stocks
stock_prices
news
price_alerts
alert_histories
memos
tags
```

주의:

```text
- 기준 문서를 반복해서 다시 읽지 않는다.
- 새 DB 테이블을 만들지 않는다.
- 새 마이그레이션을 만들지 않는다.
- 기존 API를 우선 재사용한다.
- 부족한 경우에만 dashboard 전용 조회 API를 최소로 추가한다.
```

## Backend 작업 항목

대상 후보:

```text
backend/app/domains/dashboard/
backend/app/domains/portfolio/
backend/app/domains/holdings/
backend/app/domains/trades/
backend/app/domains/news/
backend/app/main.py
```

권장 API:

```text
GET /api/dashboard/summary
```

응답에 포함할 항목:

```text
portfolio_summary
holding_summary
top_holdings
recent_trades
recent_news
recent_alert_histories
price_alert_summary
news_alert_summary
memo_summary
```

### 1. 포트폴리오 요약

기존 `/api/portfolio/summary` 계산을 재사용한다.

포함 항목:

```text
total_cash
total_market_value
total_unrealized_profit_loss
total_unrealized_profit_loss_rate
realized_profit_loss
total_asset_value
holding_count
today_change_amount
today_change_rate
```

### 2. 보유 종목 요약

포함 항목:

```text
top holdings by market_value
top gainers by profit_rate
top losers by profit_rate
```

기본 limit:

```text
5
```

### 3. 최근 거래

포함 항목:

```text
recent_trades limit 5
trade_type
stock_name
quantity
price
trade_date
memo
```

### 4. 최근 뉴스

포함 항목:

```text
recent_news limit 5
title
source
published_at
importance_score
gpt_summary_status
is_alert_target
```

### 5. 알림 요약

포함 항목:

```text
price_alert_summary
news_alert_summary
recent_alert_histories limit 5
```

기존 API가 있으면 재사용하고, 없으면 dashboard service에서 조회한다.

### 6. 메모/태그 요약

가능한 범위에서 구현한다.

```text
recent_memos limit 5
top_tags limit 10
```

복잡하면 recent_memos만 구현하고 top_tags는 확인 필요 항목에 기록한다.

## Frontend 작업 항목

대상:

```text
frontend/src/pages/main/dashboard/
```

대시보드 화면을 실제 API와 연결한다.

구성:

```text
1. 상단 KPI 카드
2. 포트폴리오 요약 카드
3. 보유 종목 TOP 5
4. 평가손익 TOP / 손실 TOP
5. 최근 거래
6. 최근 뉴스
7. 최근 알림 이력
8. 최근 메모
```

UI 기준:

```text
- MVP 수준으로 간결하게 구현한다.
- 과도한 차트는 넣지 않는다.
- 필요한 경우 간단한 bar/list 중심으로 구성한다.
- 빈 데이터, 로딩, 오류 상태를 처리한다.
```

가능하면 아래 빠른 이동 버튼을 추가한다.

```text
- 거래 기록으로 이동
- 포트폴리오로 이동
- 뉴스로 이동
- 알림으로 이동
- 차트로 이동
```

## 검증 항목

Backend:

```text
- python -m compileall app 성공
- /api/dashboard/summary 200
- portfolio_summary 포함 확인
- top_holdings 포함 확인
- recent_trades 포함 확인
- recent_news 포함 확인
- recent_alert_histories 포함 확인
```

Frontend:

```text
- 대시보드 화면 표시
- KPI 카드 표시
- 최근 거래 표시
- 최근 뉴스 표시
- 최근 알림 표시
- 빈 데이터 상태 표시
- npm run build 성공
```

Regression:

```text
/health
/api/auth/status
/api/prices/summary
/api/portfolio/summary
/api/price-alerts/summary
/api/news/alerts/send/dry-run
```

## 문서 갱신

작업 완료 후 다음 문서를 짧게 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 새 문서를 작성한다.

```text
docs/DASHBOARD_REPORT.md
```

포함 내용:

```markdown
# DASHBOARD REPORT

## 1. 작업 개요

## 2. 구현한 API

## 3. 대시보드 구성

## 4. 포트폴리오 요약 방식

## 5. Frontend 연결 결과

## 6. 테스트 결과

## 7. 확인 필요 항목

## 8. 다음 단계 제안
```

## 완료 조건

```text
- /api/dashboard/summary 구현
- 대시보드 화면 API 연결
- 포트폴리오 KPI 표시
- 보유 종목 요약 표시
- 최근 거래 표시
- 최근 뉴스 표시
- 최근 알림 표시
- Backend compile 성공
- Frontend build 성공
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 다음과 같이 보고하세요.

```text
대시보드 / 투자 리포트 화면 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
