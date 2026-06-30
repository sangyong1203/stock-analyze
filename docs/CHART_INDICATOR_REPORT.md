# CHART INDICATOR REPORT

## 1. 작업 개요

- 작업 목표: `stock_prices` 일봉 데이터를 기반으로 차트 기술지표를 실시간 계산하고 화면에 표시한다.
- 신규 DB 테이블: 없음
- 저장 방식: 계산 결과는 DB에 저장하지 않고 API 요청 시 계산한다.
- 기준 작업 문서: `docs/CODEX_TASK_1.8.md`

## 2. 구현한 지표

- MA20
- MA60
- MA120
- RSI14
- MACD
- MACD signal
- MACD histogram

## 3. 계산 방식

- 이동평균: close 기준 단순 이동평균
- RSI14: 최근 14개 변화분의 평균 상승폭/평균 하락폭 기준
- MACD: EMA12 - EMA26
- MACD signal: MACD의 EMA9
- MACD histogram: MACD - signal
- 데이터 개수가 부족하거나 close 값이 없으면 `null`을 반환한다.

## 4. API 변경 사항

`GET /api/charts/stocks/{stock_id}/ohlcv` 응답 item에 다음 필드를 추가했다.

```text
ma20
ma60
ma120
rsi14
macd
macd_signal
macd_histogram
```

## 5. Frontend 연결 결과

- 기존 candlestick 차트에 MA20/60/120 line series를 추가했다.
- RSI14 전용 차트 영역을 추가했다.
- MACD histogram, MACD line, signal line 차트 영역을 추가했다.
- MA/RSI/MACD 표시 on/off 옵션을 추가했다.
- 상승 빨강, 하락 파랑 기준을 유지했다.

## 6. 테스트 결과

- `python -m compileall app`: 성공
- 지표 계산 함수 검증: 130개 synthetic close 데이터 기준 MA/RSI/MACD 비-null 계산 확인
- `/api/charts/stocks/2/ohlcv?limit=130`: 200 응답, 지표 필드 포함 확인
- `/api/charts/stocks/202/ohlcv?limit=130`: 200 응답, 지표 필드 포함 확인
- 데이터 부족 처리: 현재 대표 종목은 일봉 1건이라 지표값이 `null`로 반환되는 것 확인
- Regression: `/health`, `/api/auth/status`, `/api/prices/summary`, `/api/prices/stocks/2/latest`, `/api/news/alerts/send/dry-run` 정상
- Frontend build: `npm run build` 성공

## 7. 확인 필요 항목

- 항목: 실제 비-null 지표 화면 표시
- 이유: 현재 저장된 대표 종목 가격 데이터가 1거래일뿐이라 MA/RSI/MACD는 `null`이 정상이다.
- 제안: 120거래일 이상 KRX 가격 데이터를 수집한 뒤 차트 화면에서 지표 line/영역을 시각 확인한다.

## 8. 다음 단계 제안

- 다중 기준일 KRX 가격 데이터 수집
- 차트 기간 필터 개선
- 지표 설정값(period) 사용자 조정 기능 검토
