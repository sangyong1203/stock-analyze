# CODEX TASK 2.5 REPORT

## Scope

- Task file: `docs/CODEX_TASK_2.5.md`
- Work type: initial portfolio current-price validation, latest KRX price refresh, holdings recalculation, and reporting

## Summary

- 초기 4개 보유 종목의 수량과 평균단가는 그대로 유지했다
- 가격 기준은 기존 `stock_prices` 최신일 `2025-06-24`에서 `2025-07-03`으로 갱신됐다
- 기존 KRX 일별 수집 API와 holdings 재계산 API만 사용했다
- holdings, portfolio, dashboard API 값이 최신 가격 기준으로 다시 맞춰진 것을 확인했다
- 브라우저 검증은 `Failed to fetch`로 부분 완료 처리했다

## Work completed

1. holdings 평가 계산이 `stocks.current_price` 기준인지 확인했다
2. held-stock 최신 `stock_prices` 날짜와 종가를 확인했다
3. KRX 일별 수집 dry-run으로 실제 최신 수집 가능 날짜를 확인했다
4. `2025-07-03` KRX 일별 가격을 실제 적재했다
5. holdings 재계산을 다시 실행했다
6. `/api/holdings`, `/api/holdings/summary`, `/api/portfolio/summary`, `/api/dashboard/summary`, `/api/prices/summary`를 검증했다
7. 사용자 제공 이전 평가금액과 시스템 최신 평가금액을 비교했다
8. `INITIAL_PORTFOLIO_PRICE_VALIDATION_REPORT.md`를 작성했다

## Verification

- `python -m compileall app`: success
- `npm run build`: success
- dry-run `2025-07-03`: success
- actual collect `2025-07-03`: success
- `/api/prices/summary`: 200
- `/api/holdings`: 200
- `/api/holdings/summary`: 200
- `/api/portfolio/summary`: 200
- `/api/dashboard/summary`: 200
- latest price date after refresh: `2025-07-03`
- holding count: `4`
- total cost basis unchanged: `5,108,090`

## Files changed

- `docs/CODEX_PROGRESS.md`
- `docs/DEVELOPMENT_REPORT.md`
- `docs/INITIAL_PORTFOLIO_PRICE_VALIDATION_REPORT.md`
- `docs/CODEX_TASK_2.5_REPORT.md`

## Final note

CODEX_TASK_2.5 초기 포트폴리오 현재가 검증 작업 완료했습니다.
`DEVELOPMENT_REPORT.md`와 `INITIAL_PORTFOLIO_PRICE_VALIDATION_REPORT.md`를 확인해 주세요.
