# CODEX_TASK_2.5

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

CODEX_TASK_2.4에서 초기 포트폴리오 입력은 완료됐습니다.

이번 작업은 **초기 포트폴리오 현재가 검증 / 가격 데이터 최신화 / 평가손익 재계산 확인**입니다.

## 목표

1. 사용자가 제공한 며칠 전 데이터는 평단가 산출용으로만 사용한다.
2. 현재 평가금액과 손익은 시스템의 최신 가격 데이터 기준으로 다시 계산한다.
3. 현재 holdings / portfolio 평가금액이 어떤 가격 기준으로 계산되는지 확인한다.
4. 가격 데이터가 오래됐거나 누락됐으면 기존 KRX 가격 수집 기능으로 최신화한다.
5. 평균단가와 수량은 변경하지 않는다.
6. 새 기능, 새 테이블, 새 마이그레이션은 만들지 않는다.
7. 실제 Gmail 발송은 하지 않는다.

## 작업 전 확인

직전 문서만 확인한다.

```text id="reqgjq"
docs/DEVELOPMENT_REPORT.md
docs/NON_ETF_INITIAL_PORTFOLIO_INPUT_REPORT.md
```

기준 문서를 반복해서 다시 읽지 않는다.

## 현재 입력된 초기 포트폴리오

아래 4개 종목만 확인한다.

```csv id="nkwxo0"
stock_name,stock_code,quantity,average_price,cost_amount
삼성SDI,006400,5,596970,2984850
두산에너빌리티,034020,10,105215,1052150
삼성E&A,028050,10,55809,558090
NAVER,035420,2,256500,513000
```

## 1. 현재 holdings 계산 기준 확인

다음 API와 DB를 확인한다.

```text id="l79rhj"
/api/holdings
/api/holdings/summary
/api/portfolio/summary
/api/dashboard/summary
```

확인할 것:

```text id="tdphk0"
- 각 종목 quantity
- average_price
- cost_amount
- current_price
- market_value
- unrealized_profit_loss
- unrealized_profit_loss_rate
- 가격 기준일
```

가격 기준일이 API에 없으면 DB에서 `stock_prices`의 최신 `date`를 확인한다.

## 2. 가격 데이터 검증

아래 종목의 최신 가격 데이터를 확인한다.

```text id="d4zopf"
006400 삼성SDI
034020 두산에너빌리티
028050 삼성E&A
035420 NAVER
```

확인 항목:

```text id="qzu77v"
- stock_prices에 최신 데이터가 있는지
- latest date가 언제인지
- close price가 얼마인지
- holdings current_price와 일치하는지
- 종목코드 매칭이 정확한지
```

## 3. 최신 가격 수집

가격 데이터가 오래됐거나 누락됐으면 기존 KRX 수집 기능 또는 scheduled job 수동 실행 구조를 사용해 최신 거래일 기준 가격을 수집한다.

주의:

```text id="fheh58"
- 새 수집 기능을 만들지 않는다.
- 기존 수집 API/job만 사용한다.
- 수집 실패 시 원인을 보고서에 기록한다.
```

## 4. 재계산 확인

최신 가격 반영 후 다시 확인한다.

```text id="usm405"
/api/holdings
/api/holdings/summary
/api/portfolio/summary
/api/dashboard/summary
```

검증 기준:

```text id="xyrje0"
- quantity는 기존 입력값 유지
- average_price는 기존 입력값 유지
- cost_amount 합계 = 5,108,090
- current_price는 최신 가격 기준
- market_value = current_price * quantity
- unrealized_profit_loss = market_value - cost_amount
- portfolio total_market_value = holdings market_value 합계
- dashboard 값이 portfolio summary와 일치
```

## 5. 사용자 제공 이전 데이터와 비교

참고용으로만 비교한다.

```csv id="oj4oek"
stock_name,old_current_value,old_profit_loss,quantity
삼성SDI,2242500,-742350,5
두산에너빌리티,804000,-248150,10
삼성E&A,403500,-154590,10
NAVER,384200,-128800,2
```

비교 보고서에 기록할 것:

```text id="pwgopb"
- 사용자 제공 당시 평가금액
- 시스템 최신 가격 기준 평가금액
- 차이 금액
- 차이 원인 추정
  - 가격 기준일 차이
  - KRX 가격 데이터 미갱신
  - 종목 매칭 문제
  - 장중/종가 기준 차이
```

## 6. 브라우저 확인

가능하면 아래 화면을 확인한다.

```text id="ppqm6d"
/portfolio
/dashboard
```

확인:

```text id="s7yvpt"
- 보유 종목 4개 표시
- 현재가 표시
- 평가금액 표시
- 평가손익 표시
- dashboard KPI 반영
- 한글 깨짐 없음
- 콘솔 에러 없음
- 네트워크 실패 없음
```

브라우저 확인이 안 되면 API 검증 결과를 우선한다.

## 7. 금지 사항

```text id="x2jon2"
- 평균단가 변경 금지
- 수량 변경 금지
- 기존 BUY 거래 삭제/수정 금지
- holdings 직접 수정 금지
- 평가금액을 수동 입력하지 않는다
- 실제 Gmail 발송 금지
- 새 기능 추가 금지
- 새 테이블 생성 금지
- 새 마이그레이션 생성 금지
```

## 8. 문서 갱신

작업 완료 후 아래 문서를 갱신한다.

```text id="en9z45"
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 작성:

```text id="kf7r1n"
docs/INITIAL_PORTFOLIO_PRICE_VALIDATION_REPORT.md
```

포함 내용:

```markdown id="tcw9zg"
# INITIAL PORTFOLIO PRICE VALIDATION REPORT

## 1. 작업 개요

## 2. 현재 입력된 포트폴리오

## 3. 가격 데이터 기준일 확인

## 4. 종목별 현재가 검증

## 5. holdings 재계산 결과

## 6. portfolio summary 검증 결과

## 7. dashboard 검증 결과

## 8. 사용자 제공 이전 평가금액과 비교

## 9. 발견한 문제

## 10. 보류 / 확인 필요 항목
```

## 완료 보고

작업 완료 후 다음과 같이 보고하세요.

```text id="towrjy"
CODEX_TASK_2.5 초기 포트폴리오 현재가 검증 작업 완료했습니다.
DEVELOPMENT_REPORT.md와 INITIAL_PORTFOLIO_PRICE_VALIDATION_REPORT.md를 확인해 주세요.
```
