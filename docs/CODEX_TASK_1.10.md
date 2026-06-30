# CODEX_TASK_1.10

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

KRX 다중 기준일 수집은 완료됐고, 삼성전자/알테오젠 기준 OHLCV 128건 응답까지 확인됐습니다.

이번 작업은 **차트 기간 필터 + 종목 검색 UX 보완**입니다.

## 작업 목표

1. 차트 화면에서 기간 선택을 쉽게 한다.
2. 종목 검색/선택 UX를 개선한다.
3. MA/RSI/MACD 표시 옵션을 정리한다.
4. 실제 KRX OHLCV 데이터가 차트에 안정적으로 표시되게 한다.
5. 새 DB 테이블과 마이그레이션은 만들지 않는다.

## 작업 항목

대상:

```text
frontend/src/pages/main/charts/
backend/app/domains/charts/
```

구현 항목:

1. 차트 기간 선택 옵션 추가

```text
1개월
3개월
6개월
1년
직접 선택
```

2. 기간 옵션에 따라 OHLCV API 요청 파라미터를 조정한다.

```text
limit 또는 date_from/date_to 사용
```

3. 기본 조회 기간은 지표 확인이 가능하도록 최소 130개 이상 데이터가 조회되게 한다.

4. 종목 검색 UX를 개선한다.

```text
- 종목명 검색
- 종목코드 검색
- KOSPI/KOSDAQ 구분 표시
- 선택된 종목명/코드 표시
```

5. MA 표시 옵션을 정리한다.

```text
MA20 on/off
MA60 on/off
MA120 on/off
```

6. 보조지표 표시 옵션을 정리한다.

```text
RSI on/off
MACD on/off
```

7. 데이터 부족/데이터 없음/로딩/오류 상태를 정리한다.

8. 차트 화면에서 실제 지표값이 깨지지 않고 표시되는지 확인한다.

9. Backend API가 추가 보완이 필요하면 최소 범위에서만 수정한다.

10. `DEVELOPMENT_REPORT.md`를 짧게 갱신한다.

필요 시 `CHART_UX_REPORT.md`를 작성한다.

## 검증 항목

1. 삼성전자 `stock_id=2` 차트 조회 확인
2. 알테오젠 `stock_id=202` 차트 조회 확인
3. 1개월/3개월/6개월/1년 기간 선택 확인
4. MA20/60/120 표시 on/off 확인
5. RSI 표시 on/off 확인
6. MACD 표시 on/off 확인
7. 종목명/종목코드 검색 확인
8. 데이터 없음 상태 확인
9. Backend compile 성공
10. Frontend build 성공

Regression:

```text
/health
/api/auth/status
/api/prices/summary
/api/charts/stocks/2/ohlcv?limit=130
/api/news/alerts/send/dry-run
```

## 주의

- 기준 문서를 반복해서 다시 읽지 않는다.
- 새 DB 테이블은 만들지 않는다.
- 새 마이그레이션은 만들지 않는다.
- 전문 트레이딩 차트처럼 과도하게 복잡하게 만들지 않는다.
- 이번 단계는 MVP 차트 사용성 마무리가 목적이다.

작업 완료 후 다음과 같이 보고하세요.

```text
차트 기간 필터와 종목 검색 UX 보완 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
