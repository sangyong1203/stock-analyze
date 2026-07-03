# CODEX_TASK_2.15

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

이번 작업은 **가격 데이터 최신화 운영 루틴 정리**입니다.

작업:

1. 현재 KRX 가격 수집 job/API 상태를 확인하세요.
2. 가격 수집 후 holdings 재계산이 필요한 흐름을 정리하세요.
3. 현재 보유 4종목의 최신 가격 기준일과 holdings 반영 상태를 확인하세요.
4. 기존 API/job으로 가격 수집 → holdings 재계산 → portfolio/dashboard 확인 순서를 검증하세요.
5. 실제 Gmail 발송은 하지 마세요.
6. 새 기능, 새 테이블, 새 마이그레이션은 만들지 마세요.
7. 결과를 `docs/DEVELOPMENT_REPORT.md`에 정리하세요.
8. 필요하면 `docs/PRICE_REFRESH_OPERATION_ROUTINE.md`를 작성하세요.

운영 루틴 문서에는 아래만 정리하세요.

```text
1. KRX 가격 수집 순서
2. 수집 완료 확인 API
3. holdings 재계산 순서
4. portfolio/dashboard 확인 API
5. 가격 알림 dry-run 실행 순서
6. 실패 시 확인할 항목
```

완료 보고:

```text
CODEX_TASK_2.15 가격 데이터 최신화 운영 루틴 정리 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
