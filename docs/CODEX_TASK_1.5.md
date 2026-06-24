# Codex 다음 작업 지시 프롬프트 v1.5

## 0. 작업 목표

이전 작업에서 다음 항목이 완료되었다.

- 네이버 금융 실제 운영 수집 검증
- parser 보정
- 뉴스 저장/중복 처리/news_stock_links 생성
- GPT 요약 대상 산출 기준 구현
- GPT 요약 dry-run API 구현
- GPT 재필터링 dry-run API 구현
- API key 누락 시 안전한 오류 처리
- 뉴스 화면 GPT 상태/필터/상세 UI 연결

이번 작업의 목표는 다음이다.

1. OpenAI 환경변수 설정 상태를 점검한다.
2. GPT 요약을 실제 소량 실행한다.
3. GPT 재필터링을 실제 소량 실행한다.
4. 결과 품질을 검토할 수 있는 검수 API와 화면 보조 기능을 만든다.
5. 뉴스 알림 후보 산출 구조를 구현한다.
6. 실제 Gmail 발송은 아직 구현하지 않고, 알림 후보까지만 만든다.

기준 문서:

```text
AGENTS.md
docs/INVESTMENT_SYSTEM_PLAN_v1.2.md
docs/MVP_DB_SCHEMA_v1.2.md
docs/DEVELOPMENT_REPORT.md
docs/GPT_NEWS_PROCESSING_REPORT.md
docs/NEWS_COLLECTION_REPORT.md
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

이번 작업에서는 기존 27개 MVP 테이블을 그대로 사용한다.

DB 테이블을 새로 추가하지 않는다.

필요 데이터는 기존 테이블의 다음 필드를 사용한다.

```text
news.gpt_summary
news.gpt_summary_model
news.gpt_summary_status
news.gpt_summary_at
news.gpt_filter_result
news.gpt_filter_reason
news.gpt_filter_model
news.gpt_filter_at
news.is_gpt_summary_target
news.is_alert_target
news.importance_score
news.duplicate_count
news.source_count
news.event_type
news.market_scope
news.filter_status

alert_settings
alert_histories
news_stock_links
stocks
```

---

## 2. OpenAI 환경변수 점검

### 2.1 사용할 환경변수

다음 값을 사용한다.

```text
OPENAI_API_KEY
OPENAI_NEWS_SUMMARY_MODEL
OPENAI_NEWS_FILTER_MODEL
```

### 2.2 구현 항목

다음 기능을 구현하거나 기존 구현을 보완한다.

```text
- OpenAI 환경변수 존재 여부 확인
- 모델명 누락 시 명확한 오류 반환
- API key 누락 시 명확한 오류 반환
- dry_run=true이면 API key가 없어도 대상 목록 확인 가능
- dry_run=false이면 API key와 모델명이 모두 있어야 실행
```

### 2.3 주의

실제 API 호출은 비용이 발생할 수 있으므로 기본 limit은 작게 둔다.

```text
기본 limit:
- summary run: 5
- filter run: 5
```

---

## 3. GPT 요약 실제 소량 실행 검증

### 3.1 대상 API

```text
POST /api/news/gpt/summary/run
```

### 3.2 요청 예시

```json
{
  "limit": 5,
  "dry_run": false
}
```

### 3.3 검증 항목

다음을 확인한다.

```text
- is_gpt_summary_target = true 대상 조회
- gpt_summary_status = pending 또는 failed 대상 조회
- OpenAI 호출 성공 여부
- gpt_summary 저장 여부
- gpt_summary_model 저장 여부
- gpt_summary_status = done 저장 여부
- gpt_summary_at 저장 여부
- 실패 시 gpt_summary_status = failed 저장 여부
```

### 3.4 요약 품질 기준

요약은 너무 길게 만들지 않는다.

권장 기준:

```text
- 200~300자 내외
- 투자 판단에 필요한 핵심만 요약
- 단순 반복 제목 요약 금지
- 관련 종목, 이벤트, 수혜/리스크, 확인 필요 사항 중심
```

---

## 4. GPT 재필터링 실제 소량 실행 검증

### 4.1 대상 API

```text
POST /api/news/gpt/filter/run
```

### 4.2 요청 예시

```json
{
  "limit": 5,
  "dry_run": false
}
```

### 4.3 분류값

`gpt_filter_result`는 다음 값만 사용한다.

```text
important
price_impact
unnecessary
failed
```

### 4.4 검증 항목

다음을 확인한다.

```text
- gpt_summary_status = done 또는 content_preview/original_summary가 있는 뉴스 조회
- gpt_filter_result가 비어 있는 대상 조회
- OpenAI 호출 성공 여부
- gpt_filter_result 저장 여부
- gpt_filter_reason 저장 여부
- gpt_filter_model 저장 여부
- gpt_filter_at 저장 여부
```

### 4.5 품질 기준

재필터링 판단은 다음 관점으로 한다.

```text
important:
- 실적, 수주, 공시, 증자, 배당, 자사주, 정책, 규제, 기술, 소송, 제재 등 투자 판단 핵심 뉴스

