# Codex 다음 작업 지시 프롬프트 v1.4

## 0. 작업 목표

이전 작업에서 다음 항목이 완료되었다.

- KODEX 200 / KODEX 코스닥150 실제 XLS import 검증
- 수집 종목 관리 API 구현
- 최종 수집 대상 재계산 로직 구현
- 수집 종목 관리 화면 API 연결
- 네이버 금융 뉴스 client/parser/type 구조 구현
- 뉴스 수집 API 구현
- 뉴스 중복 처리 구현
- 수집 대상 종목 매칭 구현
- news_stock_links 저장 구현
- 뉴스 화면 실제 API 연결

이번 작업의 목표는 다음이다.

1. 네이버 금융 뉴스 실제 운영 수집을 실행하고 parser를 검증/보정한다.
2. GPT 요약 대상 뉴스 산출 기준을 구현한다.
3. OpenAI GPT mini 기반 뉴스 요약 job 구조를 구현한다.
4. GPT-5 계열 모델 기반 뉴스 재필터링 job 구조를 구현한다.
5. 뉴스 화면에서 GPT 요약/필터링 상태를 확인할 수 있도록 보완한다.

기준 문서:

```text
AGENTS.md
docs/INVESTMENT_SYSTEM_PLAN_v1.2.md
docs/MVP_DB_SCHEMA_v1.2.md
docs/DEVELOPMENT_REPORT.md
docs/COLLECTION_TARGET_REPORT.md
docs/SCHEMA_VALIDATION_REPORT.md
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
docs/COLLECTION_TARGET_REPORT.md
docs/NEWS_COLLECTION_REPORT.md
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
```

---

## 2. 네이버 금융 실제 운영 수집 검증

### 2.1 목적

이전 작업에서 구현한 네이버 금융 뉴스 수집 구조가 실제 네이버 금융 HTML에서 안정적으로 동작하는지 확인한다.

### 2.2 실행 대상

기본 URL:

```text
https://finance.naver.com/news/news_list.naver
```

실행 API:

```text
POST /api/news/collect/market
```

요청 예시:

```json
{
  "pages": 1,
  "max_items": 50
}
```

### 2.3 검증 항목

다음을 확인한다.

```text
- 실제 네이버 금융 뉴스 목록 요청 성공 여부
- HTML parser가 제목, URL, 언론사, 발행시각, preview를 정상 추출하는지
- URL 정규화 정상 여부
- title 정규화 정상 여부
- url_hash/title_hash 생성 정상 여부
- news row 생성 또는 중복 갱신 정상 여부
- news_stock_links 생성 정상 여부
- news_collect_jobs 생성 및 status 갱신 정상 여부
- news_collect_job_items 생성 정상 여부
```

### 2.4 parser 보정

실제 HTML 구조에서 누락되는 케이스가 있으면 parser를 보완한다.

수정 위치:

```text
backend/app/external/naver/parser.py
backend/app/external/naver/news_client.py
```

단, 네이버 금융 이외의 뉴스 사이트 크롤링은 이번 범위에 포함하지 않는다.

---

## 3. GPT 요약 대상 산출 기준 구현

### 3.1 목적

모든 뉴스에 GPT를 호출하지 않고, 중요도가 높은 뉴스만 요약 대상으로 지정한다.

### 3.2 대상 기준

다음 조건 중 하나 이상이면 `is_gpt_summary_target = true`로 설정한다.

```text
importance_score >= 6
duplicate_count >= 3
source_count >= 3
event_type in ["earnings", "disclosure", "contract", "supply_contract", "rights_issue", "bonus_issue", "buyback", "dividend", "capacity_expansion", "mna", "legal_risk", "technology"]
is_alert_target = true
```

조건에 해당하지 않으면 `is_gpt_summary_target = false`로 둔다.

### 3.3 상태값

GPT 요약 전 기본 상태는 다음처럼 둔다.

