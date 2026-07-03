# CODEX_TASK_2.7

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

CODEX_TASK_2.6에서 포트폴리오 브라우저 UI 검증과 `Failed to fetch` 수정은 완료됐습니다.

이번 작업은 **실사용 가격 알림 조건 준비 / dry-run 검증 / Gmail 발송 전 안전 점검**입니다.

## 목표

1. 현재 포트폴리오 기준 가격 알림 기능이 정상 동작하는지 확인한다.
2. 실제 알림 조건 가격은 사용자가 명시 제공한 경우에만 등록한다.
3. 사용자가 제공하지 않은 목표가, 진입가, 손절가를 임의 생성하지 않는다.
4. 실제 Gmail 발송은 하지 않는다.
5. dry-run으로만 가격 알림 평가 흐름을 검증한다.
6. 알림 등록 전 입력 가이드를 작성한다.
7. 새 기능, 새 테이블, 새 마이그레이션은 만들지 않는다.

## 작업 전 확인

직전 문서만 확인한다.

```text
docs/DEVELOPMENT_REPORT.md
docs/PORTFOLIO_BROWSER_FETCH_FIX_REPORT.md
docs/INITIAL_PORTFOLIO_PRICE_VALIDATION_REPORT.md
```

기준 문서를 반복해서 다시 읽지 않는다.

## 현재 포트폴리오 기준값

아래 보유 종목은 이미 입력되어 있고, 수정하지 않는다.

```csv
stock_name,stock_code,quantity,average_price,current_price,market_value,unrealized_profit_loss
삼성SDI,006400,5,596970,185300,926500,-2058350
두산에너빌리티,034020,10,105215,61900,619000,-433150
삼성E&A,028050,10,55809,23200,232000,-326090
NAVER,035420,2,256500,253000,506000,-7000
```

포트폴리오 합계:

```text
total_cash = 0
total_invested_amount = 5108090
total_market_value = 2283500
total_unrealized_profit_loss = -2824590
holding_count = 4
```

## 1. 현재 알림 상태 확인

다음 API를 확인한다.

```text
/api/price-alerts
/api/price-alerts/summary
/api/price-alerts/histories
/api/price-alerts/evaluate/dry-run
```

확인할 것:

```text
- 현재 price_alerts row count
- 활성 알림 수
- 비활성 알림 수
- alert_histories 기존 기록 수
- dry-run 실행 시 실제 발송이 발생하지 않는지
- 중복 발송 방지 로직이 유지되는지
```

## 2. 알림 등록 조건

이번 작업에서는 사용자가 명시적으로 제공한 가격 조건이 없으면 실제 알림을 등록하지 않는다.

금지:

```text
- 목표가 임의 생성 금지
- 진입가 임의 생성 금지
- 손절가 임의 생성 금지
- 평균단가 기준으로 자동 목표가 만들기 금지
- 현재가 기준 ±%로 임의 알림 만들기 금지
```

허용:

```text
- 사용자가 제공한 조건이 문서 또는 현재 입력에 명확히 있으면 등록 후보로 정리
- 애매하면 등록하지 않고 확인 필요 항목에 기록
- dry-run API 검증은 가능
```

## 3. 알림 조건 입력 가이드 작성

사용자가 다음에 가격 조건을 쉽게 줄 수 있도록 입력 가이드를 만든다.

작성 문서:

```text
docs/PRICE_ALERT_INPUT_GUIDE.md
```

구성:

```markdown
# PRICE ALERT INPUT GUIDE

## 1. 목적

## 2. 현재 보유 종목

## 3. 알림 조건 종류

## 4. 입력 양식

## 5. 예시

## 6. dry-run 확인 절차

## 7. 실제 Gmail 발송 전 체크리스트

## 8. 중복 발송 방지 기준

## 9. 주의사항
```

알림 조건 종류 설명:

```text
TARGET_PRICE_ABOVE:
현재가가 특정 가격 이상일 때 알림

TARGET_PRICE_BELOW:
현재가가 특정 가격 이하일 때 알림

DROP_FROM_HIGH:
최근 고점 대비 일정 하락 시 알림

RISE_FROM_LOW:
최근 저점 대비 일정 상승 시 알림
```

입력 양식 예시:

```csv
stock_name,stock_code,alert_name,alert_type,target_price,enabled,memo
NAVER,035420,NAVER 진입 알림,TARGET_PRICE_BELOW,190000,true,사용자 지정 진입 가격
삼성SDI,006400,삼성SDI 회복 알림,TARGET_PRICE_ABOVE,400000,true,사용자 지정 회복 가격
```

주의:

```text
위 예시는 문서용 예시일 뿐이며, 이번 작업에서 실제 등록하지 않는다.
```

## 4. dry-run 검증

실제 알림 등록이 없는 상태에서도 dry-run API가 정상 응답하는지 확인한다.

```text
/api/price-alerts/evaluate/dry-run
/api/price-alerts/summary
/api/price-alerts/histories
```

확인:

```text
- API 200
- 실제 Gmail 발송 없음
- alert_histories에 sent 기록이 불필요하게 추가되지 않음
- 조건이 없으면 evaluated 0 또는 이에 준하는 정상 응답
```

## 5. 브라우저 확인

가능하면 아래 화면을 확인한다.

```text
/alerts
/dashboard
```

확인:

```text
- 가격 알림 화면 진입 가능
- 현재 알림 목록 표시
- 빈 상태 표시 정상
- dry-run 관련 버튼/영역 표시
- 알림 이력 표시
- 실제 발송 버튼은 누르지 않음
- 콘솔 에러 없음
- Failed to fetch 없음
- 한글 깨짐 없음
```

## 6. 검증

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
/api/price-alerts
/api/price-alerts/summary
/api/price-alerts/histories
/api/price-alerts/evaluate/dry-run
/api/dashboard/summary
```

## 7. 금지 사항

```text
- 실제 Gmail 발송 금지
- /api/price-alerts/evaluate 실제 발송 경로 실행 금지
- 사용자가 제공하지 않은 알림 조건 등록 금지
- 가격 목표 임의 생성 금지
- 포트폴리오 수량 변경 금지
- 평균단가 변경 금지
- 기존 BUY 거래 수정/삭제 금지
- holdings 직접 수정 금지
- 새 기능 추가 금지
- 새 테이블 생성 금지
- 새 마이그레이션 생성 금지
```

## 8. 문서 갱신

작업 완료 후 아래 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 작성:

```text
docs/PRICE_ALERT_READY_REPORT.md
```

포함 내용:

```markdown
# PRICE ALERT READY REPORT

## 1. 작업 개요

## 2. 현재 알림 상태

## 3. dry-run 검증 결과

## 4. 브라우저 확인 결과

## 5. PRICE_ALERT_INPUT_GUIDE 작성 결과

## 6. 실제 발송 전 체크리스트

## 7. 보류 / 확인 필요 항목
```

## 완료 보고

작업 완료 후 다음과 같이 보고하세요.

```text
CODEX_TASK_2.7 실사용 가격 알림 준비 작업 완료했습니다.
DEVELOPMENT_REPORT.md와 PRICE_ALERT_INPUT_GUIDE.md를 확인해 주세요.
```
