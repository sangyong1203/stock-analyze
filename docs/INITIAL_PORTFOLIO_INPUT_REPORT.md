# INITIAL PORTFOLIO INPUT REPORT

## 1. 작업 개요

- 작업 기준: `docs/CODEX_TASK_2.3.md`
- 목적: 실제 초기 보유 종목을 initial BUY 거래로 입력하기 전, 백업과 종목 코드 매칭을 검증하고 입력 가능 여부를 판단
- 결과: 입력 전 백업은 성공했지만, 필수 stock code 누락으로 실제 입력은 중단

## 2. 백업 결과

- source DB: `backend/stock_analyze.db`
- backup file: `storage/backups/stock_analyze_before_initial_holdings_input_20260703_110349.db`
- source size: `72810496`
- backup size: `72810496`
- verification: `ok`

## 3. 입력 데이터

- fund pool name: `기본 투자계좌`
- initial deposit target: `11,231,348`
- trade date: `2026-07-03`
- trade memo:
  - `초기 보유 종목 등록 - 사용자 제공 평가금액/손익 기준 역산 평단가`

입력 대상 종목:

| stock_code | stock_name | quantity | cost_amount | exact_average_price | rounded_average_price |
|---|---:|---:|---:|---:|---:|
| `368590` | RISE 미국나스닥100 | 95 | 2119218 | 22307.5578947368 | 22308 |
| `006400` | 삼성SDI | 5 | 2984850 | 596970 | 596970 |
| `411060` | ACE KRX금현물 | 50 | 1586580 | 31731.6 | 31732 |
| `442320` | RISE 글로벌자율주행 | 25 | 1142115 | 45684.6 | 45685 |
| `034020` | 두산에너빌리티 | 10 | 1052150 | 105215 | 105215 |
| `422420` | RISE 2차전지TOP10 | 90 | 820010 | 9111.2222222222 | 9111 |
| `028050` | 삼성E&A | 10 | 558090 | 55809 | 55809 |
| `035420` | NAVER | 2 | 513000 | 256500 | 256500 |
| `487240` | KODEX AI전력핵심설비 | 10 | 455335 | 45533.5 | 45534 |

## 4. 종목 코드 매칭 결과

### Matched

| stock_code | result |
|---|---|
| `006400` | matched |
| `034020` | matched |
| `028050` | matched |
| `035420` | matched |

### Missing

| stock_code | result |
|---|---|
| `368590` | missing |
| `411060` | missing |
| `442320` | missing |
| `422420` | missing |
| `487240` | missing |

## 5. 자금 풀 / 입금 결과

- fund pool create: not performed
- deposit create: not performed

이유:

- 필수 stock code 누락으로 전체 입력을 중단
- partial input 금지 조건 준수

## 6. 거래 입력 결과

- initial BUY trade insert count: `0`
- holdings direct edit: not performed
- partial trade insert: not performed

## 7. holdings 검증 결과

- `/api/holdings/summary`
  - `holding_count = 0`
  - `total_market_value = 0`
  - `total_unrealized_profit_loss = 0`
  - `total_realized_profit_loss = 0`

## 8. portfolio 검증 결과

- `/api/funds/summary`
  - `active_pool_count = 0`
  - `total_cash = 0`
  - `transaction_count = 0`
- `/api/portfolio/summary`
  - `total_asset_value = 0`
  - `holding_count = 0`
  - `total_cash = 0`

## 9. dashboard 검증 결과

- `/api/dashboard/summary`
  - portfolio summary baseline unchanged
  - recent trades empty
  - dashboard KPI remained baseline

## 10. 반올림 사용 여부

- actual insert가 실행되지 않았으므로 rounding rule was not applied
- 입력이 재개되면 저장 정밀도(`Numeric(20, 2)`) 기준으로 재평가 필요

## 11. 보류 / 확인 필요 항목

- `368590`, `411060`, `442320`, `422420`, `487240`가 `stocks`에 없음
- 누락 종목 해소 전에는 전체 initial portfolio input을 다시 시작하지 않는 것이 적절함
- 재시도 시 현재 백업 파일 기준으로 시작하는 것이 안전함
