# CODEX_TASK_2.1

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

MVP 1차 완료 정리는 끝났습니다.
이번 작업부터는 Phase 2입니다.

이번 작업은 **실사용 운영 준비 / 환경변수 점검 / DB 백업 전략 / 첫 운영 전 점검**입니다.

## 목표

1. 실제 사용 전에 필요한 환경 설정 상태를 점검한다.
2. Gmail, OpenAI, KRX, SQLite DB 백업 준비 상태를 확인한다.
3. 민감 정보는 출력하지 않는다.
4. 운영 전 체크리스트 문서를 만든다.
5. 새 기능 추가는 하지 않는다.
6. 새 테이블과 마이그레이션은 만들지 않는다.
7. 실제 Gmail 발송은 하지 않는다.

## 작업 전 확인

직전 문서만 확인한다.

```text
docs/DEVELOPMENT_REPORT.md
docs/MVP_COMPLETION_REPORT.md
```

기준 문서를 반복해서 다시 읽지 않는다.

## 점검 대상

### 1. 환경변수 점검

Backend `.env` 또는 설정 로딩 구조에서 아래 항목이 준비되어 있는지 확인한다.

```text
Gmail SMTP 관련
- SMTP_HOST
- SMTP_PORT
- SMTP_USERNAME
- SMTP_PASSWORD
- SMTP_FROM_EMAIL

OpenAI 관련
- OPENAI_API_KEY
- 사용할 모델 설정값

KRX 관련
- KRX_AUTH_KEY

DB 관련
- SQLite DB 경로
- 백업 대상 DB 경로

Frontend 관련
- API base URL
- localhost / 127.0.0.1 CORS 설정
```

주의:

```text
- 실제 key 값은 출력하지 않는다.
- 존재 여부만 true/false 또는 configured/missing으로 기록한다.
- 민감 정보 일부 마스킹도 가능하면 하지 않는다.
- 누락 항목은 운영 전 체크리스트에 기록한다.
```

### 2. 설정 로딩 검증

현재 backend 설정 구조가 다음을 지원하는지 확인한다.

```text
- localhost / 127.0.0.1 CORS 허용 유지
- allowed_origin 기존 호환 유지
- allowed_origins 다중 origin 유지
- Gmail SMTP 설정 로딩
- OpenAI 설정 로딩
- KRX auth key 설정 로딩
```

문제가 있으면 최소 수정한다.

단, 새 기능으로 확장하지 않는다.

### 3. DB 백업 전략 정리

SQLite 운영 전 백업 방식을 정리한다.

필요 시 간단한 백업 스크립트 또는 명령어 문서를 작성한다.

우선순위:

```text
1. 수동 백업 명령어 문서화
2. 백업 파일명 규칙 정리
3. 백업 보관 위치 정리
4. 복구 명령어 정리
```

예시 형식:

```text
storage/backups/stock_analyze_YYYYMMDD_HHMMSS.db
```

주의:

```text
- DB schema 변경 금지
- migration 추가 금지
- 운영 DB 삭제/초기화 금지
```

### 4. 운영 전 dry-run 확인

실제 발송 없이 아래 항목을 확인한다.

```text
- /api/jobs/summary
- /api/prices/summary
- /api/news/summary
- /api/price-alerts/summary
- /api/news/alerts/send/dry-run
- /api/price-alerts/evaluate/dry-run
```

실제 Gmail 발송성 API는 실행하지 않는다.

### 5. 운영 데이터 입력 전 체크리스트 작성

첫 실사용 전 사용자가 직접 확인해야 할 항목을 정리한다.

포함할 것:

```text
- 실제 보유 현금 입력 전 DB 백업
- fund pool 생성 기준
- 과거 거래를 어디까지 입력할지 기준
- 보유 종목 평균단가 입력 방식
- 알림 조건을 실제 발송 전에 dry-run으로 확인
- 뉴스 알림은 후보 확인 후 발송
- Gmail 발송은 limit 1 테스트 후 확대
```

## 생성 문서

다음 문서를 작성한다.

```text
docs/OPERATION_READY_CHECKLIST.md
```

구성:

```markdown
# OPERATION READY CHECKLIST

## 1. 목적

## 2. 환경변수 점검 결과

## 3. Gmail SMTP 준비 상태

## 4. OpenAI API 준비 상태

## 5. KRX API 준비 상태

## 6. SQLite DB 백업 전략

## 7. 운영 전 dry-run 점검 결과

## 8. 첫 운영 데이터 입력 순서

## 9. 알림 발송 안전 수칙

## 10. 보류 / 확인 필요 항목
```

## DEVELOPMENT_REPORT.md 갱신

이번 작업 결과만 짧게 정리한다.

포함 내용:

```text
- CODEX_TASK_2.1 완료
- 운영 전 환경변수 점검 결과
- DB 백업 전략 문서 작성
- dry-run 점검 결과
- 새 기능 / 새 테이블 / 새 마이그레이션 없음
- 실제 Gmail 발송 없음
```

## 검증

Backend:

```bash
cd backend
python -m compileall app
```

필요 시 Frontend:

```bash
cd frontend
npm run build
```

Regression API:

```text
/health
/api/auth/status
/api/jobs/summary
/api/prices/summary
/api/news/summary
/api/price-alerts/summary
```

Dry-run API:

```text
/api/news/alerts/send/dry-run
/api/price-alerts/evaluate/dry-run
```

## 금지 사항

```text
- 실제 Gmail 발송 금지
- 실제 운영 데이터 임의 입력 금지
- 실제 보유 종목/거래 데이터 생성 금지
- 새 기능 추가 금지
- 새 테이블 생성 금지
- 새 마이그레이션 생성 금지
- API key 값 출력 금지
- SMTP password 출력 금지
```

## 완료 보고

작업 완료 후 다음과 같이 보고하세요.

```text
CODEX_TASK_2.1 실사용 운영 준비 점검 작업 완료했습니다.
DEVELOPMENT_REPORT.md와 OPERATION_READY_CHECKLIST.md를 확인해 주세요.
```
