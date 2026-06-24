# Codex 다음 작업 지시 프롬프트 v1.6

## 0. 작업 목표

이전 작업에서 다음 항목이 완료되었다.

- 네이버 금융 뉴스 수집 구조 구현
- 뉴스 API 및 뉴스 화면 연결
- GPT 요약 대상 산출 기준 구현
- GPT 요약/재필터링 API 구조 구현
- GPT 실제 요약 limit 1 성공
- GPT 재필터링은 OpenAI quota 부족으로 실패 처리 확인
- GPT 결과 검수 API 구현
- GPT 결과 수동 보정 UI 구현
- 뉴스 알림 후보 재계산/조회/요약 API 구현
- 뉴스 화면 알림 후보 UI 구현

이번 작업의 목표는 다음이다.

1. 뉴스 알림 후보를 기반으로 Gmail SMTP 발송 구조를 구현한다.
2. 실제 발송 전 dry-run 기능을 제공한다.
3. 발송 성공/실패 이력을 `alert_histories`에 기록한다.
4. 일별/시간별 발송 제한을 적용한다.
5. 같은 뉴스/종목에 대한 중복 발송을 방지한다.
6. 알림 관리 화면 또는 뉴스 화면에서 발송 결과를 확인할 수 있게 한다.

기준 문서:

```text
AGENTS.md
docs/INVESTMENT_SYSTEM_PLAN_v1.2.md
docs/MVP_DB_SCHEMA_v1.2.md
docs/DEVELOPMENT_REPORT.md
docs/GPT_NEWS_PROCESSING_REPORT.md
docs/NEWS_ALERT_CANDIDATE_REPORT.md
```

문서에 없는 기능은 임의로 추가하지 않는다.

---

## 1. 작업 전 확인 사항

작업 시작 전에 다음 문서를 읽는다.

```text
AGENTS.md
docs/INVESTMENT_SYSTEM_PLAN_v1.2.md
docs/MVP_DB_SCHEMA_v1.2.md
docs/DEVELOPMENT_REPORT.md
docs/GPT_NEWS_PROCESSING_REPORT.md
```

`docs/NEWS_ALERT_CANDIDATE_REPORT.md`가 있으면 함께 읽는다.

이번 작업에서는 기존 27개 MVP 테이블을 그대로 사용한다.

새 테이블을 추가하지 않는다.

알림 발송 이력은 기존 테이블을 사용한다.

```text
alert_histories
alert_settings
news
news_stock_links
stocks
```

---

## 2. Gmail SMTP 환경변수

### 2.1 사용할 환경변수

다음 환경변수를 사용한다.

```text
GMAIL_SMTP_HOST=smtp.gmail.com
GMAIL_SMTP_PORT=587
GMAIL_SMTP_USERNAME=
GMAIL_SMTP_APP_PASSWORD=
ALERT_RECIPIENT_EMAIL=
```

필요 시 `.env.example`에 예시를 추가한다.

### 2.2 주의

Gmail 일반 계정 비밀번호를 직접 사용하지 않는다.

Gmail 앱 비밀번호 또는 사용자가 제공한 SMTP 전용 비밀번호를 사용한다.

환경변수가 없으면 실제 발송은 하지 않고 명확한 오류 메시지를 반환한다.

---

## 3. Gmail SMTP client 구현

### 3.1 위치

다음 위치에 Gmail client를 구현한다.

```text
backend/app/external/gmail/
```

권장 파일:

```text
backend/app/external/gmail/client.py
backend/app/external/gmail/types.py
```

### 3.2 구현 기능

```text
- SMTP 연결
- TLS 시작
- 로그인
- 이메일 제목/본문 작성
- HTML 또는 plain text 발송
- timeout 처리
- 실패 예외 처리
```

### 3.3 발송 형식

처음에는 plain text 또는 간단한 HTML로 구현한다.

이메일에는 다음 정보를 포함한다.

```text
- 뉴스 제목
- 발행시각
- 출처
- 관련 종목
- 중요도 점수
- GPT 요약
- GPT 필터 결과
- GPT 필터 사유
- 원문 URL
- 시스템 상세 링크가 있으면 포함
```

---

## 4. 뉴스 알림 발송 API 구현

### 4.1 구현 API

다음 API를 구현한다.

```text
POST /api/news/alerts/send
POST /api/news/alerts/send/dry-run
GET  /api/news/alerts/histories
GET  /api/news/alerts/histories/summary
```

### 4.2 POST /api/news/alerts/send/dry-run

목적:

```text
실제 이메일을 보내지 않고, 발송 대상과 제한 적용 결과를 미리 확인한다.
```

요청 예시:

```json
{
  "limit": 20
}
```

응답에는 다음을 포함한다.

```text
- candidate_count
- sendable_count
- skipped_count
- skipped_reasons
- daily_sent_count
- hourly_sent_count
- would_send_items
```

### 4.3 POST /api/news/alerts/send

동작:

```text
1. alert_settings 조회
2. is_alert_target = true 인 뉴스 후보 조회
3. 이미 발송된 뉴스/종목 조합 제외
4. 일별/시간별 발송 제한 확인
5. Gmail SMTP 환경변수 확인
6. 이메일 발송
7. alert_histories에 성공/실패 기록
8. 결과 통계 반환
```

요청 예시:

```json
{
  "limit": 20,
  "force": false
}
```

주의:

