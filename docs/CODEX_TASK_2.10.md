# CODEX_TASK_2.10

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

CODEX_TASK_2.9에서 Gmail 실제 발송 1회 테스트는 완료됐습니다.

이번 작업은 **테스트 가격 알림 정리 / 실사용 알림 등록 준비 상태 복원**입니다.

## 목표

1. 테스트 목적으로 만든 가격 알림 2건을 삭제한다.
2. 실제 발송 검증 이력은 보존한다.
3. 실사용 알림 등록 전 깨끗한 상태로 되돌린다.
4. 포트폴리오, 거래, holdings 데이터는 변경하지 않는다.
5. 실제 Gmail 발송은 하지 않는다.
6. 새 기능, 새 테이블, 새 마이그레이션은 만들지 않는다.

## 작업 전 확인

직전 문서만 확인한다.

```text
docs/DEVELOPMENT_REPORT.md
docs/PRICE_ALERT_GMAIL_SEND_TEST_REPORT.md
docs/PRICE_ALERT_TEST_REGISTRATION_REPORT.md
```

기준 문서를 반복해서 다시 읽지 않는다.

## 현재 상태

현재 테스트 알림 2건이 등록되어 있다.

```csv
stock_name,stock_code,alert_name,alert_type,target_price,status
NAVER,035420,TEST_NAVER_즉시매칭_TEST,TARGET_PRICE_ABOVE,250000,sent history exists
삼성SDI,006400,TEST_삼성SDI_미매칭_TEST,TARGET_PRICE_ABOVE,400000,skipped history exists
```

현재 이력:

```text
alert_histories = 2
- NAVER sent 1건
- 삼성SDI skipped 1건
```

## 1. 삭제 전 상태 확인

다음 API를 확인한다.

```text
/api/price-alerts
/api/price-alerts/summary
/api/price-alerts/histories
/api/dashboard/summary
```

기대값:

```text
price_alerts row count = 2
enabled_count = 2
alert_histories row count = 2
sent_count = 1
skipped_count = 1
```

## 2. 테스트 알림 삭제

아래 2건만 삭제한다.

```text
TEST_NAVER_즉시매칭_TEST
TEST_삼성SDI_미매칭_TEST
```

주의:

```text
- alert_histories는 삭제하지 않는다.
- 테스트 알림 row만 삭제한다.
- 포트폴리오/거래/보유종목 데이터는 건드리지 않는다.
```

## 3. 삭제 후 상태 확인

다음 API를 다시 확인한다.

```text
/api/price-alerts
/api/price-alerts/summary
/api/price-alerts/histories
/api/dashboard/summary
```

검증 기준:

```text
price_alerts row count = 0
enabled_count = 0
alert_histories row count = 2 유지
sent_count = 1 유지
skipped_count = 1 유지
dashboard 가격 알림 활성 = 0
dashboard 가격 알림 발송 이력은 보존
```

## 4. dry-run 확인

삭제 후 dry-run을 실행한다.

```text
/api/price-alerts/evaluate/dry-run
```

기대값:

```text
evaluated_count = 0
matched_count = 0
sendable_count = 0
sent_count = 0
failed_count = 0
```

실제 Gmail 발송 API는 실행하지 않는다.

## 5. 브라우저 확인

가능하면 Codex in-app browser로 확인한다.

```text
/alerts
/dashboard
```

확인:

```text
- /alerts 알림 목록 0건
- 기존 발송/스킵 이력 표시 여부 확인
- /dashboard 가격 알림 활성 0
- 가격 알림 발송 수 또는 최근 이력은 보존
- Failed to fetch 없음
- 콘솔 application error 없음
```

## 6. 금지 사항

```text
- 실제 Gmail 발송 금지
- /api/price-alerts/evaluate 실제 발송 경로 실행 금지
- alert_histories 삭제 금지
- 포트폴리오 데이터 수정 금지
- 거래 수정/삭제 금지
- holdings 직접 수정 금지
- 새 기능 추가 금지
- 새 테이블 생성 금지
- 새 마이그레이션 생성 금지
```

## 7. 검증

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

API:

```text
/health
/api/price-alerts
/api/price-alerts/summary
/api/price-alerts/histories
/api/price-alerts/evaluate/dry-run
/api/dashboard/summary
```

## 8. 문서 갱신

작업 완료 후 아래 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 작성:

```text
docs/PRICE_ALERT_TEST_CLEANUP_REPORT.md
```

포함 내용:

```markdown
# PRICE ALERT TEST CLEANUP REPORT

## 1. 작업 개요

## 2. 삭제 전 상태

## 3. 삭제한 테스트 알림

## 4. 삭제 후 상태

## 5. alert_histories 보존 확인

## 6. dry-run 확인 결과

## 7. 브라우저 확인 결과

## 8. 다음 단계
```

## 완료 보고

작업 완료 후 다음과 같이 보고하세요.

```text
CODEX_TASK_2.10 테스트 가격 알림 정리 작업 완료했습니다.
테스트 알림 2건은 삭제했고, 발송 검증 이력은 보존했습니다.
DEVELOPMENT_REPORT.md와 PRICE_ALERT_TEST_CLEANUP_REPORT.md를 확인해 주세요.
```
