# Codex 다음 작업 지시 프롬프트 v1.7

## 0. 작업 목표

이전 작업 컨텍스트를 유지하고 이어서 진행한다.

이미 읽은 기준 문서를 반복해서 다시 읽지 않는다.

이번 작업은 **KRX 가격 데이터 수집 구조 구현**이다.

목표:

1. KRX 일별 시세 수집 client를 구현한다.
2. KOSPI / KOSDAQ 일별 데이터를 수집해 `stock_prices`에 저장한다.
3. 최신 가격, 등락률, 시가총액을 `stocks`에 반영한다.
4. 가격 데이터 조회 API를 구현한다.
5. 종목 화면과 차트 화면에서 가격 데이터를 조회할 수 있게 연결한다.
6. 수집 결과와 오류는 기존 `system_logs` 또는 응답 결과에 기록한다.
7. 새 DB 테이블은 만들지 않는다.

---

## 1. 작업 전 확인 사항

직전 `DEVELOPMENT_REPORT.md`의 완료/미완료/확인 필요 항목만 확인하고 이어서 진행한다.

문서가 새로 수정되지 않았다면 아래 기준 문서를 다시 반복해서 읽지 않는다.

```text
docs/INVESTMENT_SYSTEM_PLAN_v1.2.md
docs/MVP_DB_SCHEMA_v1.2.md
docs/SCHEMA_VALIDATION_REPORT.md
```

DB 구조 확인이 필요할 때만 `docs/MVP_DB_SCHEMA_v1.2.md`에서 `stocks`, `stock_prices`, `price_snapshots`, `system_logs` 테이블 정의를 확인한다.

---

## 2. 작업 범위

주요 작업 대상:

