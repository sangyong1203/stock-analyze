# CODEX_TASK_2.6

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

CODEX_TASK_2.5에서 초기 포트폴리오 현재가 검증은 API/DB 기준으로 완료됐습니다.
다만 브라우저에서 `/portfolio`, `/dashboard` 확인 시 `Failed to fetch`가 발생해 실제 UI 수치 검증은 완료되지 않았습니다.

이번 작업은 **브라우저 Failed to fetch 원인 수정 / 실제 UI 포트폴리오 화면 검증**입니다.

## 목표

1. `/portfolio`, `/dashboard`에서 발생하는 `Failed to fetch` 원인을 확인한다.
2. 실제 dev server 환경에서 API 요청이 정상 연결되도록 수정한다.
3. 포트폴리오/대시보드 화면에서 실제 보유종목, 평가금액, 손익이 렌더링되는지 확인한다.
4. 기존 포트폴리오 데이터, 거래, 수량, 평단가는 변경하지 않는다.
5. 새 기능, 새 테이블, 새 마이그레이션은 만들지 않는다.
6. 실제 Gmail 발송은 하지 않는다.

## 작업 전 확인

직전 문서만 확인한다.

```text
docs/DEVELOPMENT_REPORT.md
docs/INITIAL_PORTFOLIO_PRICE_VALIDATION_REPORT.md
```

기준 문서를 반복해서 다시 읽지 않는다.

## 현재 검증된 포트폴리오 기준값

아래 값은 변경하지 않는다.

```csv
stock_name,stock_code,quantity,average_price,current_price,market_value,unrealized_profit_loss
삼성SDI,006400,5,596970,185300,926500,-2058350
두산에너빌리티,034020,10,105215,61900,619000,-433150
삼성E&A,028050,10,55809,23200,232000,-326090
NAVER,035420,2,256500,253000,506000,-7000
```

포트폴리오 합계 기준값:

```text
total_cash = 0
total_invested_amount = 5108090
total_market_value = 2283500
total_unrealized_profit_loss = -2824590
holding_count = 4
```

## 1. 실행 환경 확인

Backend와 Frontend를 dev 기준으로 실행한다.

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

브라우저 접속 URL:

```text
http://127.0.0.1:5173/portfolio
http://127.0.0.1:5173/dashboard
```

주의:

```text
- npm run preview 기준이 아니라 npm run dev 기준으로 먼저 확인한다.
- preview에서만 발생하는 문제인지, dev에서도 발생하는 문제인지 분리한다.
```

## 2. Failed to fetch 원인 분리

브라우저 콘솔과 네트워크 탭에서 확인한다.

확인 항목:

```text
1. API 요청 URL
2. 요청 origin
3. backend 응답 여부
4. CORS 에러 여부
5. OPTIONS preflight 실패 여부
6. VITE_API_BASE_URL 값
7. frontend fallback API base URL
8. backend ALLOWED_ORIGIN / ALLOWED_ORIGINS 적용 여부
9. Mixed host 문제
   - localhost vs 127.0.0.1
10. preview 환경에서 /api proxy 미적용 문제 여부
```

## 3. API 직접 확인

브라우저 문제와 별도로 API는 직접 확인한다.

```text
/api/portfolio/summary
/api/holdings
/api/holdings/summary
/api/dashboard/summary
```

기대값:

```text
portfolio.total_market_value = 2283500
portfolio.total_unrealized_profit_loss = -2824590
holdings.holding_count = 4
dashboard.portfolio_summary.total_market_value = 2283500
```

## 4. 수정 기준

원인이 확인되면 최소 범위만 수정한다.

가능한 수정 후보:

```text
- frontend API base URL 설정 정리
- dev/preview 환경별 API base fallback 보정
- Vite proxy 설정 확인 또는 보정
- backend CORS allowed origins 보정
- localhost / 127.0.0.1 혼용 문제 수정
```

주의:

```text
- 포트폴리오 계산 로직은 수정하지 않는다.
- holdings/trades/funds 데이터는 수정하지 않는다.
- DB schema 변경 금지
- 새 migration 금지
```

## 5. 브라우저 UI 검증

수정 후 Codex in-app browser로 아래 화면을 확인한다.

```text
/portfolio
/dashboard
/trades
```

확인 항목:

```text
- 보유 종목 4개 표시
- 삼성SDI, 두산에너빌리티, 삼성E&A, NAVER 표시
- 총 투자금 5,108,090원 표시
- 총 평가금액 2,283,500원 표시
- 평가손익 -2,824,590원 표시
- 현금 0원 표시
- 거래내역 4건 표시
- dashboard KPI와 portfolio summary 일치
- 콘솔 application error 없음
- network Failed to fetch 없음
- 한글 깨짐 없음
```

## 6. 검증

Backend:

```bash
cd backend
python -m compileall app
```

Frontend:

```bash
cd frontend
npm run build
```

API regression:

```text
/health
/api/portfolio/summary
/api/holdings/summary
/api/dashboard/summary
```

브라우저 route:

```text
/portfolio
/dashboard
/trades
```

## 7. 금지 사항

```text
- 수량 변경 금지
- 평균단가 변경 금지
- 기존 BUY 거래 수정/삭제 금지
- holdings 직접 수정 금지
- 평가금액 수동 입력 금지
- 실제 Gmail 발송 금지
- 새 기능 추가 금지
- 새 테이블 생성 금지
- 새 마이그레이션 생성 금지
```

## 8. 문서 갱신

작업 완료 후 아래 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 작성:

```text
docs/PORTFOLIO_BROWSER_FETCH_FIX_REPORT.md
```

포함 내용:

```markdown
# PORTFOLIO BROWSER FETCH FIX REPORT

## 1. 작업 개요

## 2. Failed to fetch 원인

## 3. 수정 내용

## 4. API 검증 결과

## 5. 브라우저 UI 검증 결과

## 6. 포트폴리오 수치 검증

## 7. 보류 / 확인 필요 항목
```

## 완료 보고

작업 완료 후 다음과 같이 보고하세요.

```text
CODEX_TASK_2.6 브라우저 Failed to fetch 수정 및 포트폴리오 UI 검증 작업 완료했습니다.
DEVELOPMENT_REPORT.md와 PORTFOLIO_BROWSER_FETCH_FIX_REPORT.md를 확인해 주세요.
```
