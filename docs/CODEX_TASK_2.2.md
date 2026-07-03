# CODEX_TASK_2.2

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

CODEX_TASK_2.1 운영 준비 상태 점검은 완료됐습니다.

이번 작업은 **첫 운영 데이터 입력 준비 / 자금 풀·보유 종목 입력 검증 / 초기 포트폴리오 확인**입니다.

## 목표

1. 실제 운영 데이터 입력 전에 DB 백업 절차를 검증한다.
2. 자금 풀, 입금, 보유 종목, 평균단가 입력 흐름을 점검한다.
3. 실제 운영 데이터는 사용자가 제공한 값이 있을 때만 입력한다.
4. 사용자가 제공하지 않은 금액/종목/수량/평균단가는 절대 임의 입력하지 않는다.
5. 입력 후 holdings, portfolio, dashboard 정합성을 확인한다.
6. 새 기능, 새 테이블, 새 마이그레이션은 만들지 않는다.
7. 실제 Gmail 발송은 하지 않는다.

## 작업 전 확인

직전 문서만 확인한다.

```text
docs/DEVELOPMENT_REPORT.md
docs/OPERATION_READY_CHECKLIST.md
docs/MVP_COMPLETION_REPORT.md
```

기준 문서를 반복해서 다시 읽지 않는다.

## 1. DB 백업 선행

실제 운영 데이터 입력 전 반드시 현재 SQLite DB를 백업한다.

백업 위치:

```text
storage/backups/
```

백업 파일명 예시:

```text
stock_analyze_before_first_operation_YYYYMMDD_HHMMSS.db
```

확인할 것:

```text
- 원본 DB 경로 확인
- 백업 파일 생성 확인
- 백업 파일 크기 0 아님 확인
- 백업 후 원본 DB 유지 확인
```

주의:

```text
- 운영 DB 삭제 금지
- 운영 DB 초기화 금지
- migration 실행 금지
- schema 변경 금지
```

## 2. 실제 운영 데이터 입력 여부 판단

사용자가 제공한 실제 데이터가 있는지 먼저 확인한다.

필수 입력 데이터:

```text
1. 자금 풀 이름
2. 총 입금액 또는 초기 현금
3. 보유 종목 코드
4. 보유 종목명
5. 보유 수량
6. 평균단가
7. 매수일 또는 기준일
```

실제 데이터가 없으면 DB에 실제 운영 데이터를 입력하지 않는다.

그 경우 아래 문서만 작성한다.

```text
docs/FIRST_OPERATION_DATA_INPUT_GUIDE.md
```

## 3. 입력 방식

실제 데이터가 제공된 경우에만 아래 순서로 입력한다.

```text
1. DB 백업
2. fund pool 생성
3. 초기 입금 등록
4. 보유 종목별 매수 거래 입력
5. holdings 자동 계산 확인
6. portfolio summary 확인
7. dashboard 반영 확인
8. alerts 화면에서 알림은 생성하지 않음
9. 실제 Gmail 발송 없음
```

## 4. 정합성 검증

입력 후 다음을 확인한다.

```text
- funds.active_pool_count >= 1
- funds.total_cash 계산 정상
- holdings.holding_count가 입력 종목 수와 일치
- holdings quantity 합계 정상
- average_price 정상
- portfolio.total_asset_value 정상
- portfolio.cash + holdings market_value 합산 정상
- dashboard summary에 portfolio 값 반영
```

검증 API:

```text
/api/funds/summary
/api/holdings/summary
/api/portfolio/summary
/api/dashboard/summary
/api/trades
```

## 5. 화면 확인

브라우저에서 아래 화면을 확인한다.

```text
/portfolio
/trades
/dashboard
```

확인 항목:

```text
- 자금 풀 표시
- 입금 내역 표시
- 거래 내역 표시
- 보유 종목 표시
- 손익 요약 표시
- dashboard KPI 반영
- 한글 깨짐 없음
- 콘솔 에러 없음
- 네트워크 실패 없음
```

## 6. 실제 데이터가 없을 경우 작성할 입력 가이드

실제 데이터가 제공되지 않았으면 `docs/FIRST_OPERATION_DATA_INPUT_GUIDE.md`를 작성한다.

구성:

```markdown
# FIRST OPERATION DATA INPUT GUIDE

## 1. 목적

## 2. 입력 전 백업 절차

## 3. 필요한 입력 데이터

## 4. 자금 풀 생성 기준

## 5. 초기 입금 입력 기준

## 6. 보유 종목 입력 방식

## 7. 평균단가 입력 기준

## 8. 과거 거래 입력 범위 결정 기준

## 9. 입력 후 확인할 화면

## 10. 입력 후 확인할 API

## 11. 주의사항
```

## 7. DEVELOPMENT_REPORT.md 갱신

이번 작업 결과만 짧게 정리한다.

포함 내용:

```text
- CODEX_TASK_2.2 완료
- DB 백업 수행 여부
- 실제 운영 데이터 입력 여부
- 입력한 경우 자금/보유/포트폴리오 요약
- 입력하지 않은 경우 FIRST_OPERATION_DATA_INPUT_GUIDE.md 작성
- 새 기능 / 새 테이블 / 새 마이그레이션 없음
- 실제 Gmail 발송 없음
```

## 검증

Backend:

```bash
cd backend
python -m compileall app
```

Frontend:

```bash
cd frontend
npm run build
```

Regression API:

```text
/health
/api/auth/status
/api/funds/summary
/api/holdings/summary
/api/portfolio/summary
/api/dashboard/summary
```

## 금지 사항

```text
- 사용자가 제공하지 않은 실제 투자 데이터를 임의 입력하지 않는다.
- 실제 Gmail 발송 금지
- 운영 DB 삭제 금지
- 운영 DB 초기화 금지
- 새 기능 추가 금지
- 새 테이블 생성 금지
- 새 마이그레이션 생성 금지
- 종목/수량/평균단가 임의 생성 금지
```

## 완료 보고

작업 완료 후 다음과 같이 보고하세요.

```text
CODEX_TASK_2.2 첫 운영 데이터 입력 준비 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