```text
force = true여도 일별/시간별 제한은 무시하지 않는다.
force = true는 이미 failed였던 항목 재시도 정도로만 사용한다.
```

---

## 5. 발송 제한 정책

기준 문서의 제한을 따른다.

```text
일별 최대 200건
시간별 최대 50건
```

단, 실제 값은 `alert_settings` 값을 우선 사용한다.

사용 필드:

```text
alert_settings.max_daily_alerts
alert_settings.max_hourly_alerts
alert_settings.send_email
alert_settings.enabled
alert_settings.news_alert_enabled
```

### 5.1 제한 적용 방식

```text
- alert_settings.enabled = false이면 발송하지 않는다.
- alert_settings.news_alert_enabled = false이면 뉴스 알림을 발송하지 않는다.
- alert_settings.send_email = false이면 이메일 발송하지 않는다.
- 오늘 발송 성공 건수가 max_daily_alerts 이상이면 발송하지 않는다.
- 최근 1시간 발송 성공 건수가 max_hourly_alerts 이상이면 발송하지 않는다.
```

---

## 6. 중복 발송 방지

같은 뉴스/종목 조합은 중복 발송하지 않는다.

### 6.1 중복 기준

```text
news_id + stock_id + alert_type = "news"
```

`stock_id`가 없는 시장/매크로 뉴스는 다음 기준을 사용한다.

```text
news_id + alert_type = "news"
```

### 6.2 alert_histories 기록

발송 시 `alert_histories`에 기록한다.

사용 필드:

```text
news_id
stock_id
alert_type
recipient_email
title
message
link_url
status
sent_at
error_message
created_at
```

status 예시:

```text
pending
sent
failed
skipped
```

---

## 7. 발송 대상 선정

대상 뉴스:

```text
news.is_alert_target = true
```

추가 조건:

```text
- gpt_filter_result in ["important", "price_impact"] 이면 우선 발송
- gpt_filter_result가 없더라도 importance_score가 alert_settings.min_importance_score 이상이면 발송 후보
- duplicate_count/source_count 기준을 충족하면 발송 후보
```

대상 종목:

```text
news_stock_links로 연결된 종목
```

종목 링크가 없는 시장/매크로 뉴스도 발송 가능하게 한다.

---

## 8. Frontend 연결

대상 화면은 기존 구현 상황에 맞게 선택한다.

우선순위:

```text
1. frontend/src/pages/main/alerts/
2. 없거나 미완성이라면 frontend/src/pages/main/news/
```

### 8.1 구현 기능

다음 UI를 구현한다.

```text
- 알림 발송 후보 수 표시
- dry-run 버튼
- 실제 발송 버튼
- 일별 발송 건수 표시
- 시간별 발송 건수 표시
- 발송 이력 목록
- 발송 상태 필터
- 실패 사유 표시
```

### 8.2 주의

실제 발송 버튼은 사용자가 실수로 누르지 않도록 확인 confirm을 추가한다.

---

## 9. 테스트 항목

### 9.1 Backend 테스트

다음을 확인한다.

```text
- /api/news/alerts/send/dry-run 200 응답
- /api/news/alerts/send 환경변수 없을 때 명확한 400 오류
- Gmail 환경변수 있을 때 limit 1 실제 발송 성공
- alert_histories sent 기록 생성
- 실패 시 alert_histories failed 기록 생성
- 중복 발송 방지 확인
- 일별 제한 확인
- 시간별 제한 확인
- /api/news/alerts/histories 200 응답
- /api/news/alerts/histories/summary 200 응답
```

### 9.2 Frontend 테스트

다음을 확인한다.

```text
- 알림 화면 또는 뉴스 화면 접근
- dry-run 버튼 동작
- 실제 발송 버튼 confirm 표시
- 발송 이력 목록 조회
- 발송 상태 필터 동작
- Frontend build 성공
```

### 9.3 Regression

기존 기능이 깨지지 않았는지 확인한다.

```text
- /health
- /api/auth/status
- 설정 API
- 종목 API
- 수집 종목 관리 API
- 뉴스 목록/수집 API
- GPT dry-run API
- 알림 후보 API
- Frontend build
```

---

## 10. 문서 갱신

작업 완료 후 다음 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 다음 문서를 새로 작성한다.

```text
docs/NEWS_ALERT_SEND_REPORT.md
```

`NEWS_ALERT_SEND_REPORT.md`에는 다음 내용을 기록한다.

```markdown
# NEWS ALERT SEND REPORT

## 1. 작업 개요

## 2. 구현한 API

## 3. Gmail SMTP 구조

## 4. 발송 제한 정책

## 5. 중복 발송 방지 방식

## 6. Frontend 연결 결과

## 7. 테스트 결과

## 8. 확인 필요 항목

## 9. 다음 단계 제안
```

---

## 11. 완료 조건

이번 작업 완료 조건은 다음이다.

```text
- Gmail SMTP client 구조 구현
- 뉴스 알림 dry-run API 구현
- 뉴스 알림 실제 발송 API 구현
- alert_histories 성공/실패 기록 구현
- 일별/시간별 발송 제한 구현
- 중복 발송 방지 구현
- 알림 화면 또는 뉴스 화면 UI 연결
- Backend 테스트 통과
- Frontend build 통과
- CODEX_PROGRESS.md 갱신
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 사용자에게 다음과 같이 보고한다.

```text
뉴스 알림 Gmail 발송 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
