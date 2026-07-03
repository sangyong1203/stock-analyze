# NON ETF INITIAL PORTFOLIO INPUT REPORT

## 1. 작업 개요

- 작업 기준: `docs/CODEX_TASK_2.4.md`
- 목적: ETF를 제외하고 현재 `stocks`에 존재하는 일반 주식 4개만 초기 BUY 거래로 입력한 뒤, funds/trades/holdings/portfolio/dashboard 정합성을 검증
- 결과: live DB 입력 완료, API 기준 정합성 확인 완료, 브라우저 preview 검증은 부분 완료

## 2. ETF 제외 확정

아래 ETF 코드는 이번 작업에서 입력하지 않았다.

- `368590` RISE 미국나스닥100
- `411060` ACE KRX금현물
- `442320` RISE 글로벌자율주행
- `422420` RISE 2차전지TOP10
- `487240` KODEX AI전력핵심설비

검증 결과:

- ETF stock master 추가: 미수행
- ETF trade 생성: `0`
- ETF holdings 생성: `0`

## 3. 백업 결과

- source DB: `backend/stock_analyze.db`
- backup file: `storage/backups/stock_analyze_before_non_etf_initial_input_20260703_111724.db`
- backup size: `72810496`
- verification: backup file exists

## 4. 입력 데이터

- fund pool name: `기본 투자계좌`
- initial deposit: `5,108,090`
- trade date: `2026-07-03`
- trade memo:
  - `초기 보유 종목 등록 - ETF 제외, 일반 주식만 입력`

입력 종목:

| stock_code | stock_name | quantity | average_price | cost_amount |
|---|---|---:|---:|---:|
| `006400` | 삼성SDI | 5 | 596970 | 2984850 |
| `034020` | 두산에너빌리티 | 10 | 105215 | 1052150 |
| `028050` | 삼성E&A | 10 | 55809 | 558090 |
| `035420` | NAVER | 2 | 256500 | 513000 |

## 5. 자금 풀 / 입금 결과

- fund pool create: success
  - id: `1`
  - name: `기본 투자계좌`
- deposit create: success
  - amount: `5108090.00`
  - transaction type: `deposit`
- funds summary:
  - `active_pool_count = 1`
  - `total_cash = 0`
  - `total_deposit_amount = 5108090.00`
  - `total_withdraw_amount = 0`
  - `transaction_count = 5`

참고:

- transaction count `5`는 입금 1건과 BUY 거래 연동 자금 내역 4건을 포함한다.

## 6. 거래 입력 결과

- BUY trade insert count: `4`
- inserted trade rows:
  - `006400` quantity `5`, price `596970.00`, total `2984850.00`
  - `034020` quantity `10`, price `105215.00`, total `1052150.00`
  - `028050` quantity `10`, price `55809.00`, total `558090.00`
  - `035420` quantity `2`, price `256500.00`, total `513000.00`
- `/api/trades` row count: `4`

## 7. holdings 검증 결과

- `/api/holdings/summary`
  - `holding_count = 4`
  - `closed_holding_count = 0`
  - `total_market_value = 2386500.00`
  - `total_unrealized_profit_loss = -2721590.00`
  - `total_realized_profit_loss = 0`

개별 holdings:

| stock_code | stock_name | quantity | average_price |
|---|---|---:|---:|
| `006400` | 삼성SDI | 5 | 596970 |
| `028050` | 삼성E&A | 10 | 55809 |
| `034020` | 두산에너빌리티 | 10 | 105215 |
| `035420` | NAVER | 2 | 256500 |

검증 포인트:

- 수량 일치: success
- 평균단가 일치: success
- ETF holding 없음: success

## 8. portfolio 검증 결과

- `/api/portfolio/summary`
  - `total_cash = 0`
  - `total_invested_amount = 5108090.00`
  - `total_market_value = 2386500.00`
  - `total_unrealized_profit_loss = -2721590.00`
  - `realized_profit_loss = 0`
  - `total_asset_value = 2386500.00`
  - `holding_count = 4`

검증 포인트:

- 입력 원가 합계와 투자금 일치: success
- 현금 잔고 0 반영: success
- 일반 주식 4개만 반영: success

## 9. dashboard 검증 결과

- `/api/dashboard/summary`
  - `portfolio_summary.holding_count = 4`
  - `holding_summary.holding_count = 4`
  - `recent_trades` contains 4 BUY rows
  - `top_holdings` contains only the 4 non-ETF stocks

브라우저 preview 확인:

- checked routes:
  - `/portfolio`
  - `/trades`
  - `/dashboard`
- result:
  - route shell load: success
  - preview-mode data fetch: failed
  - cause observed: `TypeError: Failed to fetch`

따라서 화면 데이터 정확성은 API 검증 결과를 기준으로 확정했다.

## 10. 보류 / 확인 필요 항목

- Browser preview에서는 `/api/*` fetch가 실패해 실제 화면 렌더링 검증을 끝까지 완료하지 못했다.
- 이번 작업 범위는 live DB 입력과 API 정합성 검증이므로, 추가 코드 수정 없이 결과만 기록했다.
