# CODEX_TASK_2.9

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

CODEX_TASK_2.8에서 테스트용 가격 알림 2건 등록과 dry-run 검증은 완료됐습니다.

사용자 확인:
Gmail 실제 발송 1회 테스트를 진행합니다.

이번 작업은 **NAVER 테스트 가격 알림 기준 Gmail 실제 발송 1회 테스트 / 발송 이력 검증 / 중복 방지 확인**입니다.

## 목표

1. 테스트 알림 중 실제 매칭된 NAVER 알림 1건만 실제 발송되도록 확인한다.
2. 실제 Gmail 발송 API를 1회만 실행한다.
3. 삼성SDI 미매칭 알림은 발송되지 않아야 한다.
4. 발송 후 `alert_histories` 기록을 확인한다.
5. 같은 날 중복 발송 방지 상태를 확인한다.
6. 포트폴리오, 거래, holdings 데이터는 변경하지 않는다.
7. 새 기능, 새 테이블, 새 마이그레이션은 만들지 않는다.

## 작업 전 확인

직전 문서만 확인한다.

```text id="m5lmnb"
docs/DEVELOPMENT_REPORT.md
docs/PRICE_ALERT_TEST_REGISTRATION_REPORT.md
docs/PRICE_ALERT_READY_REPORT.md
```

기준 문서를 반복해서 다시 읽지 않는다.

## 현재 테스트 알림 상태

현재 등록된 테스트 알림은 2건이다.

```csv id="z2xg2u"
stock_name,stock_code,alert_name,alert_type,target_price,expected_result
NAVER,035420,TEST_NAVER_즉시매칭_TEST,TARGET_PRICE_ABOVE,250000,matched
삼성SDI,006400,TEST_삼성SDI_미매칭_TEST,TARGET_PRICE_ABOVE,400000,not_matched
```

직전 dry-run 결과:

```text id="piwqfg"
evaluated_count = 2
matched_count = 1
sendable_count = 1
sent_count = 0
failed_count = 0
skipped_count = 1

NAVER: would_send
삼성SDI: skipped / condition_not_met
```

## 1. 발송 전 상태 확인

다음 API를 확인한다.

```text id="j7xz7v"
/api/price-alerts
/api/price-alerts/summary
/api/price-alerts/histories
/api/price-alerts/evaluate/dry-run
```

발송 전 기대값:

```text id="z0k0h9"
price_alerts row count = 2
enabled_count = 2
price alert histories row count = 0
dry-run matched_count = 1
dry-run sendable_count = 1
```

## 2. Gmail 설정 확인

실제 발송 전 Gmail 관련 설정 존재 여부만 확인한다.

확인 항목:

```text id="mizvbm"
GMAIL_SMTP_HOST
GMAIL_SMTP_PORT
GMAIL_SMTP_USERNAME
GMAIL_SMTP_APP_PASSWORD
ALERT_RECIPIENT_EMAIL
```

주의:

```text id="uekj1e"
- 실제 값은 출력하지 않는다.
- configured / missing 상태만 기록한다.
- 하나라도 missing이면 실제 발송을 실행하지 말고 중단한다.
```

## 3. 실제 발송 실행

Gmail 설정이 configured 상태이면 실제 발송 API를 정확히 1회만 실행한다.

실행 대상:

```text id="mpe5z2"
POST /api/price-alerts/evaluate
```

조건:

```text id="rqb32d"
- force=false
- 실제 발송 API는 한 번만 호출
- force=true 금지
- 반복 호출 금지
```

기대 결과:

```text id="x89r25"
evaluated_count = 2
matched_count = 1
sendable_count = 1
sent_count = 1
failed_count = 0
skipped_count = 1

NAVER: sent 예상
삼성SDI: skipped / condition_not_met 예상
```

실패 시:

```text id="ma8qb5"
- 실패 원인을 기록한다.
- 같은 작업에서 재시도하지 않는다.
- force=true 사용하지 않는다.
- Gmail 설정 또는 SMTP 오류면 확인 필요 항목에 기록한다.
```

## 4. 발송 후 이력 확인

실행 후 확인 API:

```text id="sz1lkr"
/api/price-alerts/histories
/api/price-alerts/summary
/api/dashboard/summary
```

확인 기준:

```text id="cfaybk"
- alert_histories row count = 1 예상
- NAVER 테스트 알림 sent 이력 1건 예상
- 삼성SDI sent 이력 없어야 함
- summary sent_count = 1 예상
- today_sent_count = 1 예상
- dashboard 가격 알림 발송 수 반영 확인
```

## 5. 중복 발송 방지 확인

실제 발송 API를 다시 호출하지 않는다.

대신 아래 방식으로 확인한다.

```text id="ncm6re"
1. alert_histories에서 NAVER sent 이력이 오늘 날짜로 존재하는지 확인
2. duplicate-send prevention 로직이 같은 날 sent 이력을 기준으로 막는 구조인지 확인
3. 필요하면 dry-run만 다시 실행해 상태를 확인한다
```

주의:

```text id="pgn7xk"
- 실제 발송 API 두 번째 호출 금지
- force=true 금지
```

## 6. 브라우저 확인

가능하면 Codex in-app browser로 확인한다.

```text id="o0hz4v"
/alerts
/dashboard
```

확인:

```text id="lyf12r"
- /alerts에 테스트 알림 2건 표시
- 발송 이력 1건 표시
- 오늘 발송 수 1 표시
- dashboard 가격 알림 발송 수 1 반영
- 실제 발송 버튼 추가 클릭 금지
- Failed to fetch 없음
- 콘솔 application error 없음
```

## 7. 금지 사항

```text id="hc3a29"
- 실제 발송 API 반복 호출 금지
- force=true 실행 금지
- 삼성SDI 알림을 발송되게 조건 변경 금지
- 테스트 알림 조건 변경 금지
- 포트폴리오 데이터 수정 금지
- 거래 수정/삭제 금지
- holdings 직접 수정 금지
- 새 기능 추가 금지
- 새 테이블 생성 금지
- 새 마이그레이션 생성 금지
```

## 8. 문서 갱신

작업 완료 후 아래 문서를 갱신한다.

```text id="kznjxc"
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 작성:

```text id="k8q08f"
docs/PRICE_ALERT_GMAIL_SEND_TEST_REPORT.md
```

포함 내용:

```markdown id="ye3ofw"
# PRICE ALERT GMAIL SEND TEST REPORT

## 1. 작업 개요

## 2. 발송 전 알림 상태

## 3. Gmail 설정 확인 결과

## 4. 실제 발송 실행 결과

## 5. alert_histories 검증 결과

## 6. dashboard / alerts 화면 확인 결과

## 7. 중복 발송 방지 확인

## 8. 보류 / 확인 필요 항목
```

## 완료 보고

발송 성공 시:

```text id="qqly8b"
CODEX_TASK_2.9 Gmail 실제 발송 1회 테스트 완료했습니다.
NAVER 테스트 알림 1건이 발송되었고, 삼성SDI 테스트 알림은 조건 미충족으로 발송되지 않았습니다.
DEVELOPMENT_REPORT.md와 PRICE_ALERT_GMAIL_SEND_TEST_REPORT.md를 확인해 주세요.
```

발송 실패 또는 설정 누락 시:

```text id="vfqxp8"
CODEX_TASK_2.9 Gmail 실제 발송 테스트는 중단/실패했습니다.
원인과 확인 필요 항목을 DEVELOPMENT_REPORT.md와 PRICE_ALERT_GMAIL_SEND_TEST_REPORT.md에 기록했습니다.
```
