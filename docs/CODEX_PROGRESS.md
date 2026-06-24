# CODEX PROGRESS

## 현재 작업 상태

- 현재 단계: CODEX_TASK_1.6 뉴스 알림 Gmail 발송 구조 완료
- 마지막 작업 시간: 2026-06-24
- 전체 진행률: 100%
- 현재 작업 중인 파일: backend/app/domains/news/, backend/app/external/gmail/, frontend/src/pages/main/alerts/, docs/

## 완료한 작업

- [x] 기준 문서 확인
  - 설명: AGENTS.md, 투자 분석 시스템 계획서, MVP DB 스키마, 기존 개발 리포트, GPT 뉴스 처리 리포트, 뉴스 알림 후보 리포트를 기준으로 작업 범위를 확인했다.
  - 관련 파일: AGENTS.md, docs/INVESTMENT_SYSTEM_PLAN_v1.2.md, docs/MVP_DB_SCHEMA_v1.2.md, docs/DEVELOPMENT_REPORT.md, docs/GPT_NEWS_PROCESSING_REPORT.md, docs/NEWS_ALERT_CANDIDATE_REPORT.md

- [x] Gmail SMTP 설정 구조 추가
  - 설명: Gmail SMTP 사용자명, 앱 비밀번호, 알림 수신자 이메일 환경변수를 설정 구조와 예시 파일에 추가했다.
  - 관련 파일: backend/app/core/config.py, backend/.env.example

- [x] Gmail SMTP client 구현
  - 설명: STARTTLS 기반 SMTP 연결, 로그인, plain text 메일 발송 구조를 구현했다.
  - 관련 파일: backend/app/external/gmail/client.py, backend/app/external/gmail/types.py, backend/app/external/gmail/__init__.py

- [x] 뉴스 알림 dry-run API 구현
  - 설명: 실제 메일 발송 없이 발송 후보, 발송 가능 건수, 스킵 사유, 일별/시간별 발송 수를 확인하는 API를 구현했다.
  - 관련 파일: backend/app/domains/news/router.py, backend/app/domains/news/service.py, backend/app/domains/news/repository.py, backend/app/domains/news/schemas.py

- [x] 뉴스 알림 실제 발송 API 구현
  - 설명: alert_settings 기준으로 이메일 발송 가능 여부를 판단하고 Gmail SMTP 발송 성공/실패를 alert_histories에 기록하도록 구현했다.
  - 관련 파일: backend/app/domains/news/router.py, backend/app/domains/news/service.py, backend/app/domains/news/repository.py

- [x] 발송 제한 및 중복 방지 구현
  - 설명: 일별/시간별 발송 제한, 동일 news_id + stock_id + alert_type 기준 중복 발송 방지, 실패 이력 force 재시도 정책을 구현했다.
  - 관련 파일: backend/app/domains/news/service.py, backend/app/domains/news/repository.py

- [x] 발송 이력 조회 API 구현
  - 설명: alert_histories 목록 조회, status 필터, 요약 통계 API를 구현했다.
  - 관련 파일: backend/app/domains/news/router.py, backend/app/domains/news/service.py, backend/app/domains/news/repository.py

- [x] 알림 관리 화면 실제 API 연결
  - 설명: 알림 후보 수, 금일/최근 1시간 발송 수, 실패 수, dry-run, 실제 발송 confirm, 발송 이력 목록, 상태 필터 UI를 구현했다.
  - 관련 파일: frontend/src/pages/main/alerts/AlertsPage.vue, frontend/src/pages/main/alerts/service/alerts.api.ts, frontend/src/pages/main/alerts/service/alerts.types.ts

- [x] 테스트 및 회귀 검증
  - 설명: Backend compile, 주요 API 응답, dry-run 200, Gmail 설정 누락 시 send 400, 발송 이력 API 200, Frontend build를 확인했다.
  - 관련 파일: backend/, frontend/

- [x] Gmail SMTP 실제 발송 검증
  - 설명: Gmail SMTP 환경변수 로드 확인 후 `/api/news/alerts/send`를 실행해 실제 발송 성공 및 `alert_histories` sent 기록을 확인했다. 검증 중 요청 `limit`이 뉴스 단위가 아니라 발송 단위에 적용되도록 보정했다.
  - 관련 파일: backend/app/domains/news/service.py, docs/NEWS_ALERT_SEND_REPORT.md

- [x] 뉴스 알림 발송 리포트 작성
  - 설명: 구현 API, Gmail 구조, 발송 제한, 중복 방지, Frontend 연결, 테스트 결과, 확인 필요 항목을 문서화했다.
  - 관련 파일: docs/NEWS_ALERT_SEND_REPORT.md

## 진행 중인 작업

- [x] CODEX_TASK_1.6 작업 완료
  - 현재 상태: 구현 및 검증 완료
  - 남은 작업: 없음

## 남은 작업

- [ ] OpenAI quota/billing 확인 후 GPT 필터 limit 1 재검증
- [ ] KRX 가격 데이터 수집 구조 구현

## 막힌 항목

- 항목: 없음
- 원인: 없음
- 필요한 확인: 없음

## 생성한 파일

- 파일 경로: backend/app/external/gmail/types.py
- 설명: Gmail 발송 메시지 타입
- 파일 경로: docs/NEWS_ALERT_SEND_REPORT.md
- 설명: 뉴스 알림 Gmail 발송 구조 작업 리포트

## 수정한 파일

- 파일 경로: backend/app/core/config.py
- 수정 내용: Gmail SMTP 환경변수 추가
- 파일 경로: backend/.env.example
- 수정 내용: Gmail SMTP 환경변수 예시 추가
- 파일 경로: backend/app/external/gmail/client.py
- 수정 내용: Gmail SMTP client 구현
- 파일 경로: backend/app/external/gmail/__init__.py
- 수정 내용: Gmail client/type export
- 파일 경로: backend/app/domains/news/
- 수정 내용: 뉴스 알림 발송 dry-run, 실제 발송, 발송 이력 API 구현
- 파일 경로: frontend/src/pages/main/alerts/
- 수정 내용: 알림 관리 화면 실제 API 연결
- 파일 경로: docs/DEVELOPMENT_REPORT.md
- 수정 내용: CODEX_TASK_1.6 결과 반영

## 확인 필요 항목

- 항목: Gmail SMTP 실제 발송 운영 확인
- 이유: 개발 환경에서 실제 발송과 sent 이력 기록은 확인했으나, 운영 수신 정책과 발송 빈도는 별도 확인이 필요하다.
- 제안: 알림 수신 메일함에서 도착 여부를 확인하고 `alert_settings`의 일별/시간별 제한값을 운영 기준에 맞게 조정한다.

- 항목: OpenAI quota/billing
- 이유: GPT 필터 실제 호출에서 `insufficient_quota` 오류가 발생했다.
- 제안: OpenAI billing/quota 복구 후 GPT 필터 limit 1부터 재검증한다.