price_impact:
- 단기 주가 영향은 가능하지만 핵심 펀더멘털 판단까지는 약한 뉴스

unnecessary:
- 단순 특징주
- 광고성 기사
- 사진/행사/봉사활동
- 중복성이 높지만 내용 가치가 낮은 기사
- 종목 관련성이 약한 기사
```

---

## 5. GPT 결과 검수 API 구현

### 5.1 목적

초기 GPT 결과 품질을 사람이 확인할 수 있도록 검수용 API를 만든다.

### 5.2 구현 API

```text
GET   /api/news/gpt/review
PATCH /api/news/gpt/review/{news_id}
```

### 5.3 GET /api/news/gpt/review

지원 필터:

```text
gpt_summary_status
gpt_filter_result
min_importance_score
stock_code
keyword
published_from
published_to
```

응답에는 다음을 포함한다.

```text
news_id
title
source
published_at
related_stocks
importance_score
duplicate_count
source_count
gpt_summary
gpt_filter_result
gpt_filter_reason
is_alert_target
```

### 5.4 PATCH /api/news/gpt/review/{news_id}

수동 보정 가능한 필드:

```text
gpt_filter_result
gpt_filter_reason
is_alert_target
filter_status
```

주의:

```text
새 테이블을 추가하지 않는다.
수동 검수 이력 테이블은 이번 범위에 포함하지 않는다.
```

---

## 6. 뉴스 화면 GPT 검수 기능 보완

대상 화면:

```text
frontend/src/pages/main/news/
```

### 6.1 구현 기능

다음 기능을 추가한다.

```text
- GPT 검수 목록 필터
- GPT 결과 수동 보정 UI
- is_alert_target 수동 체크/해제
- filter_status 수동 변경
- GPT 요약/재필터 결과 비교 표시
```

### 6.2 주의

이번 단계에서는 복잡한 별도 검수 화면을 만들지 않아도 된다.

기존 뉴스 화면의 상세 drawer 또는 테이블 action으로 구현해도 된다.

---

## 7. 뉴스 알림 후보 산출 구조 구현

### 7.1 목적

실제 Gmail 발송 전 단계로, 어떤 뉴스가 알림 후보인지 산출한다.

이번 단계에서는 이메일을 보내지 않는다.

### 7.2 알림 후보 기준

다음 조건 중 하나 이상이면 `news.is_alert_target = true`로 설정한다.

```text
importance_score >= alert_settings.min_importance_score
duplicate_count >= alert_settings.min_duplicate_count
source_count >= alert_settings.min_source_count
gpt_filter_result in ["important", "price_impact"]
event_type in alert_settings.event_types_json
```

추가 가중 조건:

```text
- 보유종목 관련 뉴스
- 관심종목 관련 뉴스
- 가격 알림 설정 종목 관련 뉴스
```

위 조건은 가능한 경우 반영한다.

### 7.3 구현 API

```text
POST /api/news/alerts/candidates/recalculate
GET  /api/news/alerts/candidates
GET  /api/news/alerts/summary
```

### 7.4 POST /api/news/alerts/candidates/recalculate

동작:

```text
1. alert_settings 조회
2. news와 news_stock_links 조회
3. 중요도, 중복, source_count, GPT 필터 결과, event_type 기준으로 후보 산출
4. news.is_alert_target 갱신
5. 결과 통계 반환
```

### 7.5 GET /api/news/alerts/candidates

지원 필터:

```text
stock_code
gpt_filter_result
min_importance_score
published_from
published_to
```

응답에는 다음을 포함한다.

```text
news_id
title
source
published_at
related_stocks
importance_score
duplicate_count
source_count
gpt_filter_result
gpt_filter_reason
is_alert_target
```

### 7.6 주의

이번 단계에서는 `alert_histories`를 생성하지 않는다.

Gmail SMTP 실제 발송은 후속 단계에서 구현한다.

---

## 8. 테스트 항목

### 8.1 Backend 테스트

다음을 확인한다.

```text
- /api/news/gpt/targets 200 응답
- /api/news/gpt/status 200 응답
- /api/news/gpt/summary/run dry_run=true 성공
- /api/news/gpt/filter/run dry_run=true 성공
- API key 없을 때 dry_run=false 명확한 400 오류
- API key가 있으면 summary limit 5 실제 실행 성공
- API key가 있으면 filter limit 5 실제 실행 성공
- /api/news/gpt/review 200 응답
- /api/news/gpt/review/{news_id} PATCH 성공
- /api/news/alerts/candidates/recalculate 성공
- /api/news/alerts/candidates 200 응답
- /api/news/alerts/summary 200 응답
```

### 8.2 Frontend 테스트

다음을 확인한다.

```text
- 뉴스 화면 접근
- GPT 상태 KPI 표시
- GPT 검수 필터 동작
- GPT 결과 수동 보정 동작
- 알림 후보 재계산 버튼 동작
- 알림 후보 필터 동작
- 뉴스 상세 drawer 정상 표시
- npm run build 성공
```

### 8.3 Regression

기존 기능이 깨지지 않았는지 확인한다.

```text
- /health
- /api/auth/status
- 설정 API
- 종목 API
- 수집 종목 관리 API
- 뉴스 목록/수집 API
- GPT dry-run API
- Frontend build
```

---

## 9. 문서 갱신

작업 완료 후 다음 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
docs/GPT_NEWS_PROCESSING_REPORT.md
```

