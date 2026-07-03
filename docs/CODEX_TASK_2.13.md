# CODEX_TASK_2.13

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

이번 작업은 **뉴스 알림 발송 정책 강화**입니다.

## 목표

- GPT filter failed 뉴스가 sendable 후보로 남지 않게 수정
- 오래된 뉴스의 발송 후보 제외 기준 확인
- 종목 연결 없는 광범위 시장 뉴스의 발송 기준 정리
- 실제 Gmail 발송 없음
- 새 테이블 / 새 마이그레이션 없음

## 작업

1. 현재 뉴스 알림 후보 산정 로직을 확인하세요.
2. `gpt_filter_result = failed` 또는 unresolved 상태인 뉴스가 sendable이 되는지 확인하세요.
3. 해당 뉴스는 실제 발송 후보에서 제외되도록 최소 수정하세요.
4. 기존 뉴스 알림 dry-run을 다시 실행해 sendable 후보가 적절히 줄었는지 확인하세요.
5. `/news`, `/dashboard`, `/settings` 화면을 확인하세요.
6. 결과를 `docs/DEVELOPMENT_REPORT.md`에 정리하세요.
7. 필요하면 `docs/NEWS_ALERT_POLICY_FIX_REPORT.md`를 작성하세요.

## 기준

- 실제 발송 API는 실행하지 마세요.
- 뉴스 데이터 자체를 삭제하지 마세요.
- 기존 발송 이력은 보존하세요.
- 새 기능을 크게 추가하지 말고 발송 후보 정책만 정리하세요.

## 완료 보고

```text
CODEX_TASK_2.13 뉴스 알림 발송 정책 강화 작업 완료했습니다.
실제 Gmail 발송은 하지 않았습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
