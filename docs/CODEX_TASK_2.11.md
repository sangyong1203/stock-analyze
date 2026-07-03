# CODEX_TASK_2.11

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

이번 작업은 **가격 알림 + 뉴스 알림 실사용 준비 통합 점검**입니다.

## 목표

- 가격 알림 현재 상태 확인
- 뉴스 알림 현재 상태 확인
- 두 알림 모두 dry-run 검증
- `/alerts`, `/dashboard`, `/news`, `/settings` 화면 확인
- 실제 Gmail 발송은 하지 않음
- 새 기능 / 새 테이블 / 새 마이그레이션 없음

## 참고 문서

직전 결과만 확인하세요.

```text
docs/DEVELOPMENT_REPORT.md
docs/PRICE_ALERT_TEST_CLEANUP_REPORT.md
docs/PRICE_ALERT_INPUT_GUIDE.md
docs/PRICE_ALERT_READY_REPORT.md
```

기준 문서를 반복해서 다시 읽지 마세요.

## 작업 내용

### 1. 가격 알림 확인

확인 API:

```text
/api/price-alerts
/api/price-alerts/summary
/api/price-alerts/histories
/api/price-alerts/evaluate/dry-run
```

확인할 것:

```text
- 현재 알림 수
- 기존 발송/스킵 이력 유지 여부
- dry-run 정상 여부
- 실제 발송 이력 추가 없음
```

사용자가 새 가격 조건을 제공하지 않았으므로 가격 알림은 새로 만들지 않습니다.

### 2. 뉴스 알림 확인

확인 API:

```text
/api/news/summary
/api/news/gpt/targets
/api/news/gpt/status
/api/news/alerts/summary
/api/news/alerts/send/dry-run
```

확인할 것:

```text
- 뉴스 수집 상태
- GPT 처리 대상 상태
- 뉴스 알림 후보 상태
- 뉴스 알림 dry-run 정상 여부
- 실제 발송 이력 추가 없음
```

실제 뉴스 알림 발송 API는 실행하지 않습니다.

### 3. 화면 확인

가능하면 브라우저에서 확인하세요.

```text
/alerts
/dashboard
/news
/settings
```

확인할 것:

```text
- 가격 알림 상태 표시
- 뉴스 목록 표시
- 뉴스 알림 요약 표시
- job 상태 표시
- Failed to fetch 없음
- 한글 깨짐 없음
```

### 4. 검증

```bash
cd backend
python -m compileall app
```

```bash
cd frontend
npm run build
```

최소 API:

```text
/health
/api/price-alerts/summary
/api/price-alerts/evaluate/dry-run
/api/news/summary
/api/news/alerts/summary
/api/news/alerts/send/dry-run
/api/dashboard/summary
/api/jobs/summary
```

## 문서

갱신:

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 작성:

```text
docs/ALERTS_OPERATION_READY_REPORT.md
```

포함 내용:

```markdown
# ALERTS OPERATION READY REPORT

## 1. 작업 개요

## 2. 가격 알림 상태

## 3. 가격 알림 dry-run 결과

## 4. 뉴스 알림 상태

## 5. 뉴스 알림 dry-run 결과

## 6. 화면 확인 결과

## 7. 실제 발송 미실행 확인

## 8. 보류 / 다음 단계
```

## 완료 보고

```text
CODEX_TASK_2.11 가격 알림 + 뉴스 알림 실사용 준비 통합 점검 완료했습니다.
실제 Gmail 발송 없이 dry-run과 화면 확인만 수행했습니다.
DEVELOPMENT_REPORT.md와 ALERTS_OPERATION_READY_REPORT.md를 확인해 주세요.
```
