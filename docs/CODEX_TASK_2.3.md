# CODEX_TASK_2.3

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

CODEX_TASK_2.2에서 운영 전 DB 백업과 첫 운영 데이터 입력 가이드 작성은 완료됐습니다.

이번 작업은 **실제 초기 운영 데이터 입력 / 포트폴리오 검증 / 대시보드 확인**입니다.

## 목표

1. 사용자가 제공한 실제 보유 종목 데이터를 초기 BUY 거래로 입력한다.
2. 보유종목을 직접 조작하지 말고 기존 거래 입력 구조를 사용한다.
3. 입력 전 DB 백업을 한 번 더 생성한다.
4. 입력 후 funds / trades / holdings / portfolio / dashboard 정합성을 검증한다.
5. 새 기능, 새 테이블, 새 마이그레이션은 만들지 않는다.
6. 실제 Gmail 발송은 하지 않는다.

## 작업 전 확인

직전 문서만 확인한다.

```text
docs/DEVELOPMENT_REPORT.md
docs/OPERATION_READY_CHECKLIST.md
docs/FIRST_OPERATION_DATA_INPUT_GUIDE.md
docs/MVP_COMPLETION_REPORT.md
```

기준 문서를 반복해서 다시 읽지 않는다.

## 1. DB 백업

실제 데이터 입력 전 현재 DB를 백업한다.

```text
backup filename:
storage/backups/stock_analyze_before_initial_holdings_input_YYYYMMDD_HHMMSS.db
```

확인:

```text
- source DB: backend/stock_analyze.db
- backup file exists
- backup file size > 0
- source DB size and backup DB size are reasonable
```

## 2. 입력 기준

이번 데이터는 사용자가 며칠 전 작성한 보유 현황입니다.

계산 기준:

```text
매입원금 = 현재금액 - 손익금액
평단가 = 매입원금 / 보유주식수
```

보유종목 테이블을 직접 수정하지 말고, 아래 데이터를 **초기 BUY 거래**로 입력하세요.

자금 풀 이름:

```text
기본 투자계좌
```

입금액:

```text
11,231,348
```

주의:

```text
- 이 입금액은 제공 데이터 기준 매입원금 합계입니다.
- 현금 잔고는 제공되지 않았으므로 0원으로 간주합니다.
- 거래 입력 시 소수점 평단가를 DB가 지원하면 소수점 그대로 사용합니다.
- DB/API가 정수 가격만 지원하면 반올림 가격을 사용하고 rounding 차이를 DEVELOPMENT_REPORT.md에 기록합니다.
```

## 3. 입력 데이터

가능하면 `exact_average_price`를 사용하세요.
정수만 가능하면 `rounded_average_price`를 사용하세요.

```csv
stock_name,stock_code,quantity,current_value,profit_loss,cost_amount,exact_average_price,rounded_average_price
RISE 미국나스닥100,368590,95,3146400,1027182,2119218,22307.5578947368,22308
삼성SDI,006400,5,2242500,-742350,2984850,596970,596970
ACE KRX금현물,411060,50,1356250,-230330,1586580,31731.6,31732
RISE 글로벌원자력,442320,25,1018250,-123865,1142115,45684.6,45685
두산에너빌리티,034020,10,804000,-248150,1052150,105215,105215
RISE 2차전지액티브,422420,90,597150,-222860,820010,9111.2222222222,9111
삼성E&A,028050,10,403500,-154590,558090,55809,55809
NAVER,035420,2,384200,-128800,513000,256500,256500
KODEX AI전력핵심설비,487240,10,368950,-86385,455335,45533.5,45534
```

중요:

```text
KODEX AI전력핵심설비 코드는 487240입니다.
487230을 사용하지 마세요.
```

## 4. 종목 매칭 확인

입력 전 stocks 테이블/API에서 종목코드가 존재하는지 확인한다.

확인 대상:

```text
368590
006400
411060
442320
034020
422420
028050
035420
487240
```

처리 기준:

```text
- 종목코드가 있으면 해당 stock_id를 사용한다.
- 종목명이 약간 다르면 stock_code를 우선한다.
- 종목코드가 없으면 임의 생성하지 말고 확인 필요 항목에 기록한다.
- 없는 종목 때문에 전체 입력이 막히면 입력 가능한 종목만 입력하지 말고, 먼저 보고서에 누락 종목을 기록하고 중단한다.
```

## 5. 입력 순서

```text
1. DB 백업 생성
2. 기존 fund pool 확인
3. "기본 투자계좌" fund pool이 없으면 생성
4. 초기 입금 11,231,348원 등록
5. 위 9개 종목을 초기 BUY 거래로 입력
6. holdings 자동 반영 확인
7. portfolio summary 확인
8. dashboard summary 확인
9. trades 목록 확인
```

거래일:

```text
2026-07-03
```

거래 메모:

```text
초기 보유 종목 등록 - 사용자 제공 평가금액/손익 기준 역산 평단가
```

## 6. 정합성 검증

입력 후 아래를 확인한다.

```text
/api/funds/summary
/api/trades
/api/holdings/summary
/api/portfolio/summary
/api/dashboard/summary
```

검증 기준:

```text
- funds.active_pool_count >= 1
- trades row count가 9건 증가
- holdings.holding_count = 9
- 각 종목 quantity가 입력 수량과 일치
- average_price가 계산 평단가와 일치 또는 반올림 기준으로 근접
- portfolio total_asset_value가 정상 계산
- dashboard에 portfolio 값 반영
```

## 7. 브라우저 확인

가능하면 Codex in-app browser로 확인한다.

```text
/portfolio
/trades
/dashboard
```

확인:

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

브라우저 timeout이 발생하면 API 검증 결과를 우선 기록하고, 브라우저 확인 미완료로 분리한다.

## 8. 금지 사항

```text
- 보유종목 holdings 테이블 직접 수정 금지
- 사용자가 제공하지 않은 종목/수량/금액 임의 입력 금지
- 실제 Gmail 발송 금지
- 알림 실제 발송 API 실행 금지
- 운영 DB 삭제 금지
- 운영 DB 초기화 금지
- 새 기능 추가 금지
- 새 테이블 생성 금지
- 새 마이그레이션 생성 금지
```

## 9. 문서 갱신

작업 완료 후 아래 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 작성:

```text
docs/INITIAL_PORTFOLIO_INPUT_REPORT.md
```

포함 내용:

```markdown
# INITIAL PORTFOLIO INPUT REPORT

## 1. 작업 개요

## 2. 백업 결과

## 3. 입력 데이터

## 4. 종목 코드 매칭 결과

## 5. 자금 풀 / 입금 결과

## 6. 거래 입력 결과

## 7. holdings 검증 결과

## 8. portfolio 검증 결과

## 9. dashboard 검증 결과

## 10. 반올림 오차 여부

## 11. 보류 / 확인 필요 항목
```

## 10. 완료 보고

작업 완료 후 다음과 같이 보고하세요.

```text
CODEX_TASK_2.3 실제 초기 운영 데이터 입력 작업 완료했습니다.
DEVELOPMENT_REPORT.md와 INITIAL_PORTFOLIO_INPUT_REPORT.md를 확인해 주세요.
```
