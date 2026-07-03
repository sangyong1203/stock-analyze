# CODEX_TASK_2.18

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

이번 작업은 **가격 알림 실제 Gmail 1회 발송 테스트**입니다.

## 작업

1. 가격 알림 dry-run을 먼저 실행해 sendable 대상 수를 확인하세요.
2. sendable 대상이 직전과 동일하게 정상이라면 실제 가격 알림 평가/발송 API를 1회만 실행하세요.
3. `force=true`는 사용하지 마세요.
4. 발송 후 alert histories, summary, dashboard 상태를 확인하세요.
5. 다시 dry-run을 실행해 당일 중복 발송이 차단되는지 확인하세요.
6. 뉴스 알림은 실행하지 마세요.
7. 새 테이블 / 새 마이그레이션은 만들지 마세요.
8. 결과를 `docs/DEVELOPMENT_REPORT.md`에 정리하세요.

## 기준

- 실제 발송 API는 최대 1회만 호출
- 예상 발송 대상은 가격 알림 6건
- NAVER는 조건 미충족이면 발송되지 않아야 함
- 발송 후 동일 알림은 `already_sent_today`로 막혀야 함

## 완료 보고

```text id="ksm9hb"
CODEX_TASK_2.18 가격 알림 실제 Gmail 1회 발송 테스트 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
