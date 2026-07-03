# CODEX_TASK_2.8

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

CODEX_TASK_2.7에서 가격 알림 기능 준비와 dry-run 검증은 완료됐습니다.

사용자 결정:
실사용 알림 조건은 아직 없지만, 테스트를 위해 지금 당장 테스트 가능한 가격 알림 조건을 등록합니다.

이번 작업은 **테스트용 가격 알림 조건 등록 / dry-run 검증 / 실제 발송 전 안전 확인**입니다.

## 목표

1. 테스트용 가격 알림 조건을 명시적으로 등록한다.
2. 매칭되는 알림과 매칭되지 않는 알림을 각각 만든다.
3. `/api/price-alerts/evaluate/dry-run`으로 결과를 확인한다.
4. 실제 Gmail 발송은 하지 않는다.
5. 포트폴리오, 거래, holdings 데이터는 변경하지 않는다.
6. 새 기능, 새 테이블, 새 마이그레이션은 만들지 않는다.

## 작업 전 확인

직전 문서만 확인한다.

```text id="imz8na"
docs/DEVELOPMENT_REPORT.md
docs/PRICE_ALERT_INPUT_GUIDE.md
docs/PRICE_ALERT_READY_REPORT.md
```

기준 문서를 반복해서 다시 읽지 않는다.

## 현재 기준 가격

아래 값은 CODEX_TASK_2.5에서 검증된 가격 기준이다.

```csv id="cfz9yl"
stock_name,stock_code,current_price
삼성SDI,006400,185300
두산에너빌리티,034020,61900
삼성E&A,028050,23200
NAVER,035420,253000
```

## 등록할 테스트 알림

아래 2개만 생성한다.

```csv id="cuh6zq"
stock_name,stock_code,alert_name,alert_type,target_price,threshold_percent,enabled,memo
NAVER,035420,TEST_NAVER_즉시매칭_TEST,TARGET_PRICE_ABOVE,250000,,true,dry-run 매칭 확인용 테스트 알림
삼성SDI,006400,TEST_삼성SDI_미매칭_TEST,TARGET_PRICE_ABOVE,400000,,true,dry-run 미매칭 확인용 테스트 알림
```

기대 결과:

```text id="kdn2ko"
NAVER:
현재가 253,000 >= 목표가 250,000
dry-run matched 예상

삼성SDI:
현재가 185,300 < 목표가 400,000
dry-run not matched 예상
```

## 입력 전 상태 확인

다음 API를 확인한다.

```text id="f23z3i"
/api/price-alerts
/api/price-alerts/summary
/api/price-alerts/histories
```

현재 기준 예상:

```text id="t58sd8"
price_alerts row count = 0
price_alert_histories row count = 0
```

## 등록 순서

```text id="x8vg18"
1. NAVER 테스트 알림 생성
2. 삼성SDI 테스트 알림 생성
3. /api/price-alerts로 생성 결과 확인
4. /api/price-alerts/summary 확인
5. /api/price-alerts/evaluate/dry-run 실행
6. /api/price-alerts/histories 확인
7. 실제 Gmail 발송은 하지 않음
```

## dry-run 검증 기준

```text id="4ln2yv"
- evaluated_count = 2 예상
- matched_count >= 1 예상
- NAVER 테스트 알림은 matched 예상
- 삼성SDI 테스트 알림은 not matched 예상
- sent_count = 0
- failed_count = 0
- 실제 Gmail 발송 없음
```

주의:

```text id="dqppyh"
dry-run은 실제 발송하지 않아야 한다.
alert_histories에 sent 기록이 생기면 안 된다.
```

## 브라우저 확인

가능하면 Codex in-app browser로 확인한다.

```text id="lg132p"
/alerts
/dashboard
```

확인:

```text id="5st93o"
- /alerts에 테스트 알림 2개 표시
- TEST_NAVER_즉시매칭_TEST 표시
- TEST_삼성SDI_미매칭_TEST 표시
- summary total_count = 2
- dry-run 버튼 동작 확인
- 실제 발송 버튼 클릭 금지
- /dashboard 가격 알림 active count 반영
- Failed to fetch 없음
- 콘솔 application error 없음
```

## 금지 사항

```text id="26girf"
- 실제 Gmail 발송 금지
- /api/price-alerts/evaluate 실제 발송 경로 실행 금지
- force=true 실행 금지
- 포트폴리오 데이터 수정 금지
- 거래 수정/삭제 금지
- holdings 직접 수정 금지
- 테스트 알림 2개 외 추가 알림 생성 금지
- 새 기능 추가 금지
- 새 테이블 생성 금지
- 새 마이그레이션 생성 금지
```

## 문서 갱신

작업 완료 후 아래 문서를 갱신한다.

```text id="7k3crf"
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 작성:

```text id="5dzr02"
docs/PRICE_ALERT_TEST_REGISTRATION_REPORT.md
```

포함 내용:

```markdown id="yutg0k"
# PRICE ALERT TEST REGISTRATION REPORT

## 1. 작업 개요

## 2. 등록한 테스트 알림

## 3. dry-run 검증 결과

## 4. 브라우저 확인 결과

## 5. 실제 발송 미실행 확인

## 6. 다음 단계

## 7. 보류 / 확인 필요 항목
```

## 완료 보고

작업 완료 후 다음과 같이 보고하세요.

```text id="ugb4gx"
CODEX_TASK_2.8 테스트용 가격 알림 조건 등록 작업 완료했습니다.
실제 Gmail 발송 없이 dry-run까지 확인했습니다.
DEVELOPMENT_REPORT.md와 PRICE_ALERT_TEST_REGISTRATION_REPORT.md를 확인해 주세요.
```
