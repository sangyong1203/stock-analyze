# CODEX_TASK_2.16

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

이번 작업은 **가격 수집 후 holdings 자동 재계산 연결 검토**입니다.

## 작업

1. 현재 KRX 가격 수집 API/job 이후 holdings 재계산이 자동으로 실행되는지 확인하세요.
2. 자동 실행이 안 된다면, 연결하는 것이 안전한지 검토하세요.
3. 안전하면 최소 수정으로 가격 수집 완료 후 holdings 재계산까지 이어지게 하세요.
4. 위험하거나 범위가 크면 코드 수정하지 말고 운영 절차 유지로 판단하세요.
5. 실제 Gmail 발송은 하지 마세요.
6. 새 테이블 / 새 마이그레이션은 만들지 마세요.
7. 결과를 `docs/DEVELOPMENT_REPORT.md`에 정리하세요.
8. 필요하면 `docs/PRICE_REFRESH_RECALCULATION_LINK_REPORT.md`를 작성하세요.

## 확인 기준

- KRX daily collect
- KRX range collect
- scheduled job manual run
- holdings recalculation
- portfolio summary
- dashboard summary

## 완료 보고

```text
CODEX_TASK_2.16 가격 수집 후 holdings 자동 재계산 연결 검토 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
