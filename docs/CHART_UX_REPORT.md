# CHART UX REPORT

## 1. 작업 개요

- 작업: 차트 기간 필터 및 종목 검색 UX 개선
- 대상 화면: `frontend/src/pages/main/charts/ChartsPage.vue`
- 대상 API: `/api/charts/stocks/{stock_id}/ohlcv`
- DB 변경: 없음
- 마이그레이션: 없음

## 2. 구현 결과

- 차트 기간 선택 추가: 1개월, 3개월, 6개월, 1년, 직접 선택
- 기간 선택에 따라 `limit` 또는 `date_from/date_to` API 파라미터 사용
- 기본 기간은 6개월이며 최소 130개 내외 데이터 조회를 우선함
- 종목명/종목코드 원격 검색 UI 추가
- KOSPI/KOSDAQ 시장 필터 추가
- 선택 종목의 시장, 종목명, 종목코드 표시
- MA20, MA60, MA120 개별 on/off 추가
- RSI, MACD on/off 추가
- 로딩, 오류, 빈 데이터 상태 표시 개선
- 실제 KRX 데이터 기반 SVG 차트 표시

## 3. 검증 결과

| 항목 | 결과 |
|---|---|
| 삼성전자 `stock_id=2` 기본 차트 | 정상, 128건 표시 |
| 알테오젠 `stock_id=202` API 조회 | 정상 |
| 1개월 기간 | 정상, 30건 |
| 3개월 기간 | 정상, 70건 |
| 6개월 기간 | 정상, 128건 |
| 1년 기간 | 정상, 저장 데이터 기준 128건 |
| MA120 토글 | 정상, polyline 7개에서 6개로 감소 확인 |
| 종목코드 검색 `005930` | 정상 |
| 종목코드 검색 `196170` | 정상 |
| 브라우저 차트 렌더링 | 정상, SVG 표시 및 렌더 오류 없음 |

## 4. 실행 검증

| 항목 | 결과 |
|---|---|
| Backend compile | 성공 |
| Frontend build | 성공 |
| `/health` | 200 |
| `/api/auth/status` | 200 |
| `/api/prices/summary` | 200 |
| `/api/charts/stocks/2/ohlcv?limit=130` | 200 |
| `/api/news/alerts/send/dry-run` | 200 |

## 5. 확인 필요 항목

- 항목: ECharts 렌더러 재적용 여부
- 관련 문서: `docs/CODEX_TASK_1.10.md`, `AGENTS.md`
- 애매한 이유: ECharts line/bar/candlestick 렌더링 중 coordinateSystem 오류가 발생해 화면 오류가 남았음
- 가능한 선택지: SVG 렌더러 유지, ECharts core 등록/옵션 추가 재조사, vue-echarts 도입 검토
- 추천안: MVP UX 검증은 현재 SVG 렌더러로 유지하고, 별도 작업에서 ECharts 재적용을 검토
- 현재 구현 여부: SVG 렌더러로 대체

- 항목: 종목명 검색 인코딩
- 관련 문서: `docs/CODEX_TASK_1.10.md`
- 애매한 이유: 일부 DB 종목명이 깨진 문자열로 저장되어 한글 종목명 검색이 실패할 수 있음
- 가능한 선택지: KRX 수집 파서 인코딩 재검토, stocks 종목명 재정비, 종목코드 검색 우선 사용
- 추천안: 다음 데이터 정합성 작업에서 종목명 인코딩을 재검증
- 현재 구현 여부: 종목코드 검색은 정상, 종목명 검색은 확인 필요