```text
gpt_summary_status = "pending"
```

요약 대상이 아니면 다음 중 하나를 사용한다.

```text
gpt_summary_status = "skipped"
```

---

## 4. OpenAI GPT mini 요약 job 구조 구현

### 4.1 목적

`is_gpt_summary_target = true`인 뉴스에 대해 GPT mini 요약을 수행하는 job 구조를 만든다.

이번 단계에서는 환경변수가 없으면 실제 호출을 실행하지 않고, `확인 필요 항목`으로 기록한다.

### 4.2 외부 client 위치

다음 위치를 사용한다.

```text
backend/app/external/openai/
```

권장 파일:

```text
backend/app/external/openai/client.py
backend/app/external/openai/types.py
```

### 4.3 환경변수

다음 환경변수를 사용한다.

```text
OPENAI_API_KEY
OPENAI_NEWS_SUMMARY_MODEL
OPENAI_NEWS_FILTER_MODEL
```

기본 모델명은 `.env.example`에만 예시로 작성한다.

실제 모델명은 사용자가 확정하기 전까지 코드에 강하게 고정하지 않는다.

### 4.4 요약 입력

요약 입력에는 다음 값을 사용한다.

```text
title
source
published_at
original_summary
content_preview
matched_keywords_json
related stock names
importance_score
duplicate_count
source_count
event_type
market_scope
```

### 4.5 요약 결과 저장

요약 성공 시 다음 필드를 갱신한다.

```text
gpt_summary
gpt_summary_model
gpt_summary_status = "done"
gpt_summary_at
```

실패 시:

```text
gpt_summary_status = "failed"
```

실패 사유는 가능하면 system_logs 또는 job 결과에 기록한다.

---

## 5. GPT-5 재필터링 job 구조 구현

### 5.1 목적

GPT mini 요약 결과 또는 원문 preview를 기반으로 뉴스의 투자 중요도를 다시 분류한다.

### 5.2 분류값

`gpt_filter_result`는 다음 값 중 하나를 사용한다.

```text
important
price_impact
unnecessary
```

### 5.3 판단 기준

다음 관점으로 분류한다.

```text
- 투자 판단에 중요한가
- 특정 종목의 실적/수주/증자/정책/기술/리스크와 관련 있는가
- 단순 주가 급등락/특징주 기사인가
- 광고/행사/사진/봉사활동성 기사인가
- 시장/섹터 방향성에 영향을 줄 수 있는가
```

### 5.4 저장 필드

재필터링 성공 시 다음 필드를 갱신한다.

```text
gpt_filter_result
gpt_filter_reason
gpt_filter_model
gpt_filter_at
```

---

## 6. GPT job API 구현

다음 API를 구현한다.

```text
POST /api/news/gpt/summary/run
POST /api/news/gpt/filter/run
GET  /api/news/gpt/targets
GET  /api/news/gpt/status
```

### 6.1 POST /api/news/gpt/summary/run

요청 예시:

```json
{
  "limit": 20,
  "dry_run": false
}
```

동작:

```text
1. is_gpt_summary_target = true 인 뉴스 중 gpt_summary_status가 pending/failed인 항목 조회
2. OPENAI_API_KEY 존재 여부 확인
3. dry_run=true이면 실제 호출 없이 대상 목록만 반환
4. dry_run=false이고 API key가 있으면 GPT mini 요약 호출
5. 결과를 news 테이블에 저장
```

API key가 없으면 실제 호출하지 말고 명확한 오류 메시지를 반환한다.

### 6.2 POST /api/news/gpt/filter/run

요청 예시:

```json
{
  "limit": 20,
  "dry_run": false
}
```

동작:

```text
1. gpt_summary_status = done 이거나 content_preview가 있는 뉴스 조회
2. gpt_filter_result가 비어 있는 항목을 대상으로 처리
3. dry_run=true이면 실제 호출 없이 대상 목록만 반환
4. dry_run=false이고 API key가 있으면 GPT-5 계열 모델 호출
5. 결과를 news 테이블에 저장
```

