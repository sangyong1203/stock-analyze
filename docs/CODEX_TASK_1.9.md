# CODEX_TASK_1.9

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

차트 기술지표 계산 구조는 완료됐지만, 실제 저장된 가격 데이터가 1거래일뿐이라 MA/RSI/MACD 값이 null로 나오는 상태입니다.

이번 작업은 **KRX 가격 데이터를 여러 기준일로 확장 수집**하는 것입니다.

## 작업 항목

1. 기존 `/api/prices/collect/krx/daily` 구조를 유지한다.
2. 새 테이블과 마이그레이션은 만들지 않는다.
3. 기간 수집 API를 추가한다.

권장 API:

```text
POST /api/prices/collect/krx/range
```

요청 예시:

```json
{
  "date_from": "20250101",
  "date_to": "20250624",
  "markets": ["KOSPI", "KOSDAQ"],
  "dry_run": false,
  "skip_empty": true
}
```

## 구현 기준

1. `date_from ~ date_to` 범위를 일자별로 순회한다.
2. KRX 응답이 빈 배열이면 휴장일/데이터 없음으로 보고 skip 처리한다.
3. 각 영업일 데이터는 기존 daily 저장 로직을 재사용한다.
4. `stock_prices`는 기존 기준대로 `stock_id + date + timeframe` 기준 upsert한다.
5. 중복 row를 만들지 않는다.
6. 수집 결과를 날짜별로 요약 반환한다.
7. 전체 `fetched / inserted / updated / skipped_empty_dates / error_count`를 반환한다.
8. 너무 많은 날짜 요청을 막기 위해 1회 최대 220일 정도 제한을 둔다.
9. `KRX_AUTH_KEY` 값은 로그나 문서에 기록하지 않는다.
10. 과거 날짜를 재수집해도 `stocks.current_price`, `change_rate`, `market_cap`이 더 최신 데이터에서 과거 데이터로 덮이지 않게 한다.

## 검증 항목

1. 최근 130거래일 이상 수집한다.
2. `/api/prices/summary`의 `total_price_rows` 증가를 확인한다.
3. 삼성전자 `stock_id=2`의 `/api/charts/stocks/2/ohlcv?limit=130`을 확인한다.
4. MA20 / MA60 / RSI14 / MACD 값이 null이 아닌 구간이 생기는지 확인한다.
5. 알테오젠 `stock_id=202`도 동일하게 확인한다.
6. 차트 화면에서 MA/RSI/MACD 표시를 확인한다.
7. 동일 기간 재수집 시 중복 row 없이 update 되는지 확인한다.
8. Backend compile 성공을 확인한다.
9. Frontend build 성공을 확인한다.
10. `DEVELOPMENT_REPORT.md`를 짧게 갱신한다.
11. 필요 시 `KRX_RANGE_COLLECTION_REPORT.md`를 작성한다.

## 주의

- 기준 문서를 반복해서 다시 읽지 않는다.
- 새 DB 테이블은 만들지 않는다.
- 새 마이그레이션은 만들지 않는다.
- 기존 daily 수집 로직을 최대한 재사용한다.

작업 완료 후 다음과 같이 보고하세요.

```text
KRX 다중 기준일 가격 데이터 수집 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