필요 시 다음 문서를 새로 작성한다.

```text
docs/NEWS_ALERT_CANDIDATE_REPORT.md
```

`NEWS_ALERT_CANDIDATE_REPORT.md`에는 다음 내용을 기록한다.

```markdown
# NEWS ALERT CANDIDATE REPORT

## 1. 작업 개요

## 2. 구현한 API

## 3. 알림 후보 산출 기준

## 4. GPT 검수 기능

## 5. Frontend 연결 결과

## 6. 테스트 결과

## 7. 확인 필요 항목

## 8. 다음 단계 제안
```

---

## 10. 완료 조건

이번 작업 완료 조건은 다음이다.

```text
- OpenAI 환경변수 점검 구조 보완
- GPT 실제 호출 소량 실행 또는 API key 부재 시 확인 필요 항목 기록
- GPT 결과 검수 API 구현
- GPT 결과 수동 보정 UI 구현
- 뉴스 알림 후보 산출 API 구현
- 뉴스 알림 후보 조회 API 구현
- 뉴스 화면 알림 후보 UI 보완
- Backend 테스트 통과
- Frontend build 통과
- CODEX_PROGRESS.md 갱신
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 사용자에게 다음과 같이 보고한다.

```text
GPT 실제 검증 및 뉴스 알림 후보 산출 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
