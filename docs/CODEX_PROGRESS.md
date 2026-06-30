# CODEX PROGRESS

## 현재 단계

- Phase: 가격 알림 조건 / Gmail 발송 연결 / Alerts 화면 정리
- 작업 문서: `docs/CODEX_TASK_1.12.md`
- 상태: 구현 및 검증 완료

## 완료된 주요 작업

- `price_alerts` CRUD API 구현
- 가격 알림 평가 API 구현
- `TARGET_PRICE_ABOVE`, `TARGET_PRICE_BELOW`, `DROP_FROM_HIGH`, `RISE_FROM_LOW` 조건 구현
- Gmail SMTP 실제 발송 연결 구현
- `alert_histories` sent / failed / skipped 기록 구현
- 동일 일자 중복 발송 skip 처리 구현
- Alerts 화면을 가격 알림 관리 화면으로 재구성
- Backend compile 성공
- Frontend build 성공

## 검증 결과

| 항목 | 결과 |
|---|---|
| 가격 알림 생성 | 성공 |
| 가격 알림 조회 | 성공 |
| 가격 알림 수정 | 성공 |
| 가격 알림 삭제 | 성공 |
| 목표가 이상 조건 | 성공 |
| 목표가 이하 조건 | 성공 |
| 고점 대비 하락률 조건 | 성공 |
| 저점 대비 상승률 조건 | 성공 |
| dry-run 평가 | 성공 |
| 실제 Gmail 발송 1건 | 성공 |
| 동일 일자 중복 발송 skip | 성공 |
| `/api/price-alerts/summary` | 200 |
| `/api/price-alerts/histories` | 200 |
| Backend compile | 성공 |
| Frontend build | 성공 |
| Regression API | 모두 200 |

## 확인 필요 항목

- 항목: `lookback_days` 저장 위치
- 관련 문서: `docs/CODEX_TASK_1.12.md`
- 애매한 이유: `price_alerts` 테이블에 전용 `lookback_days` 컬럼이 없음
- 가능한 선택지: `base_price` 재사용, 메모 문자열 저장, 새 컬럼 추가
- 추천안: 이번 작업에서는 마이그레이션 없이 `base_price`를 정수형 `lookback_days` 보관 용도로 재사용
- 현재 구현 여부: 반영

- 항목: 종목명 인코딩 깨짐
- 관련 문서: `docs/DEVELOPMENT_REPORT.md`
- 애매한 이유: DB 내 일부 종목명이 깨진 문자열로 남아 있어 알림 제목/본문에도 그대로 반영됨
- 가능한 선택지: KRX 원본 재정비, 종목명 정제 스크립트, 표시 레이어 보정
- 추천안: 별도 데이터 정비 작업으로 분리
- 현재 구현 여부: 보류

## 다음 작업 후보

- 가격 알림 생성 진입 버튼을 stocks / portfolio 화면으로 연결
- 가격 알림 발송 본문 템플릿 고도화
- 종목명 인코딩 정리
