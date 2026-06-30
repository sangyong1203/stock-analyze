# Codex 다음 작업 지시 프롬프트 v1.8

## 0. 작업 목표

이전 작업 컨텍스트를 유지하고 이어서 진행한다.

이번 작업은 **차트 기술지표 계산 구조 구현**이다.

목표:

1. `stock_prices`의 일봉 데이터를 기반으로 MA20 / MA60 / MA120을 계산한다.
2. RSI를 계산한다.
3. MACD를 계산한다.
4. 차트 OHLCV API에 지표 데이터를 포함하거나 별도 indicators API를 구현한다.
5. Frontend 차트 화면에서 이동평균선, RSI, MACD를 표시한다.
6. 새 DB 테이블은 만들지 않는다.
7. 계산 결과는 우선 실시간 계산 방식으로 처리한다.

---

## 1. 작업 전 확인 사항

직전 `DEVELOPMENT_REPORT.md`의 완료/미완료/확인 필요 항목만 확인한다.

이미 읽은 기준 문서를 반복해서 다시 읽지 않는다.

이번 작업에서 필요한 기존 구조만 확인한다.

```text
backend/app/domains/charts/
backend/app/domains/prices/
frontend/src/pages/main/charts/
```

새 테이블과 새 마이그레이션은 만들지 않는다.

---

## 2. Backend 작업 범위

대상:

```text
backend/app/domains/charts/
```

필요 시 다음 구조를 추가한다.

```text
backend/app/domains/charts/indicators.py
backend/app/domains/charts/service.py
backend/app/domains/charts/router.py
```

구현 지표:

```text
MA20
MA60
MA120
RSI14
MACD
MACD signal
MACD histogram
```

---

## 3. 계산 기준

### 3.1 이동평균선

종가 기준 단순 이동평균으로 계산한다.

```text
MA20 = 최근 20개 close 평균
MA60 = 최근 60개 close 평균
MA120 = 최근 120개 close 평균
```

데이터 개수가 부족하면 해당 값은 null로 반환한다.

### 3.2 RSI

기본값은 14일 RSI로 계산한다.

```text
period = 14
상승분 평균 / 하락분 평균 기준
```

초기 데이터가 부족하면 null로 반환한다.

### 3.3 MACD

기본값:

```text
fast = 12
slow = 26
signal = 9
```

계산 항목:

```text
ema12
ema26
macd = ema12 - ema26
signal = macd의 9일 EMA
histogram = macd - signal
```

초기 데이터가 부족하면 null로 반환한다.

---

## 4. API 구현

기존 OHLCV API를 보완한다.

```text
GET /api/charts/stocks/{stock_id}/ohlcv
```

응답에 다음 필드를 추가한다.

```text
ma20
ma60
ma120
rsi14
macd
macd_signal
macd_histogram
```

또는 구조상 더 적합하면 별도 API를 추가한다.

```text
GET /api/charts/stocks/{stock_id}/indicators
```

단, Frontend에서 사용하기 쉬운 구조로 정리한다.

---

## 5. Frontend 작업 범위

대상:

```text
frontend/src/pages/main/charts/
```

구현 항목:

1. 기존 candlestick 차트에 MA20 / MA60 / MA120 line 표시
2. 지표 표시 on/off 옵션 추가
3. RSI 차트 영역 추가
4. MACD 차트 영역 추가
5. 데이터 부족 시 빈 값 처리
6. 차트 로딩/오류/데이터 없음 상태 유지

주의:

- ECharts 기준으로 구현한다.
- 지나치게 복잡한 전문 트레이딩 UI는 만들지 않는다.
- 이번 단계는 “지표가 정확히 계산되고 화면에 표시되는 것”을 우선한다.

---

## 6. 테스트 항목

Backend:

```text
- python -m compileall app 성공
- /api/charts/stocks/{stock_id}/ohlcv 200 응답
- 삼성전자 stock_id 2 기준 지표 계산 확인
- 알테오젠 stock_id 202 기준 지표 계산 확인
- 데이터 부족 시 null 처리 확인
- 기존 가격 API regression 확인
```

Frontend:

```text
- 차트 화면 build 성공
- 종목 선택 후 candlestick 표시 유지
- MA20/60/120 표시 확인
- RSI 영역 표시 확인
- MACD 영역 표시 확인
- npm run build 성공
```

Regression:

```text
- /health
- /api/auth/status
- /api/prices/summary
- /api/prices/stocks/{stock_id}/latest
- /api/news/alerts/send/dry-run
```

---

## 7. 문서 갱신

작업 완료 후 다음 문서를 짧게 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 새 문서를 작성한다.

```text
docs/CHART_INDICATOR_REPORT.md
```

포함 내용:

```markdown
# CHART INDICATOR REPORT

## 1. 작업 개요

## 2. 구현한 지표

## 3. 계산 방식

## 4. API 변경 사항

## 5. Frontend 연결 결과

## 6. 테스트 결과

## 7. 확인 필요 항목

## 8. 다음 단계 제안
```

---

## 8. 완료 조건

```text
- MA20 / MA60 / MA120 계산 완료
- RSI14 계산 완료
- MACD 계산 완료
- 차트 API 응답에 지표 포함
- Frontend 차트 화면에 지표 표시
- Backend compile 성공
- Frontend build 성공
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 사용자에게 다음과 같이 보고한다.

```text
차트 기술지표 계산 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
