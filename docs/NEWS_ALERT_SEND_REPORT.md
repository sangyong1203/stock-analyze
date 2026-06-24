# NEWS ALERT SEND REPORT

## 1. 작업 개요

- 작업 목표: 뉴스 알림 후보를 기반으로 Gmail SMTP 발송 구조, dry-run, 발송 이력 기록, 발송 제한, 중복 발송 방지를 구현했다.
- 기준 문서: AGENTS.md, INVESTMENT_SYSTEM_PLAN_v1.2.md, MVP_DB_SCHEMA_v1.2.md, DEVELOPMENT_REPORT.md, GPT_NEWS_PROCESSING_REPORT.md, NEWS_ALERT_CANDIDATE_REPORT.md
- DB 변경: 신규 테이블은 추가하지 않았고 기존 `alert_histories`, `alert_settings`, `news`, `news_stock_links`, `stocks`를 사용했다.

## 2. 구현한 API

| Method | Path | 설명 |
| ------ | ---- | ---- |
| POST | `/api/news/alerts/send/dry-run` | 실제 발송 없이 발송 가능 후보, 제한 적용 결과, 스킵 사유를 확인 |
| POST | `/api/news/alerts/send` | Gmail SMTP 실제 발송 및 `alert_histories` 성공/실패 기록 |
| GET | `/api/news/alerts/histories` | 뉴스 알림 발송 이력 조회, `status` 필터 지원 |
| GET | `/api/news/alerts/histories/summary` | 전체/성공/실패/스킵/금일/최근 1시간 발송 통계 조회 |

## 3. Gmail SMTP 구조

- 위치: `backend/app/external/gmail/`
- Client: `GmailSmtpClient`
- Message type: `GmailMessage`
- 방식: SMTP 연결, STARTTLS, 로그인, plain text 이메일 발송
- 환경변수:
  - `GMAIL_SMTP_HOST`
  - `GMAIL_SMTP_PORT`
  - `GMAIL_SMTP_USERNAME`
  - `GMAIL_SMTP_APP_PASSWORD`
  - `ALERT_RECIPIENT_EMAIL`
- 필수 환경변수가 없으면 실제 발송 API는 400 오류를 반환한다.

## 4. 발송 제한 정책

`alert_settings` 값을 우선 사용한다.

- `enabled = false`: 발송하지 않음
- `news_alert_enabled = false`: 뉴스 알림 발송하지 않음
- `send_email = false`: 이메일 발송하지 않음
- `max_daily_alerts`: 금일 성공 발송 건수 기준 제한
- `max_hourly_alerts`: 최근 1시간 성공 발송 건수 기준 제한

`force = true`여도 일별/시간별 제한은 무시하지 않는다.

## 5. 중복 발송 방지 방식

- 종목 연결 뉴스: `news_id + stock_id + alert_type = "news"` 기준으로 `sent` 이력이 있으면 제외한다.
- 시장/매크로 뉴스: `news_id + alert_type = "news"` 기준으로 `sent` 이력이 있으면 제외한다.
- `failed` 이력은 기본적으로 제외하고, `force = true`일 때만 재시도 대상에 포함한다.
- 발송 성공/실패는 `alert_histories`에 기록한다.

## 6. Frontend 연결 결과

- 대상 화면: `frontend/src/pages/main/alerts/AlertsPage.vue`
- 구현 기능:
  - 알림 후보 수 표시
  - dry-run 버튼
  - 실제 발송 버튼 및 confirm
  - 금일/최근 1시간 발송 건수 표시
  - 발송 이력 목록
  - 발송 상태 필터
  - 실패 사유 표시

## 7. 테스트 결과

- Backend compile: `python -m compileall app` 성공
- `/api/news/alerts/send/dry-run`: 200 응답, candidate 3, sendable 3 확인
- `/api/news/alerts/send`: Gmail 환경변수 설정 후 실제 SMTP 발송 성공
- 실제 발송 결과: sent 2, failed 0, `alert_histories` sent 2건 기록
- Gmail 환경변수 미설정 상태에서는 400 응답과 `Missing Gmail SMTP settings: GMAIL_SMTP_USERNAME, GMAIL_SMTP_APP_PASSWORD, ALERT_RECIPIENT_EMAIL` 오류 메시지를 확인했다.
- `/api/news/alerts/histories`: 200 응답
- `/api/news/alerts/histories/summary`: 200 응답
- 요청 `limit` 보정: 검증 중 `limit: 1` 요청에서 같은 뉴스의 연결 종목 2건이 발송되는 동작을 확인했고, 이후 발송 단위 기준으로 제한되도록 보정했다.
- Regression: `/health`, `/api/auth/status`, `/api/settings`, `/api/stocks`, `/api/collection/stocks/summary`, `/api/news`, `/api/news/summary`, GPT targets, 알림 후보 API 200 응답 확인
- Frontend build: `npm run build` 성공

## 8. 확인 필요 항목

- 항목: Gmail 수신 확인
- 이유: SMTP 발송 API와 sent 이력 기록은 성공했으나, 실제 메일함 도착 여부는 수신함에서 확인해야 한다.
- 제안: `ALERT_RECIPIENT_EMAIL` 메일함에서 뉴스 알림 메일 2건 도착 여부를 확인한다.

- 항목: 발송 제한 운영값
- 이유: 현재 제한은 `alert_settings` 기본값을 사용한다.
- 제안: 실제 운영 빈도에 맞춰 `max_daily_alerts`, `max_hourly_alerts`를 설정 화면에서 조정한다.

## 9. 다음 단계 제안

- `alert_histories` sent/failed 이력 기반 UI 개선
- KRX 가격 데이터 수집 구조 구현
