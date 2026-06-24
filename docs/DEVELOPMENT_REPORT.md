# DEVELOPMENT REPORT

## 1. 작업 개요

- 프로젝트명: stock-analyze
- 작업 기준 문서:
  - INVESTMENT_SYSTEM_PLAN_v1.2.md
  - MVP_DB_SCHEMA_v1.2.md
  - CODEX_TASK_1.7.md
- 작업 범위: 1차 MVP 기반 구조, 종목/수집/뉴스/GPT/알림, Gmail 발송, KRX 가격 데이터 수집 및 차트 연결
- 작업 완료 여부: 완료

## 2. 완료한 작업

- [x] 1차 MVP 기반 구조 구현
  - 설명: FastAPI, SQLAlchemy, Alembic, Vue 3, Vite, Element Plus 기반 구조를 구성했다.
  - 관련 파일: backend/, frontend/

- [x] 종목/수집/뉴스/GPT/알림 구조 구현
  - 설명: 종목 CRUD, KODEX 구성종목 import, 네이버 금융 뉴스 수집, GPT 요약/필터, 뉴스 알림 후보, Gmail 발송 구조를 구현했다.
  - 관련 파일: backend/app/domains/, backend/app/external/, frontend/src/pages/main/

- [x] KRX 가격 데이터 수집 구조 구현
  - 설명: KRX daily price client, KOSPI/KOSDAQ endpoint 구조, `stock_prices` upsert, `stocks` 최신 가격 갱신, system_logs 오류 기록을 구현했다.
  - 관련 파일: backend/app/external/krx/, backend/app/domains/prices/

- [x] 가격 조회 및 차트 API 구현
  - 설명: 가격 요약, 종목별 가격, 최신 가격, 시장별 최신 가격, 차트용 OHLCV API를 구현했다.
  - 관련 파일: backend/app/domains/prices/, backend/app/domains/charts/

- [x] Frontend 가격/차트 연결
  - 설명: 종목 화면 KRX 가격 수집 버튼, 가격 컬럼 표시, 차트 화면 종목 선택 및 ECharts candlestick/거래량 표시를 구현했다.
  - 관련 파일: frontend/src/pages/main/stocks/, frontend/src/pages/main/charts/

## 3. 생성한 파일

| 파일 | 설명 |
| ---- | ---- |
| backend/app/external/krx/types.py | KRX 일봉 가격 타입 |
| backend/app/external/krx/parser.py | KRX 응답 파서 |
| backend/app/domains/prices/router.py | 가격 수집/조회 API 라우터 |
| frontend/src/pages/main/stocks/service/prices.api.ts | Frontend 가격 수집 API client |
| docs/KRX_PRICE_COLLECTION_REPORT.md | KRX 가격 수집 구조 리포트 |

## 4. 수정한 파일

| 파일 | 수정 내용 |
| ---- | --------- |
| backend/app/core/config.py | KRX 환경변수 추가 |
| backend/.env.example | KRX 환경변수 예시 추가 |
| backend/app/external/krx/client.py | KRX Open API client 구현 |
| backend/app/domains/prices/ | 가격 수집, upsert, 조회 서비스 구현 |
| backend/app/domains/charts/ | OHLCV 차트 API 구현 |
| backend/app/main.py | prices router 등록 |
| frontend/src/pages/main/stocks/StocksPage.vue | KRX 가격 수집 버튼 추가 및 한글 UI 정리 |
| frontend/src/pages/main/charts/ | ECharts 기반 OHLCV 차트 연결 |
| docs/CODEX_PROGRESS.md | CODEX_TASK_1.7 진행 결과 반영 |
| docs/DEVELOPMENT_REPORT.md | 최신 완료 결과 반영 |

## 5. 구현한 Backend 항목

- FastAPI 구조: 도메인별 라우터 구성
- DB 연결: SQLite 연결 유지
- SQLAlchemy 모델: 기존 27개 MVP 테이블 사용, 신규 테이블 없음
- Alembic: 신규 마이그레이션 없음
- API 라우터: prices router 신규 등록, charts OHLCV 보완
- Seed 구조: 변경 없음
- KRX client: POST 요청, 인증 header, timeout, 응답 status/JSON 검증, 숫자 정규화 구현
- 가격 저장: `stock_id + date + timeframe` 기준 insert/update
- 최신값 갱신: `stocks.current_price`, `change_rate`, `market_cap` 갱신

## 6. 구현한 Frontend 항목

- 라우터: 기존 차트/종목 메뉴 유지
- 레이아웃: 기존 MainLayout 사용
- 메뉴: 종목 화면과 차트 화면 보완
- 화면 골격: 종목 테이블 가격 컬럼, KRX 수집 버튼, 차트 종목 선택/조회 UI
- API 연결 상태: 가격 수집 API, 차트 OHLCV API 연결 완료

