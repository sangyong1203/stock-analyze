# CODEX_TASK_2.14

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

이번 작업은 **OpenAI quota / GPT filter 실패 뉴스 재처리 정책 정리**입니다.

## 목표

- `gpt_filter_result = failed` 뉴스 현황 확인
- 실패 원인이 OpenAI quota 429인지 확인
- failed 뉴스 재처리 방법 정리
- 재처리 가능하면 기존 job/API로 dry-run 또는 수동 재처리 확인
- 실제 Gmail 발송 없음
- 새 테이블 / 새 마이그레이션 없음

## 작업

1. 현재 GPT summary/filter 상태를 확인하세요.
2. `gpt_filter_result = failed` 뉴스 목록과 원인을 확인하세요.
3. OpenAI quota 429로 실패한 뉴스가 있으면 재처리 정책을 정리하세요.
4. 기존 재처리 API/job이 있으면 실제 발송 없이 재처리 가능 여부만 확인하세요.
5. 실패 뉴스가 alert sendable 후보에 들어가지 않는지 다시 확인하세요.
6. 결과를 `docs/DEVELOPMENT_REPORT.md`에 정리하세요.
7. 필요하면 `docs/GPT_FILTER_FAILURE_POLICY_REPORT.md`를 작성하세요.

## 기준

- 실제 Gmail 발송 금지
- 뉴스 row 삭제 금지
- alert history 삭제 금지
- 새 기능을 크게 추가하지 말고 실패 관리 정책 중심으로 정리
- API key 값 출력 금지

## 완료 보고

```text
CODEX_TASK_2.14 GPT filter 실패 뉴스 재처리 정책 정리 완료했습니다.
실제 Gmail 발송은 하지 않았습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
