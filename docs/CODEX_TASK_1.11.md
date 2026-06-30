# CODEX_TASK_1.11

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

KRX 가격 수집, 차트 지표, 차트 UX 작업은 완료됐습니다.

이번 작업은 **거래 기록 / 보유 종목 / 손익 계산 구조 구현**입니다.

## 작업 목표

1. 매수/매도 거래 기록을 저장한다.
2. 거래 기록을 기반으로 보유 종목을 계산/갱신한다.
3. 평균단가, 보유수량, 평가금액, 평가손익을 계산한다.
4. 입금/출금/현금 잔고 구조를 구현한다.
5. 포트폴리오 요약 API와 화면을 연결한다.
6. 기존 DB 테이블만 사용한다.
7. 새 테이블과 마이그레이션은 만들지 않는다.

## 작업 전 확인

직전 `DEVELOPMENT_REPORT.md`의 완료/미완료/확인 필요 항목만 확인한다.

이번 작업에서 필요한 기존 모델만 확인한다.

```text
fund_pools
fund_transactions
trades
holdings
stocks
stock_prices
```

주의:

```text
- 기준 문서를 반복해서 다시 읽지 않는다.
- 새 DB 테이블을 만들지 않는다.
- 새 마이그레이션을 만들지 않는다.
- 기존 모델 필드 안에서 구현한다.
- 필드가 부족하거나 애매하면 임의 추가하지 말고 확인 필요 항목에 기록한다.
```

## Backend 작업 항목

대상 후보:

```text
backend/app/domains/portfolio/
backend/app/domains/trades/
backend/app/domains/funds/
backend/app/domains/holdings/
backend/app/main.py
```

필요한 API를 구현한다.

### 1. 자금 API

```text
GET  /api/funds/pools
POST /api/funds/pools
GET  /api/funds/transactions
POST /api/funds/transactions
GET  /api/funds/summary
```

기능:

```text
- 투자 자금 풀 생성/조회
- 입금/출금 기록
- 현재 현금 잔고 계산
- 거래와 연결 가능한 fund_pool 기준 정리
```

### 2. 거래 기록 API

```text
GET    /api/trades
POST   /api/trades
GET    /api/trades/{trade_id}
PATCH  /api/trades/{trade_id}
DELETE /api/trades/{trade_id}
```

거래 타입:

```text
BUY
SELL
```

거래 기록 필수 개념:

```text
stock_id
trade_type
trade_date
quantity
price
fee
tax
memo
fund_pool_id
```

기존 필드명이 다르면 기존 모델 기준으로 맞춘다.

### 3. 보유 종목 API

```text
GET  /api/holdings
GET  /api/holdings/summary
POST /api/holdings/recalculate
```

기능:

```text
- trades 기준 holdings 재계산
- 보유 수량 계산
- 평균단가 계산
- 현재가 기준 평가금액 계산
- 평가손익 / 평가손익률 계산
- 보유수량 0 이하 종목 처리
```

### 4. 포트폴리오 요약 API

```text
GET /api/portfolio/summary
```

응답에 포함:

```text
total_cash
total_invested_amount
total_market_value
total_unrealized_profit_loss
total_unrealized_profit_loss_rate
realized_profit_loss
total_asset_value
holding_count
today_change_amount
today_change_rate
```

계산이 어려운 항목은 가능한 범위에서 구현하고, 애매한 항목은 확인 필요 항목에 기록한다.

## 계산 기준

### 매수

```text
buy_amount = quantity * price
buy_total_cost = buy_amount + fee + tax
```

매수 시:

```text
- 현금 감소
- 보유 수량 증가
- 평균단가 재계산
```

### 매도

```text
sell_amount = quantity * price
sell_net_amount = sell_amount - fee - tax
realized_profit_loss = sell_net_amount - 평균단가 * quantity
```

매도 시:

```text
- 현금 증가
- 보유 수량 감소
- 실현손익 계산
- 남은 보유분 평균단가는 기존 평균단가 유지
```

### 평가손익

```text
market_value = holding_quantity * stocks.current_price
unrealized_profit_loss = market_value - holding_quantity * average_price
unrealized_profit_loss_rate = unrealized_profit_loss / (holding_quantity * average_price)
```

현재가가 없으면 평가금액/평가손익은 null 또는 0으로 안전 처리한다.

## Frontend 작업 항목

대상 후보:

```text
frontend/src/pages/main/portfolio/
frontend/src/pages/main/trades/
frontend/src/pages/main/stocks/
```

구현 항목:

1. 거래 기록 화면 API 연결
2. 매수/매도 입력 폼
3. 거래 목록 조회
4. 보유 종목 목록 표시
5. 포트폴리오 요약 카드 표시
6. 평가손익/수익률 표시
7. 자금 입금/출금 입력
8. 로딩/오류/빈 데이터 상태 처리

화면이 아직 골격만 있으면 MVP 수준으로 연결한다.

## 검증 항목

Backend:

```text
- python -m compileall app 성공
- fund pool 생성/조회 성공
- 입금/출금 기록 성공
- 매수 거래 등록 성공
- 매도 거래 등록 성공
- holdings 재계산 성공
- /api/holdings/summary 성공
- /api/portfolio/summary 성공
- 현재가 기준 평가손익 계산 확인
```

Frontend:

```text
- 거래 기록 화면 표시
- 매수/매도 등록 폼 동작
- 보유 종목 목록 표시
- 포트폴리오 요약 표시
- npm run build 성공
```

Regression:

```text
/health
/api/auth/status
/api/prices/summary
/api/charts/stocks/2/ohlcv?limit=130
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
docs/PORTFOLIO_TRADE_REPORT.md
```

포함 내용:

```markdown
# PORTFOLIO TRADE REPORT

## 1. 작업 개요

## 2. 구현한 API

## 3. 거래 계산 기준

## 4. holdings 재계산 방식

## 5. 포트폴리오 요약 계산 방식

## 6. Frontend 연결 결과

## 7. 테스트 결과

## 8. 확인 필요 항목

## 9. 다음 단계 제안
```

## 완료 조건

```text
- 거래 기록 CRUD 구현
- 입금/출금 기록 구현
- holdings 재계산 구현
- 평균단가 계산 구현
- 평가금액/평가손익 계산 구현
- 포트폴리오 요약 API 구현
- 거래/포트폴리오 화면 API 연결
- Backend compile 성공
- Frontend build 성공
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 다음과 같이 보고하세요.

```text
거래 기록, 보유 종목, 손익 계산 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