## 7. DB 구현 결과

- 생성한 테이블 수: 변경 없음
- 생성한 테이블 목록: 기존 27개 MVP 테이블 유지
- 생성한 인덱스: 변경 없음
- 마이그레이션 파일: 신규 없음
- SQLite DB 생성 여부: 기존 DB 사용

## 8. 실행 방법

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

### Migration

```bash
cd backend
python -m alembic upgrade head
python seeds/seed_defaults.py
```

### KRX 설정

```env
KRX_API_BASE_URL=https://data-dbg.krx.co.kr/svc/apis
KRX_AUTH_KEY=
```

## 9. 테스트 결과

- Backend compile: `python -m compileall app` 성공
- Frontend build: `npm run build` 성공
- `/api/prices/summary`: 200 응답
- `/api/prices/collect/krx/daily` dry_run: `KRX_AUTH_KEY` 설정 후 KOSPI `20250624` 기준 962건 조회 확인
- KRX `20260624` 기준 KOSPI: 빈 데이터 응답 확인
- KOSDAQ dry-run: 권한 재신청 후 `20250624` 기준 1795건 조회 확인
- KRX 실제 저장: `20250624`, markets `["KOSPI", "KOSDAQ"]`, `dry_run=false` 실행 성공
- KRX 실제 저장 결과: fetched 2757, inserted 2757, updated 0, stock_created 2410, error 0
- 가격 요약: total_price_rows 2757, latest_price_date 2025-06-24, KOSPI 962, KOSDAQ 1795
- 최신 가격 API: KOSPI/KOSDAQ 시장별 최신 가격 조회 200 응답
- 임의 종목 검증: 삼성전자 stock_id 2, 알테오젠 stock_id 202 최신 가격 및 OHLCV API 200 응답
- stocks 최신값 갱신: 삼성전자/알테오젠 current_price, change_rate, market_cap 갱신 확인
- 차트 화면: `/main/charts` route 200 응답 및 OHLCV API 정상 확인. in-app browser 미제공으로 시각 캔버스 직접 확인은 미수행
- KRX 반복 수집 검증: 동일 기준일 `20250624` 재실행 결과 fetched 2757, inserted 0, updated 2757, stock_created 0, error 0
- 중복 row 검증: `stock_id + date + timeframe` 중복 그룹 0건, total_price_rows 2757 유지
- 반복 수집 후 삼성전자/알테오젠 latest 및 OHLCV API 정상 유지
- mock KRX 수집 검증: insert 1건, update 1건, 신규 stock 생성, 최신값 갱신 성공
- `/api/prices/stocks/{stock_id}/latest`: mock 데이터 기준 200 응답
- `/api/charts/stocks/{stock_id}/ohlcv`: mock 데이터 기준 200 응답
- mock 검증용 임시 종목/가격 데이터 삭제 확인
- 오류 여부: 최종 API 검증 기준 오류 없음

## 10. 미완료 항목

- 항목: 차트 화면 시각 확인
- 이유: 현재 세션에서 in-app browser가 제공되지 않아 캔버스 렌더링을 직접 확인하지 못했다.
- 다음 작업 제안: 사용자가 브라우저에서 `/main/charts`에 접속해 차트 표시를 확인한다.

- 항목: OpenAI GPT 필터 실제 성공 검증
- 이유: OpenAI quota 부족으로 filter limit 1 실제 호출이 실패 처리됐다.
- 다음 작업 제안: OpenAI billing/quota 확인 후 filter limit 1부터 재검증한다.

## 11. 확인 필요 항목

- 항목: 실제 수집 기준일
- 확인이 필요한 이유: 당일 또는 미래 날짜는 빈 데이터일 수 있다.
- 제안: 마지막 완료 영업일 기준으로 실행한다.

- 항목: 후속 영업일 수집 기준
- 확인이 필요한 이유: 동일 기준일 update 경로와 중복 방지는 검증 완료됐고, 다음에는 운영 기준일 선정이 필요하다.
- 제안: 마지막 완료 영업일 기준으로 정기 수집을 실행한다.

## 12. 다음 단계 제안

- 다음 단계 1: 후속 영업일 기준 KRX 실제 수집 실행
- 다음 단계 2: 차트 기간 필터와 종목 검색 UX 보완
- 다음 단계 3: MA20/60/120, RSI, MACD 계산 구조 구현 검토

## 13. 최종 완료 선언

모든 지시 내용 작업 완료 여부:

- [x] 완료
- [ ] 일부 미완료

최종 메시지:

“KRX 가격 데이터 수집 구조 작업 완료했습니다. DEVELOPMENT_REPORT.md를 확인해 주세요.”
