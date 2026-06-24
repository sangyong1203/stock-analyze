# KRX PRICE COLLECTION REPORT

## 1. 작업 개요

- 작업 목표: KRX 일봉 가격 데이터를 수집해 `stock_prices`에 저장하고, `stocks` 최신 가격/등락률/시가총액을 갱신하는 구조를 구현했다.
- 신규 DB 테이블: 없음
- 사용 테이블: `stocks`, `stock_prices`, `system_logs`
- 기준 작업 문서: `docs/CODEX_TASK_1.7.md`

## 2. 구현한 API

| Method | Path | 설명 |
| ------ | ---- | ---- |
| POST | `/api/prices/collect/krx/daily` | KRX 일봉 가격 수집 및 저장 |
| GET | `/api/prices/summary` | 가격 데이터 요약 조회 |
| GET | `/api/prices/stocks/{stock_id}` | 종목별 가격 목록 조회 |
| GET | `/api/prices/stocks/{stock_id}/latest` | 종목 최신 가격 조회 |
| GET | `/api/prices/markets/{market}/latest` | 시장별 최신 가격 목록 조회 |
| GET | `/api/charts/stocks/{stock_id}/ohlcv` | 차트용 OHLCV 데이터 조회 |

## 3. KRX client 구조

- 위치: `backend/app/external/krx/`
- 주요 파일:
  - `client.py`: KRX API POST 호출
  - `parser.py`: 응답 row 파싱, 숫자/날짜/종목코드 정규화
  - `types.py`: `KrxDailyPrice` 타입
- 환경변수:
  - `KRX_API_BASE_URL=https://data-dbg.krx.co.kr/svc/apis`
  - `KRX_AUTH_KEY=`

## 4. KRX 응답 필드 매핑

| KRX 필드 | 내부 필드 |
| -------- | --------- |
| BAS_DD | date |
| ISU_CD | stock code |
| ISU_NM | stock name |
| MKT_NM | market |
| TDD_OPNPRC | open |
| TDD_HGPRC | high |
| TDD_LWPRC | low |
| TDD_CLSPRC | close |
| CMPPREVDD_PRC | change_price |
| FLUC_RT | change_rate |
| ACC_TRDVOL | volume |
| ACC_TRDVAL | trade_value |
| MKTCAP | market_cap |
| LIST_SHRS | listed_shares |

## 5. stock_prices 저장 방식

- 저장 기준: `stock_id + date + timeframe`
- `timeframe`: `daily`
- 기존 row가 있으면 update, 없으면 insert
- `source`: `krx`
- KRX row에 해당하는 종목이 `stocks`에 없으면 기본 종목 정보를 생성한다.

## 6. stocks 최신값 갱신 방식

수집 row 기준으로 다음 값을 갱신한다.

- `current_price = close`
- `change_rate = change_rate`
- `market_cap = market_cap`
- `updated_at = now`

## 7. Frontend 연결 결과

- 종목 화면: `KRX 가격 수집` 버튼 추가, 수집 후 종목 목록 refresh
- 차트 화면: 종목 선택, 일봉 OHLCV 조회, ECharts candlestick, 거래량 bar, 데이터 없음 상태 표시
- 상승/하락 색상: 상승 빨강, 하락 파랑 기준 적용

## 8. 테스트 결과

- Backend compile: `python -m compileall app` 성공
- Frontend build: `npm run build` 성공
- `/api/prices/summary`: 200 응답
- `/api/prices/collect/krx/daily` dry_run: `KRX_AUTH_KEY` 설정 후 KOSPI 과거 영업일 `20250624` 기준 962건 조회 확인
- `20260624` 기준 KOSPI 응답: `OutBlock_1` 빈 배열로 반환되어 데이터 없음 확인
- KOSDAQ dry_run: 권한 재신청 후 `20250624` 기준 1795건 조회 확인
- 실제 저장 검증: `20250624`, markets `["KOSPI", "KOSDAQ"]`, `dry_run=false` 실행 성공
- 실제 저장 결과: fetched 2757, inserted 2757, updated 0, stock_created 2410, error 0
- `/api/prices/summary`: total_price_rows 2757, latest_price_date 2025-06-24, KOSPI 962, KOSDAQ 1795
- 시장별 최신 가격 조회: `/api/prices/markets/KOSPI/latest`, `/api/prices/markets/KOSDAQ/latest` 200 응답
- 종목 최신 가격 확인: 삼성전자 stock_id 2, 알테오젠 stock_id 202 최신 가격 200 응답
- `stocks` 최신값 갱신 확인: 삼성전자 current_price 60500, change_rate 4.3100, market_cap 358138094281000; 알테오젠 current_price 390000, change_rate 2.6300, market_cap 20851337520000
- 차트 API 확인: `/api/charts/stocks/2/ohlcv?limit=20`, `/api/charts/stocks/202/ohlcv?limit=20` 200 응답 및 실제 KRX OHLCV 데이터 반환
- 차트 화면 확인: `/main/charts` route 200 응답, 화면이 사용하는 OHLCV API 정상 확인. 현재 세션에서 in-app browser가 제공되지 않아 시각 캔버스 직접 확인은 미수행
- 반복 수집 검증: 동일 기준일 `20250624`, markets `["KOSPI", "KOSDAQ"]`, `dry_run=false` 재실행 결과 fetched 2757, inserted 0, updated 2757, stock_created 0, error 0
- 중복 row 검증: `stock_id + date + timeframe` 중복 그룹 0건, total_price_rows 2757 유지
- 반복 수집 후 삼성전자/알테오젠 latest 및 OHLCV API 정상 유지
- mock KRX client 검증:
  - 최초 수집 insert 1건 성공
  - 반복 수집 update 1건 성공
  - 신규 stock 생성 성공
  - `stocks.current_price`, `change_rate`, `market_cap` 갱신 확인
  - `/api/prices/stocks/{stock_id}/latest` 200 응답
  - `/api/charts/stocks/{stock_id}/ohlcv` 200 응답
- mock 검증용 임시 종목/가격 데이터는 테스트 후 삭제 완료

## 9. 확인 필요 항목

- 항목: 차트 화면 시각 확인
- 이유: 현재 세션에서 in-app browser가 제공되지 않아 캔버스 렌더링을 직접 시각 확인하지 못했다.
- 제안: 실행 중인 frontend에서 `/main/charts` 접속 후 차트 표시를 확인한다.

- 항목: 후속 영업일 수집
- 이유: 동일 기준일 update 경로와 중복 방지는 검증 완료됐다.
- 제안: 다음 완료 영업일 데이터로 수집을 확장한다.

## 10. 다음 단계 제안

- 후속 영업일 기준 KRX 실제 수집 실행
- 수집된 가격 데이터를 기반으로 차트 기간 필터 UI 보완
- 후속 작업에서 MA20/60/120, RSI, MACD 계산 구조 검토
