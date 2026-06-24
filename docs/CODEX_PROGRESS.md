# CODEX PROGRESS

## 현재 작업 상태

- 현재 단계: CODEX_TASK_1.7 KRX 가격 데이터 수집 구조 완료
- 마지막 작업 시간: 2026-06-24
- 전체 진행률: 100%
- 현재 작업 중인 파일: backend/app/external/krx/, backend/app/domains/prices/, backend/app/domains/charts/, frontend/src/pages/main/stocks/, frontend/src/pages/main/charts/, docs/

## 완료한 작업

- [x] KRX 환경설정 추가
  - 설명: `KRX_API_BASE_URL`, `KRX_AUTH_KEY` 설정을 추가했다.
  - 관련 파일: backend/app/core/config.py, backend/.env.example

- [x] KRX daily price client 구현
  - 설명: KOSPI `/sto/stk_bydd_trd`, KOSDAQ `/sto/ksq_bydd_trd` POST 호출, 인증 header, timeout, JSON 응답 검증, 숫자/날짜/종목코드 정규화 구조를 구현했다.
  - 관련 파일: backend/app/external/krx/client.py, backend/app/external/krx/parser.py, backend/app/external/krx/types.py

- [x] stock_prices upsert 구현
  - 설명: `stock_id + date + timeframe` 기준으로 insert/update하고, 신규 종목은 `stocks`에 기본 생성되도록 구현했다.
  - 관련 파일: backend/app/domains/prices/repository.py, backend/app/domains/prices/service.py

- [x] stocks 최신 가격 갱신 구현
  - 설명: KRX 일봉 수집값 기준으로 `stocks.current_price`, `stocks.change_rate`, `stocks.market_cap`, `updated_at`을 갱신한다.
  - 관련 파일: backend/app/domains/prices/service.py

- [x] 가격 조회 API 구현
  - 설명: KRX 수집 실행, 가격 요약, 종목별 가격 목록, 종목 최신 가격, 시장별 최신 가격 API를 구현했다.
  - 관련 파일: backend/app/domains/prices/router.py, backend/app/domains/prices/schemas.py, backend/app/main.py

- [x] 차트 OHLCV API 구현
  - 설명: `stock_prices`를 기반으로 ECharts에서 사용 가능한 일봉 OHLCV 응답 API를 구현했다.
  - 관련 파일: backend/app/domains/charts/router.py, backend/app/domains/charts/service.py, backend/app/domains/charts/repository.py, backend/app/domains/charts/schemas.py

- [x] 종목 화면 가격 수집 연결
  - 설명: 종목 화면에 KRX 가격 수집 버튼을 추가하고 수집 후 목록 refresh가 가능하도록 연결했다.
  - 관련 파일: frontend/src/pages/main/stocks/StocksPage.vue, frontend/src/pages/main/stocks/service/prices.api.ts

- [x] 차트 화면 OHLCV 연결
  - 설명: 종목 선택, 일봉 OHLCV 조회, candlestick 차트, 거래량 bar, 데이터 없음 상태를 구현했다.
  - 관련 파일: frontend/src/pages/main/charts/ChartsPage.vue, frontend/src/pages/main/charts/service/charts.api.ts, frontend/src/pages/main/charts/service/charts.types.ts

- [x] 검증 완료
  - 설명: Backend compile, Frontend build, 가격 summary API, KRX dry-run 401 응답 처리, mock KRX insert/update/latest/chart 검증을 완료했다.
  - 관련 파일: backend/, frontend/

- [x] KRX 가격 수집 리포트 작성
  - 설명: API, client 구조, 필드 매핑, 저장 방식, 최신값 갱신 방식, 테스트 결과, 확인 필요 항목을 정리했다.
  - 관련 파일: docs/KRX_PRICE_COLLECTION_REPORT.md

## 진행 중인 작업

- [x] CODEX_TASK_1.7 작업 완료
  - 현재 상태: 구현 및 검증 완료
  - 남은 작업: `KRX_AUTH_KEY` 발급/설정 후 실제 KRX 수집 재검증

## 남은 작업

- [ ] KOSPI/KOSDAQ 마지막 완료 영업일 기준 실제 저장 실행
- [ ] OpenAI quota/billing 확인 후 GPT 필터 limit 1 재검증
- [ ] 차트 고급 지표(MA, RSI, MACD)는 후속 작업에서 검토

## 막힌 항목

- 항목: 없음
- 원인: 없음
- 필요한 확인: 없음

## 생성한 파일

- 파일 경로: backend/app/external/krx/types.py
- 설명: KRX 일봉 가격 타입
- 파일 경로: backend/app/external/krx/parser.py
- 설명: KRX 응답 파서 및 숫자/날짜 정규화
- 파일 경로: backend/app/domains/prices/router.py
- 설명: 가격 수집/조회 API 라우터
- 파일 경로: frontend/src/pages/main/stocks/service/prices.api.ts
- 설명: Frontend KRX 가격 수집 API client
- 파일 경로: docs/KRX_PRICE_COLLECTION_REPORT.md
- 설명: KRX 가격 데이터 수집 구조 리포트

## 수정한 파일

- 파일 경로: backend/app/core/config.py
- 수정 내용: KRX 환경변수 추가
- 파일 경로: backend/.env.example
- 수정 내용: KRX 환경변수 예시 추가
- 파일 경로: backend/app/external/krx/client.py
- 수정 내용: KRX Open API client 구현
- 파일 경로: backend/app/domains/prices/
- 수정 내용: 가격 수집, upsert, 조회 API 구현
- 파일 경로: backend/app/domains/charts/
- 수정 내용: OHLCV API 구현
- 파일 경로: backend/app/main.py
- 수정 내용: prices router 등록
- 파일 경로: frontend/src/pages/main/stocks/StocksPage.vue
- 수정 내용: 가격 컬럼 표시 유지 및 KRX 가격 수집 버튼 추가
- 파일 경로: frontend/src/pages/main/charts/
- 수정 내용: 종목 선택 및 ECharts candlestick 연결

## 확인 필요 항목

- 항목: KRX 인증키 및 KOSPI 조회
- 이유: `KRX_AUTH_KEY` 로드와 KOSPI 과거 영업일 dry-run 조회는 성공했다.
- 제안: KOSPI는 마지막 완료 영업일 기준으로 실제 수집을 실행한다.

- 항목: KOSDAQ endpoint
- 이유: `/sto/ksq_bydd_trd` dry-run이 `20250624` 기준 1795건으로 정상 확인됐다.
- 제안: 해당 endpoint를 유지한다.
