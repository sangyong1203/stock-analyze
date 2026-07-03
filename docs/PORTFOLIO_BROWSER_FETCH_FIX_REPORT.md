# PORTFOLIO BROWSER FETCH FIX REPORT

## 1. 작업 개요

- 작업 기준: `docs/CODEX_TASK_2.6.md`
- 목적: `/portfolio`, `/dashboard`에서 발생하던 `Failed to fetch` 원인을 확인하고, 실제 dev server 기준으로 UI 데이터 렌더링까지 검증
- 결과: backend CORS 설정이 고정 포트 기준이어서 alternate local port가 막히던 문제를 수정했고, browser에서 portfolio/dashboard/trades 데이터 렌더링을 확인했다

## 2. Failed to fetch 원인

사전 확인 결과:

- frontend 기본 API base:
  - `http://127.0.0.1:8000`
- backend 기존 allowed origins:
  - `http://localhost:5173`
  - `http://127.0.0.1:5173`

문제 상황:

- Vite dev 또는 preview가 항상 `5173`만 쓰지 않았다
- 실제 검증 중 다음 포트가 사용됐다:
  - `5174`
  - `4173`
- 이 경우 frontend origin은 바뀌지만 backend CORS 허용 목록은 그대로여서 preflight가 막혔다

원인 정리:

- root cause: local browser origin 포트가 바뀔 때 backend CORS가 이를 허용하지 못함
- 결과: browser에서 `Failed to fetch` 발생

## 3. 수정 내용

수정 파일:

- `backend/app/core/config.py`
- `backend/app/main.py`

적용 내용:

- 기존 명시적 `allowed_origins`는 유지
- 추가로 아래 regex 기반 허용 적용

```text
^https?://(localhost|127\.0\.0\.1)(:\d+)?$
```

의도:

- `localhost`와 `127.0.0.1`의 local dev/preview 포트를 유연하게 허용
- portfolio 계산 로직이나 DB 데이터는 건드리지 않음

## 4. API 검증 결과

직접 API 확인:

- `/health`: 200
- `/api/portfolio/summary`: 200
- `/api/holdings`: 200
- `/api/holdings/summary`: 200
- `/api/dashboard/summary`: 200

핵심 값:

- `portfolio.total_market_value = 2283500.00`
- `portfolio.total_unrealized_profit_loss = -2824590.00`
- `holdings.holding_count = 4`
- `dashboard.portfolio_summary.total_market_value = 2283500.00`

preflight 검증:

- origin `http://127.0.0.1:5174`: 200
- origin `http://127.0.0.1:4173`: 200
- origin `http://localhost:5173`: 200

## 5. 브라우저 UI 검증 결과

실행 환경:

- backend: `http://127.0.0.1:8000`
- frontend dev: `http://127.0.0.1:5173`

검증 라우트:

- `/portfolio`
- `/dashboard`
- `/trades`

확인 결과:

- `/portfolio`
  - 보유 종목 4건 표시
  - `삼성SDI`, `두산에너빌리티`, `삼성E&A`, `NAVER` 표시
  - `총 자산 2,283,500원`
  - `평가금액 2,283,500원`
  - `평가손익 -2,824,590원`
  - `현금 잔고 0원`
- `/dashboard`
  - `총 자산 2,283,500원`
  - `현금 잔고 0원`
  - `평가 손익 -2,824,590원`
  - `보유 종목 4`
  - `총 매수금액 5,108,090원`
- `/trades`
  - 거래 목록 4건 표시
  - 4개 종목 거래가 화면에 보임

## 6. 포트폴리오 수치 검증

검증 기준값:

- `total_cash = 0`
- `total_invested_amount = 5108090`
- `total_market_value = 2283500`
- `total_unrealized_profit_loss = -2824590`
- `holding_count = 4`

화면 반영 확인:

- portfolio 화면 수치 일치: success
- dashboard 화면 수치 일치: success
- trades 화면 row count 4 확인: success
- portfolio 데이터 변경 없음: success

## 7. 보류 / 확인 필요 항목

- in-app browser log에는 이전 `4173` 세션에서 발생한 오래된 `Failed to fetch` 항목이 남아 있었다
- 하지만 현재 `5173` 페이지는 실제 데이터가 렌더링되므로, active fetch path는 정상으로 판단했다
- 완전히 깨끗한 console audit이 필요하면 fresh browser session에서 한 번 더 확인할 수 있다