### 6.3 GET /api/news/gpt/targets

응답에는 다음을 포함한다.

```text
- summary_pending_count
- summary_done_count
- summary_failed_count
- filter_pending_count
- filter_done_count
- filter_failed_count
```

### 6.4 GET /api/news/gpt/status

최근 처리 상태와 통계를 반환한다.

```text
- total_news_count
- gpt_summary_target_count
- gpt_summary_done_count
- gpt_filter_done_count
- important_count
- price_impact_count
- unnecessary_count
```

---

## 7. 뉴스 화면 보완

대상 화면:

```text
frontend/src/pages/main/news/
```

### 7.1 구현 기능

다음 기능을 추가한다.

```text
- GPT 요약 대상 필터
- GPT 요약 상태 필터
- GPT 필터 결과 필터
- GPT 요약 실행 dry-run 버튼
- GPT 요약 실행 버튼
- GPT 재필터 dry-run 버튼
- GPT 재필터 실행 버튼
- GPT 처리 통계 KPI 표시
```

### 7.2 목록 컬럼 보완

뉴스 목록에 다음 컬럼을 표시한다.

```text
- GPT 요약 상태
- GPT 필터 결과
- GPT 요약 대상 여부
```

### 7.3 상세 drawer 보완

뉴스 상세에 다음을 표시한다.

```text
- GPT 요약
- GPT 요약 모델
- GPT 요약 시간
- GPT 필터 결과
- GPT 필터 사유
- GPT 필터 모델
- GPT 필터 시간
```

---

## 8. 테스트 항목

### 8.1 Backend 테스트

다음을 확인한다.

```text
- 실제 네이버 금융 뉴스 수집 실행
- parser 추출 결과 확인
- news row 생성 확인
- 중복 재수집 시 duplicate_count 증가 확인
- news_stock_links 생성 확인
- GPT 요약 대상 산출 확인
- /api/news/gpt/targets 200 응답
- /api/news/gpt/status 200 응답
- summary dry_run 정상 동작
- filter dry_run 정상 동작
- OPENAI_API_KEY가 없을 때 명확한 오류 반환
```

### 8.2 Frontend 테스트

다음을 확인한다.

```text
- 뉴스 화면 접근
- GPT 상태 KPI 표시
- GPT 필터 UI 동작
- GPT dry-run 버튼 동작
- 뉴스 상세 drawer에 GPT 필드 표시
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
- Frontend build
```

---

## 9. 문서 갱신

작업 완료 후 다음 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 다음 문서를 새로 작성한다.

```text
docs/GPT_NEWS_PROCESSING_REPORT.md
```

`GPT_NEWS_PROCESSING_REPORT.md`에는 다음 내용을 기록한다.

```markdown
# GPT NEWS PROCESSING REPORT

## 1. 작업 개요

## 2. 구현한 API

## 3. GPT 요약 대상 산출 기준

## 4. GPT 요약 구조

## 5. GPT 재필터링 구조

## 6. Frontend 연결 결과

## 7. 테스트 결과

## 8. 확인 필요 항목

## 9. 다음 단계 제안
```

---

## 10. 완료 조건

이번 작업 완료 조건은 다음이다.

```text
- 네이버 금융 실제 운영 수집 검증
- parser 보정
- GPT 요약 대상 산출 기준 구현
- OpenAI GPT mini 요약 job 구조 구현
- GPT-5 재필터링 job 구조 구현
- GPT dry-run 지원
- API key 없을 때 안전한 오류 처리
- 뉴스 화면 GPT 상태/필터/상세 표시 연결
- Backend 테스트 통과
- Frontend build 통과
- CODEX_PROGRESS.md 갱신
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 사용자에게 다음과 같이 보고한다.

```text
뉴스 GPT 요약/재필터링 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
