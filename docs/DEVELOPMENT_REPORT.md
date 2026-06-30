# DEVELOPMENT REPORT

## 1. 작업 개요

- 작업: CODEX_TASK_1.11 거래 기록 / 보유 종목 / 손익 계산 구조 구현
- 목적: 자금 풀, 입출금, 매수/매도 거래, holdings 재계산, 포트폴리오 요약을 기존 테이블 기준으로 구현
- DB 변경: 없음
- 마이그레이션: 없음

## 2. 참고 문서

- `AGENTS.md`
- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`
- `docs/CODEX_TASK_1.11.md`

## 3. 완료 작업

- `/api/funds/*` 자금 풀/입출금 API 구현
- `/api/trades` 거래 기록 CRUD 구현
- `/api/holdings`, `/api/holdings/summary`, `/api/holdings/recalculate` 구현
- `/api/portfolio/summary` 구현
- 평균단가 방식 holdings 재계산 구현
- 매도 실현손익 계산 구현
- 현재가 기준 평가금액/평가손익 계산 구현
- 거래 화면 API 연결 및 등록/수정/삭제 폼 구현
- 포트폴리오 화면 요약 카드/보유 목록/입출금/재계산 연결

## 4. 생성 파일

- `backend/app/domains/funds/__init__.py`
- `backend/app/domains/funds/router.py`
- `backend/app/domains/funds/service.py`
- `backend/app/domains/funds/repository.py`
- `backend/app/domains/funds/schemas.py`
- `backend/app/domains/holdings/__init__.py`
- `backend/app/domains/holdings/router.py`
- `backend/app/domains/holdings/service.py`
- `backend/app/domains/holdings/repository.py`
- `backend/app/domains/holdings/schemas.py`
- `docs/PORTFOLIO_TRADE_REPORT.md`
- `docs/CODEX_TASK_1.11_REPORT.md`

## 5. 수정 파일

- `backend/app/domains/trades/router.py`
- `backend/app/domains/trades/service.py`
- `backend/app/domains/trades/repository.py`
- `backend/app/domains/trades/schemas.py`
- `backend/app/domains/portfolio/router.py`
- `backend/app/domains/portfolio/service.py`
- `backend/app/domains/portfolio/repository.py`
- `backend/app/domains/portfolio/schemas.py`
- `backend/app/main.py`
- `frontend/src/pages/main/trades/TradesPage.vue`
- `frontend/src/pages/main/trades/service/trades.api.ts`
- `frontend/src/pages/main/trades/service/trades.types.ts`
- `frontend/src/pages/main/trades/service/trades.utils.ts`
- `frontend/src/pages/main/portfolio/PortfolioPage.vue`
- `frontend/src/pages/main/portfolio/service/portfolio.api.ts`
- `frontend/src/pages/main/portfolio/service/portfolio.types.ts`
- `frontend/src/pages/main/portfolio/service/portfolio.utils.ts`
- `docs/CODEX_PROGRESS.md`

## 6. Backend 구현 결과

- 신규 라우터:
  - `/api/funds`
  - `/api/holdings`
- 기존 라우터 확장:
  - `/api/trades`
  - `/api/portfolio/summary`
- 자금 흐름:
  - 입금/출금은 `fund_transactions`에 기록하고 `fund_pools.cash_balance`를 즉시 반영
  - 거래 생성/수정/삭제 시 대응하는 `fund_transactions`를 동기화
- holdings 계산:
  - trades를 시간순으로 순회
  - 매수 시 총원가(`amount + fee + tax`) 기준 평균단가 계산
  - 매도 시 평균단가 기준 실현손익 계산
  - `holdings`는 재계산 시 fund_pool 단위로 재작성
- 포트폴리오 요약:
  - 총 현금, 총 평가금액, 총 평가손익, 실현손익, 총자산, 보유 종목 수 계산
  - `today_change_amount`, `today_change_rate`는 `stocks.current_price`, `stocks.change_rate` 기준으로 계산

## 7. Frontend 구현 결과

- 거래 화면:
  - 자금 풀 선택
  - 종목 검색
  - 매수/매도 입력 폼
  - 거래 목록, 수정, 삭제
- 포트폴리오 화면:
  - 요약 카드
  - 자금 풀 생성
  - 입금/출금 입력
  - 보유 종목 목록
  - 현금 흐름 목록
  - holdings 재계산 버튼

## 8. DB 구현 결과

- 신규 테이블 없음
- 신규 마이그레이션 없음
- 기존 테이블만 사용:
  - `fund_pools`
  - `fund_transactions`
  - `trades`
  - `holdings`
  - `stocks`
  - `stock_prices`

## 9. 실행 방법

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

브라우저 접속:

```text
http://localhost:5173/trades
http://localhost:5173/portfolio
```

## 10. 테스트 결과

| 항목 | 결과 |
|---|---|
| `python -m compileall app` | 성공 |
| `npm run build` | 성공 |
| 자금 풀 생성 | 성공 |
| 입금 기록 | 성공 |
| 매수 거래 등록 | 성공 |
| 매도 거래 등록 | 성공 |
| holdings 재계산 | 성공 |
| `/api/holdings/summary` | 200 |
| `/api/portfolio/summary` | 200 |
| 평가손익 계산 | 성공 |
| `/health` | 200 |
| `/api/auth/status` | 200 |
| `/api/prices/summary` | 200 |
| `/api/charts/stocks/2/ohlcv?limit=130` | 200 |
| `/api/news/alerts/send/dry-run` | 200 |

## 11. 미완료 항목

- 거래 관련 뉴스 연결(`trade_news_links`) 입력 UI는 이번 작업 범위에서 제외
- 거래 당시 가격 스냅샷(`price_snapshot_id`) 자동 생성은 이번 작업 범위에서 제외

## 12. 확인 필요 항목

- 항목: `total_invested_amount` 해석
- 관련 문서: `docs/CODEX_TASK_1.11.md`
- 애매한 이유: 총 투자금이 누적 입금 기준인지 현재 보유 원가 기준인지 문서에서 명시되지 않음
- 가능한 선택지: 누적 입금액, 현재 보유 원가, 둘 다 별도 제공
- 추천안: 현재는 보유 원가(`holdings.total_buy_amount` 합계)로 구현
- 현재 구현 여부: 반영

- 항목: 오늘 변동 계산 기준
- 관련 문서: `docs/CODEX_TASK_1.11.md`
- 애매한 이유: 별도 전일 종가 필드 없이 `stocks.change_rate`만 존재
- 가능한 선택지: `change_rate` 역산 사용, 전일 종가 저장 구조 추가, today 항목 보류
- 추천안: MVP에서는 `current_price + change_rate` 역산 사용
- 현재 구현 여부: 반영

- 항목: 종목명 인코딩
- 관련 문서: `docs/DEVELOPMENT_REPORT.md` 직전 확인 필요 항목
- 애매한 이유: 일부 종목명이 DB에 깨진 문자열로 저장되어 거래/보유 화면에서도 그대로 표시됨
- 가능한 선택지: KRX 파서 인코딩 정비, 종목명 재수집
- 추천안: 데이터 정합성 작업에서 별도 정비
- 현재 구현 여부: 보류

## 13. 다음 단계 제안

- 거래 관련 뉴스 연결 입력 UI 추가
- 가격 스냅샷 자동 생성 연동
- 보유 종목 차트 빠른 이동
- 손절/목표가 기반 거래 보조 입력 검토

## 14. 최종 완료 문장

거래 기록, 보유 종목, 손익 계산 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
