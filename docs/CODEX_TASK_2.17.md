# CODEX_TASK_2.17

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

이번 작업은 **실사용 가격 알림 조건 등록 준비**입니다.

## 작업

1. 현재 가격 알림 목록을 확인하세요.
2. 아래 실사용 알림 조건을 등록하세요.
3. 등록 후 dry-run만 실행하세요.
4. 실제 Gmail 발송은 하지 마세요.
5. 새 테이블 / 새 마이그레이션은 만들지 마세요.
6. 결과를 `docs/DEVELOPMENT_REPORT.md`에 정리하세요.

## 등록 조건

```text
NAVER / 035420 / NAVER 진입 가능 알림 / TARGET_PRICE_BELOW / 190000

LG에너지솔루션 / 373220 / LG엔솔 진입 가능 알림 / TARGET_PRICE_BELOW / 330000

현대모비스 / 012330 / 현대모비스 진입 가능 알림 / TARGET_PRICE_BELOW / 320000

LG / 003550 / LG 진입 가능 알림 / TARGET_PRICE_BELOW / 90000

현대차 / 005380 / 현대차 진입 가능 알림 / TARGET_PRICE_BELOW / 300000

LG전자 / 066570 / LG전자 진입 가능 알림 / TARGET_PRICE_BELOW / 140000

삼성SDI / 006400 / 삼성SDI 진입 가능 알림 / TARGET_PRICE_BELOW / 400000
```

## 기준

- 중복 알림이 있으면 새로 만들지 말고 기존 알림을 확인하세요.
- dry-run 결과에서 evaluated_count, sendable_count, skipped reason을 확인하세요.
- 실제 발송 API는 실행하지 마세요.

## 완료 보고

```text
CODEX_TASK_2.17 실사용 가격 알림 조건 등록 및 dry-run 확인 완료했습니다.
실제 Gmail 발송은 하지 않았습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
