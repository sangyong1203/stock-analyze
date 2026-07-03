# CODEX_TASK_2.4

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

CODEX_TASK_2.3은 필수 종목 중 ETF 5개가 stocks 테이블에 없어 입력 전에 정상 중단됐습니다.

사용자 결정:
ETF는 종목 마스터에 추가하지 않습니다.

이번 작업은 **ETF 제외 초기 포트폴리오 입력 / 일반 주식 4개 입력 / 정합성 검증**입니다.

## 목표

1. ETF 종목은 추가하지 않는다.
2. ETF 종목은 초기 포트폴리오에 입력하지 않는다.
3. 현재 stocks 테이블에 존재하는 일반 주식 4개만 초기 BUY 거래로 입력한다.
4. 입력 전 DB 백업을 생성한다.
5. 입력 후 funds / trades / holdings / portfolio / dashboard 정합성을 확인한다.
6. 새 기능, 새 테이블, 새 마이그레이션은 만들지 않는다.
7. 실제 Gmail 발송은 하지 않는다.

## 작업 전 확인

직전 문서만 확인한다.

```text id="aegzbh"
docs/DEVELOPMENT_REPORT.md
docs/INITIAL_PORTFOLIO_INPUT_REPORT.md
docs/FIRST_OPERATION_DATA_INPUT_GUIDE.md
```

기준 문서를 반복해서 다시 읽지 않는다.

## 1. DB 백업

입력 전 현재 DB를 백업한다.

```text id="p620yo"
backup filename:
storage/backups/stock_analyze_before_non_etf_initial_input_YYYYMMDD_HHMMSS.db
```

확인:

```text id="hz2sel"
- source DB: backend/stock_analyze.db
- backup file exists
- backup file size > 0
- source DB와 backup DB size 확인
```

## 2. ETF 제외 정책

아래 ETF는 입력하지 않는다.

```text id="bnw8g6"
368590 RISE 미국나스닥100
411060 ACE KRX금현물
442320 RISE 글로벌원자력
422420 RISE 2차전지액티브
487240 KODEX AI전력핵심설비
```

주의:

```text id="h76qg4"
- ETF 종목을 stocks 테이블에 추가하지 않는다.
- ETF 거래를 생성하지 않는다.
- ETF holdings를 직접 생성하지 않는다.
```

## 3. 입력 대상 데이터

아래 4개 종목만 초기 BUY 거래로 입력한다.

```csv id="jpkc66"
stock_name,stock_code,quantity,average_price,cost_amount
삼성SDI,006400,5,596970,2984850
두산에너빌리티,034020,10,105215,1052150
삼성E&A,028050,10,55809,558090
NAVER,035420,2,256500,513000
```

자금 풀 이름:

```text id="lvk6du"
기본 투자계좌
```

초기 입금액:

```text id="t8gxxu"
5108090
```

거래일:

```text id="lfws42"
2026-07-03
```

거래 메모:

```text id="r6kqti"
초기 보유 종목 등록 - ETF 제외, 일반 주식만 입력
```

## 4. 입력 순서

```text id="eusfv2"
1. DB 백업 생성
2. 기존 fund pool / trades / holdings 상태 확인
3. "기본 투자계좌" fund pool이 없으면 생성
4. 초기 입금 5,108,090원 등록
5. 일반 주식 4개를 BUY 거래로 입력
6. holdings 자동 반영 확인
7. portfolio summary 확인
8. dashboard summary 확인
9. trades 목록 확인
```

## 5. 정합성 검증

확인 API:

```text id="cnx8mj"
/api/funds/summary
/api/trades
/api/holdings/summary
/api/portfolio/summary
/api/dashboard/summary
```

검증 기준:

```text id="4h0iu0"
- funds.active_pool_count >= 1
- trades row count = 4
- holdings.holding_count = 4
- 삼성SDI quantity = 5
- 두산에너빌리티 quantity = 10
- 삼성E&A quantity = 10
- NAVER quantity = 2
- 각 average_price가 입력값과 일치
- ETF holdings는 없어야 함
- portfolio와 dashboard에 일반 주식 4개만 반영
```

## 6. 브라우저 확인

가능하면 Codex in-app browser로 확인한다.

```text id="ehxure"
/portfolio
/trades
/dashboard
```

확인:

```text id="wpcgj8"
- 자금 풀 표시
- 입금 내역 표시
- 거래 내역 4건 표시
- 보유 종목 4개 표시
- ETF 미표시
- 손익 요약 표시
- dashboard KPI 반영
- 한글 깨짐 없음
- 콘솔 에러 없음
- 네트워크 실패 없음
```

브라우저 timeout이 발생하면 API 검증 결과를 우선 기록하고, 브라우저 확인 미완료로 분리한다.

## 7. 금지 사항

```text id="sbm2wu"
- ETF 종목 마스터 추가 금지
- ETF 거래 입력 금지
- holdings 테이블 직접 수정 금지
- 실제 Gmail 발송 금지
- 알림 실제 발송 API 실행 금지
- 운영 DB 삭제 금지
- 운영 DB 초기화 금지
- 새 기능 추가 금지
- 새 테이블 생성 금지
- 새 마이그레이션 생성 금지
```

## 8. 문서 갱신

작업 완료 후 아래 문서를 갱신한다.

```text id="s6lnxp"
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 작성:

```text id="ln2kn1"
docs/NON_ETF_INITIAL_PORTFOLIO_INPUT_REPORT.md
```

포함 내용:

```markdown id="rpjft4"
# NON ETF INITIAL PORTFOLIO INPUT REPORT

## 1. 작업 개요

## 2. ETF 제외 정책

## 3. 백업 결과

## 4. 입력 데이터

## 5. 자금 풀 / 입금 결과

## 6. 거래 입력 결과

## 7. holdings 검증 결과

## 8. portfolio 검증 결과

## 9. dashboard 검증 결과

## 10. 보류 / 확인 필요 항목
```

## 완료 보고

작업 완료 후 다음과 같이 보고하세요.

```text id="wrq1nl"
CODEX_TASK_2.4 ETF 제외 초기 포트폴리오 입력 작업 완료했습니다.
DEVELOPMENT_REPORT.md와 NON_ETF_INITIAL_PORTFOLIO_INPUT_REPORT.md를 확인해 주세요.
```
