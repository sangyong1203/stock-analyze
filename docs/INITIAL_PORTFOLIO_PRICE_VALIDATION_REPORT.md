# INITIAL PORTFOLIO PRICE VALIDATION REPORT

## 1. 작업 개요

- 작업 기준: `docs/CODEX_TASK_2.5.md`
- 목적: 초기 입력된 4개 일반주식 포트폴리오의 현재가 기준, 평가금액, 평가손익 계산이 최신 가격 데이터 기준으로 맞는지 검증
- 결과: 기존 KRX 일별 수집 API로 `2025-07-03` 가격을 적재했고, holdings 재계산 후 API/DB 기준 정합성을 확인했다

## 2. 현재 입력된 포트폴리오

| stock_code | stock_name | quantity | average_price | cost_amount |
|---|---|---:|---:|---:|
| `006400` | 삼성SDI | 5 | 596970 | 2984850 |
| `034020` | 두산에너빌리티 | 10 | 105215 | 1052150 |
| `028050` | 삼성E&A | 10 | 55809 | 558090 |
| `035420` | NAVER | 2 | 256500 | 513000 |

고정 검증 결과:

- quantity 변경 없음
- average_price 변경 없음
- total cost amount 합계 `5,108,090` 유지

## 3. 가격 데이터 기준일 확인

사전 확인:

- `/api/prices/summary.latest_price_date = 2025-06-24`

dry-run 확인:

- `2025-06-25`: fetched success
- `2025-06-30`: fetched success
- `2025-07-03`: fetched success
- `2026-07-03`: fetched `0`

판단:

- 이번 검증에서 실제 최신 거래일로 확인된 날짜는 `2025-07-03`

실제 적재 결과:

- API: `/api/prices/collect/krx/daily`
- request date: `2025-07-03`
- fetched `2758`
- inserted `2758`
- updated `0`
- stock created `1`

사후 확인:

- `/api/prices/summary.latest_price_date = 2025-07-03`

## 4. 종목별 현재가 검증

| stock_code | latest_price_date | latest_close | holdings.current_price | match |
|---|---|---:|---:|---|
| `006400` | `2025-07-03` | 185300 | 185300 | success |
| `034020` | `2025-07-03` | 61900 | 61900 | success |
| `028050` | `2025-07-03` | 23200 | 23200 | success |
| `035420` | `2025-07-03` | 253000 | 253000 | success |

주의 사항:

- 가격 적재와 holdings 재계산을 병렬로 실행하면 holdings가 직전 가격을 유지할 수 있다.
- 이번 작업에서는 적재 완료 후 holdings 재계산을 다시 실행해 최종 값을 확정했다.

## 5. holdings 재계산 결과

| stock_code | quantity | average_price | total_buy_amount | current_price | market_value | unrealized_profit_loss | unrealized_profit_loss_rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| `006400` | 5 | 596970 | 2984850 | 185300 | 926500 | -2058350 | -0.6896 |
| `034020` | 10 | 105215 | 1052150 | 61900 | 619000 | -433150 | -0.4117 |
| `028050` | 10 | 55809 | 558090 | 23200 | 232000 | -326090 | -0.5843 |
| `035420` | 2 | 256500 | 513000 | 253000 | 506000 | -7000 | -0.0136 |

계산 검증:

- `market_value = current_price * quantity`: success
- `unrealized_profit_loss = market_value - total_buy_amount`: success
- quantity 유지: success
- average_price 유지: success

## 6. portfolio summary 검증 결과

- `/api/portfolio/summary`
  - `total_cash = 0`
  - `total_invested_amount = 5108090.00`
  - `total_market_value = 2283500.00`
  - `total_unrealized_profit_loss = -2824590.00`
  - `total_unrealized_profit_loss_rate = -0.5529640237348989544037007962`
  - `realized_profit_loss = 0`
  - `total_asset_value = 2283500.00`
  - `holding_count = 4`

합계 검증:

- holdings market value 합계:
  - `926500 + 619000 + 232000 + 506000 = 2283500`
- holdings unrealized P/L 합계:
  - `-2058350 + -433150 + -326090 + -7000 = -2824590`
- portfolio summary와 일치: success

## 7. dashboard 검증 결과

- `/api/dashboard/summary`
  - `portfolio_summary.total_market_value = 2283500.00`
  - `holding_summary.total_market_value = 2283500.00`
  - `holding_summary.holding_count = 4`
  - `top_holdings` reflects the same 4 stocks

결론:

- dashboard API 값은 portfolio/holdings 요약과 일치한다

## 8. 사용자 제공 이전 평가금액과 비교

| stock_code | old_current_value | system_current_value | difference | system_profit_loss |
|---|---:|---:|---:|---:|
| `006400` | 2242500 | 926500 | -1316000 | -2058350 |
| `034020` | 804000 | 619000 | -185000 | -433150 |
| `028050` | 403500 | 232000 | -171500 | -326090 |
| `035420` | 384200 | 506000 | 121800 | -7000 |

차이 원인 추정:

- 사용자가 준 이전 평가금액은 이번 시스템 검증에서 확인된 최신 거래일 기준 가격과 다르다
- 이번 시스템 값은 `2025-07-03` KRX 적재 후 재계산된 값이다
- 따라서 가격 기준일 차이가 가장 큰 원인으로 보인다

## 9. 발견된 문제

- 첫 holdings 재계산이 가격 적재 완료 전에 수행되면 holdings 값이 이전 가격을 유지할 수 있었다
- 이 문제는 코드 수정 없이, 가격 적재 완료 후 재계산을 다시 수행해 해결했다
- in-app browser에서는 `/portfolio`, `/dashboard` 모두 `Failed to fetch`가 발생해 UI 수치 검증을 완료하지 못했다

## 10. 보류 / 확인 필요 항목

- 환경 현재 날짜는 `2026-07-03`이지만, 이번 실행에서 실제 행이 내려온 최신 KRX 날짜는 `2025-07-03`이었다
- 따라서 본 리포트의 최신 가격 기준일은 `2025-07-03`으로 기록했다
- 브라우저 기반 검증은 fetch 실패 해소 후 별도로 다시 확인할 수 있다