```text
backend/app/external/krx/
backend/app/domains/prices/
backend/app/domains/stocks/
backend/app/domains/charts/
frontend/src/pages/main/stocks/
frontend/src/pages/main/charts/
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 아래 파일도 수정한다.

```text
backend/app/main.py
backend/app/core/config.py
backend/.env.example
frontend/src/router/routes.ts
```

새 테이블과 새 마이그레이션은 만들지 않는다.

---

## 3. KRX API 설정

### 3.1 환경변수

다음 환경변수를 추가한다.

```env
KRX_API_BASE_URL=https://data-dbg.krx.co.kr/svc/apis
KRX_AUTH_KEY=
```

`KRX_AUTH_KEY`가 필요한 구조라면 사용한다.
현재 KRX 요청이 인증 없이 동작하는 구조라면 `KRX_AUTH_KEY`는 선택값으로 처리한다.

`.env.example`에도 예시를 추가한다.

### 3.2 기본 수집 endpoint

KOSPI 일별 거래 정보:

```text
POST /sto/stk_bydd_trd
```

요청 body:

```json
{
  "basDd": "YYYYMMDD"
}
```

KOSDAQ endpoint는 현재 프로젝트 또는 KRX 문서 기준으로 확인 가능한 값을 사용한다.

예상 endpoint:

```text
POST /sto/ksq_bydd_trd
```

KOSDAQ endpoint가 확실하지 않으면 임의 확정하지 말고 `확인 필요 항목`에 기록한다.

---

## 4. KRX client 구현

### 4.1 위치

```text
backend/app/external/krx/
```

권장 파일:

```text
backend/app/external/krx/client.py
backend/app/external/krx/types.py
backend/app/external/krx/parser.py
```

### 4.2 구현 기능

```text
- KRX API POST 요청
- timeout 처리
- 인증 header 처리
- 응답 status 검증
- KOSPI 일별 데이터 수집
- KOSDAQ 일별 데이터 수집
- 숫자 문자열 정규화
- 종목코드 6자리 정규화
- 빈 값/하이픈/콤마 처리
```

### 4.3 KRX 응답 필드 매핑

KRX 응답의 주요 필드를 아래처럼 매핑한다.

```text
BAS_DD        -> date
ISU_CD        -> stock code
ISU_NM        -> stock name
MKT_NM        -> market
TDD_OPNPRC    -> open
TDD_HGPRC     -> high
TDD_LWPRC     -> low
TDD_CLSPRC    -> close
CMPPREVDD_PRC -> change_price
FLUC_RT       -> change_rate
ACC_TRDVOL    -> volume
ACC_TRDVAL    -> trade_value
MKTCAP        -> market_cap
LIST_SHRS     -> listed_shares
```

---

## 5. 가격 저장 로직

### 5.1 대상 테이블

```text
stocks
stock_prices
system_logs
```

`price_snapshots`는 이번 단계에서 필수로 사용하지 않는다.

`price_snapshots`는 거래, 알림, 현재가 스냅샷 같은 이벤트성 가격 저장에 사용한다.
KRX 일별 과거 데이터는 `stock_prices`에 저장한다.

### 5.2 stock_prices 저장

`stock_prices`에는 다음 기준으로 저장한다.

```text
stock_id
market
date
timeframe = "daily"
open
high
low
close
volume
trade_value
market_cap
listed_shares
change_price
change_rate
source = "krx"
created_at
```

중복 기준:

```text
stock_id + date + timeframe
```

이미 존재하면 update한다.
없으면 insert한다.

### 5.3 stocks 최신값 갱신

수집 기준일이 해당 종목의 최신 거래일이면 `stocks`를 갱신한다.

```text
current_price = close
change_rate = change_rate
market_cap = market_cap
updated_at = now
```

### 5.4 stocks 자동 생성

KRX 데이터에 있는 종목이 `stocks`에 없으면 기본 정보를 생성한다.

```text
code
name
market
market_cap
current_price
change_rate
is_active = true
```

단, sector/industry는 알 수 없으면 비워둔다.

---

## 6. 가격 수집 API 구현

대상 도메인:

```text
backend/app/domains/prices/
```

구현 API:

```text
POST /api/prices/collect/krx/daily
GET  /api/prices/summary
GET  /api/prices/stocks/{stock_id}
GET  /api/prices/stocks/{stock_id}/latest
GET  /api/prices/markets/{market}/latest
```

### 6.1 POST /api/prices/collect/krx/daily

요청 예시:

```json
{
  "bas_date": "20260624",
  "markets": ["KOSPI", "KOSDAQ"],
  "dry_run": false
}
```

동작:

```text
1. 요청 bas_date 검증
2. markets 검증
3. KRX API 호출
4. 응답 파싱
5. stocks upsert
6. stock_prices upsert
7. stocks 최신값 갱신
8. 결과 통계 반환
9. 오류 발생 시 system_logs에 기록
```

응답 예시:

```json
{
  "bas_date": "20260624",
  "markets": ["KOSPI", "KOSDAQ"],
  "fetched_count": 0,
  "inserted_count": 0,
  "updated_count": 0,
  "stock_created_count": 0,
  "error_count": 0
}
```

### 6.2 GET /api/prices/summary

응답:

```text
- total_price_rows
- latest_price_date
- kospi_price_count
- kosdaq_price_count
- latest_updated_stocks_count
```

### 6.3 GET /api/prices/stocks/{stock_id}

필터:

```text
timeframe
date_from
date_to
limit
```

기본:

```text
timeframe = daily
limit = 240
```

### 6.4 GET /api/prices/stocks/{stock_id}/latest

해당 종목의 최신 가격 1건을 반환한다.

### 6.5 GET /api/prices/markets/{market}/latest

시장별 최신 가격 목록을 반환한다.

필터:

```text
market = KOSPI | KOSDAQ
limit
```

---

## 7. 차트 데이터 API 보완

대상 도메인:

```text
backend/app/domains/charts/
```

기존 chart API 골격이 있으면 가격 데이터를 실제 연결한다.

구현 API 또는 기존 API 보완:

```text
GET /api/charts/stocks/{stock_id}/ohlcv
```

지원 필터:

```text
timeframe = daily
date_from
date_to
limit
```

응답에는 ECharts candlestick에 바로 사용할 수 있는 데이터를 포함한다.

```text
date
open
high
low
close
volume
change_rate
```

이번 단계에서는 MA20/60/120, MACD, RSI 계산은 필수 구현하지 않는다.
다만 후속 구현을 고려해 service 구조를 분리한다.

---

## 8. Frontend 연결

### 8.1 종목 화면 보완

대상:

```text
frontend/src/pages/main/stocks/
```

보완 항목:

```text
- 종목 목록에 current_price, change_rate, market_cap 표시 확인
- 가격 최신 갱신 후 목록 refresh 가능하게 처리
- 필요 시 가격 수집 실행 버튼은 관리자성 기능으로 작게 배치
```

### 8.2 차트 화면 연결

대상:

```text
frontend/src/pages/main/charts/
```

구현 항목:

```text
- 종목 선택
- 일봉 OHLCV 조회
- ECharts candlestick 또는 기본 line/candlestick 표시
- 거래량 bar 표시
- date range 필터
- 데이터 없음 상태 표시
```

복잡한 차트 기능은 후속 작업으로 넘긴다.

이번 단계에서는 “KRX 수집 데이터가 차트에 표시되는 것”을 우선한다.

---

## 9. 테스트 항목

### 9.1 Backend 테스트

다음을 확인한다.

```text
- /api/prices/summary 200 응답
- /api/prices/collect/krx/daily dry_run=true 동작
- /api/prices/collect/krx/daily bas_date 1건 실제 수집 동작
- KOSPI 수집 성공
- KOSDAQ 수집은 endpoint 확인 가능 시 성공
- stock_prices insert/update 확인
- stocks current_price/change_rate/market_cap 갱신 확인
- 중복 수집 시 중복 row 생성 없이 update 확인
- /api/prices/stocks/{stock_id} 200 응답
- /api/prices/stocks/{stock_id}/latest 200 응답
- /api/charts/stocks/{stock_id}/ohlcv 200 응답
```

### 9.2 Frontend 테스트

다음을 확인한다.

```text
- 종목 화면 가격 컬럼 표시
- 차트 화면 종목 선택
- 차트 데이터 조회 성공
- 차트 표시 성공
- 데이터 없음 상태 표시
- npm run build 성공
```

### 9.3 Regression

기존 기능이 깨지지 않았는지 확인한다.

```text
- /health
- /api/auth/status
- 설정 API
- 종목 API
- 수집 종목 관리 API
- 뉴스 API
- GPT API dry-run
- 뉴스 알림 발송 dry-run
- Frontend build
```

---

## 10. 문서 갱신

작업 완료 후 다음 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 다음 문서를 새로 작성한다.

```text
docs/KRX_PRICE_COLLECTION_REPORT.md
```

`KRX_PRICE_COLLECTION_REPORT.md`에는 다음 내용을 기록한다.

```markdown
# KRX PRICE COLLECTION REPORT

## 1. 작업 개요

## 2. 구현한 API

## 3. KRX client 구조

## 4. KRX 응답 필드 매핑

## 5. stock_prices 저장 방식

## 6. stocks 최신값 갱신 방식

## 7. Frontend 연결 결과

## 8. 테스트 결과

## 9. 확인 필요 항목

## 10. 다음 단계 제안
```

---

## 11. 완료 조건

이번 작업 완료 조건은 다음이다.

```text
- KRX daily price client 구현
- KOSPI 일별 가격 수집 구현
- KOSDAQ 일별 가격 수집은 endpoint 확인 가능 시 구현
- stock_prices upsert 구현
- stocks 최신 가격/등락률/시가총액 갱신 구현
- 가격 조회 API 구현
- 차트 OHLCV API 구현
- 종목 화면 가격 표시 확인
- 차트 화면 가격 데이터 표시 확인
- Backend 테스트 통과
- Frontend build 통과
- CODEX_PROGRESS.md 갱신
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 사용자에게 다음과 같이 보고한다.

```text
KRX 가격 데이터 수집 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
