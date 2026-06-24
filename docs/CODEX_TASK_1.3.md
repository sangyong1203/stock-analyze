# Codex 다음 작업 지시 프롬프트 v1.3

## 0. 작업 목표

이전 작업에서 다음 항목이 완료되었다.

- DB 스키마 검증 완료
- named UNIQUE 인덱스 보정 완료
- 설정 API CRUD 및 설정 화면 연결 완료
- 종목 API CRUD 및 종목 화면 연결 완료
- KODEX 구성종목 import 구조 구현 완료
- 수집 종목 관리 API 구현 완료
- 최종 수집 대상 재계산 로직 구현 완료
- 수집 종목 관리 화면 API 연결 완료

이번 작업의 목표는 다음이다.

1. 실제 KODEX 200 / KODEX 코스닥150 구성종목 파일로 import를 검증한다.
2. 수집 조건 규칙 기본 seed를 추가한다.
3. 수집 대상 종목을 기반으로 네이버 금융 뉴스 수집 구조를 구현한다.
4. 뉴스 수집 결과를 `news`, `news_stock_links`, `news_collect_jobs`, `news_collect_job_items` 테이블에 저장하는 기본 흐름을 만든다.
5. 뉴스 화면에서 수집된 뉴스 목록을 조회할 수 있도록 API와 Frontend를 연결한다.

기준 문서:

```text
AGENTS.md
docs/INVESTMENT_SYSTEM_PLAN_v1.2.md
docs/MVP_DB_SCHEMA_v1.2.md
docs/DEVELOPMENT_REPORT.md
docs/COLLECTION_TARGET_REPORT.md
docs/SCHEMA_VALIDATION_REPORT.md
```

문서에 없는 기능은 임의로 추가하지 않는다.

---

## 1. 작업 전 확인 사항

작업을 시작하기 전에 다음을 확인한다.

```text
1. AGENTS.md 읽기
2. INVESTMENT_SYSTEM_PLAN_v1.2.md 읽기
3. MVP_DB_SCHEMA_v1.2.md 읽기
4. DEVELOPMENT_REPORT.md 읽기
5. COLLECTION_TARGET_REPORT.md 읽기
6. SCHEMA_VALIDATION_REPORT.md 읽기
```

이번 작업은 DB 구조를 새로 설계하는 작업이 아니다.

기존 27개 MVP 테이블을 그대로 사용한다.

DB 테이블 추가가 필요해 보이면 직접 추가하지 말고 `확인 필요 항목`으로 기록한다.

---

## 2. 작업 범위

주요 작업 대상은 다음이다.

```text
backend/app/domains/collection/
backend/app/domains/news/
backend/app/external/naver/
backend/seeds/
frontend/src/pages/main/news/
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 아래 파일도 수정할 수 있다.

```text
backend/app/main.py
backend/app/db/init_db.py
frontend/src/router/routes.ts
frontend/src/shared/utils/http.ts
```

단, DB 모델과 Alembic 마이그레이션은 가능하면 수정하지 않는다.

---

## 3. 실제 KODEX 구성종목 import 검증

### 3.1 목적

이전 작업에서 구현한 KODEX 구성종목 import 구조가 실제 파일에서도 동작하는지 검증한다.

### 3.2 대상

프로젝트 저장소에 실제 파일이 있으면 해당 파일을 사용한다.

예상 파일 예시:

```text
data/코스피200 구성종목.csv
data/코스닥150 구성종목.csv
data/index_constituents.xlsx
```

파일 위치가 다르면 현재 저장소에서 확인 가능한 경로를 사용한다.

실제 파일이 없으면 import 구조만 유지하고, `확인 필요 항목`에 기록한다.

### 3.3 검증 항목

다음을 확인한다.

```text
- KODEX 200 구성종목 import 성공 여부
- KODEX 코스닥150 구성종목 import 성공 여부
- stock_code 컬럼 매핑 정상 여부
- stock_name 컬럼 매핑 정상 여부
- market 컬럼 매핑 정상 여부
- stocks 테이블 자동 생성 또는 연결 정상 여부
- index_constituents 중복 생성 방지 여부
- 기존 구성종목 is_active 처리 정상 여부
- import 후 summary API 정상 여부
```

### 3.4 지원해야 할 컬럼명

기존 구현에서 지원한 대표 컬럼명을 유지한다.

```text
stock_code
code
종목코드
단축코드

stock_name
name
종목명
한글종목명

market
시장
시장구분
```

필요하면 실제 파일 컬럼명을 추가 매핑한다.

단, 임의로 의미가 불명확한 컬럼을 강제 매핑하지 않는다.

애매하면 `확인 필요 항목`에 기록한다.

---

## 4. 수집 조건 규칙 기본 seed 추가

### 4.1 목적

수집 대상 재계산 로직에서 사용할 기본 조건 규칙을 seed로 준비한다.

대상 테이블:

```text
collection_rules
```

### 4.2 기본 seed 규칙

다음 규칙을 기본 seed로 추가한다.

```text
1. KODEX 200 포함 종목
2. KODEX 코스닥150 포함 종목
3. 관심종목 포함
4. 보유종목 포함
5. 알림 설정 종목 포함
6. 시가총액 상위 종목 조건
```

### 4.3 rule_type 예시

문서에 이미 정의된 값이 있으면 그 값을 우선 사용한다.

명확한 정의가 없으면 아래 값을 사용한다.

```text
index_member
favorite
holding
alert
market_cap
```

### 4.4 condition_json 예시

```json
{
  "index_code": "KODEX_200"
}
```

```json
{
  "index_code": "KODEX_KOSDAQ_150"
}
```

```json
{
  "is_favorite": true
}
```

```json
{
  "is_holding": true
}
```

```json
{
  "has_price_alert": true
}
```

```json
{
  "market_cap_rank_lte": 200
}
```

### 4.5 seed 안정성

seed는 반복 실행해도 중복 생성되지 않아야 한다.

다음 중 하나의 기준으로 중복을 방지한다.

```text
- name
- rule_type + condition_json
- 별도 고유 key가 있으면 해당 key
```

---

## 5. 네이버 금융 뉴스 수집 구조 구현

### 5.1 목적

네이버 금융 뉴스에서 시장 뉴스를 수집하고, 수집 대상 종목과 매칭하여 DB에 저장하는 기본 구조를 만든다.

이번 단계에서는 OpenAI 요약/필터링까지 구현하지 않는다.

이번 단계의 핵심은 다음이다.

```text
- 뉴스 수집 요청
- HTML 또는 응답 파싱
- 뉴스 중복 체크
- 종목명/종목코드 매칭
- news 저장
- news_stock_links 저장
- news_collect_jobs 기록
- news_collect_job_items 기록
```

### 5.2 수집 대상 URL

기본 대상은 네이버 금융 뉴스 목록이다.

```text
https://finance.naver.com/news/news_list.naver
```

필요 시 page 파라미터를 사용한다.

### 5.3 external client 구조

다음 위치에 네이버 금융 뉴스 client를 구현한다.

```text
backend/app/external/naver/
```

권장 파일:

```text
backend/app/external/naver/news_client.py
backend/app/external/naver/parser.py
backend/app/external/naver/types.py
```

역할:

```text
news_client.py
- HTTP 요청
- timeout 처리
- user-agent 설정
- 응답 상태 검증

parser.py
- 뉴스 목록 HTML 파싱
- 제목, URL, 언론사, 발행시각, 요약/preview 추출

types.py
- 수집 결과 타입 정의
```

### 5.4 news 도메인 service 구조

다음 위치에 수집 로직을 구현한다.

```text
backend/app/domains/news/
```

권장 파일:

```text
router.py
service.py
repository.py
schemas.py
```

구현할 주요 함수:

```text
collect_market_news()
normalize_news_url()
normalize_news_title()
generate_url_hash()
generate_title_hash()
detect_related_stocks()
calculate_basic_importance_score()
save_news_with_duplicates()
create_news_stock_links()
```

---

## 6. 뉴스 중복 처리

기준 문서의 중복 정책을 따른다.

별도 `news_duplicates` 테이블은 만들지 않는다.

중복 정보는 `news` 테이블의 필드를 사용한다.

```text
duplicate_count
source_count
sources_json
first_published_at
last_published_at
```

### 6.1 중복 기준

다음 기준을 사용한다.

```text
url_hash = sha1(normalized_url)
title_hash = sha1(normalized_title)
news_group_key = date + main_entity + event_type
```

### 6.2 중복 처리 방식

```text
1. url_hash가 같으면 동일 기사로 처리한다.
2. title_hash가 같고 최근 24시간 이내이면 중복 후보로 처리한다.
3. 중복이면 새 row를 만들지 않고 기존 news row의 duplicate_count, source_count, sources_json, last_published_at을 갱신한다.
4. 완전 신규이면 news row를 생성한다.
```

### 6.3 window

기본 중복 확인 window는 24시간으로 한다.

이벤트성 뉴스의 72시간 window는 구조만 고려하고, 실제 고급 event_type 분류는 후속 단계로 넘긴다.

---

## 7. 종목 매칭

### 7.1 대상 종목

종목 매칭은 수집 대상 종목을 기준으로 한다.

다음 데이터를 활용한다.

```text
stocks
stock_collection_settings
index_constituents
```

우선 `stock_collection_settings.collect_enabled = true`인 종목을 대상으로 매칭한다.

### 7.2 매칭 기준

다음 기준을 사용한다.

```text
- 종목명 포함
- aliases_json 포함
- 종목코드 포함
```

`aliases_json`이 비어 있으면 종목명 기준만 사용한다.

### 7.3 저장

뉴스와 종목이 매칭되면 `news_stock_links`에 저장한다.

저장 필드:

```text
news_id
stock_id
stock_code
stock_name
relation_type
relation_score
source_stock_code
created_at
```

기본값:

```text
relation_type = "mentioned"
relation_score = 1.0
source_stock_code = null
```

---

## 8. 기본 중요도 점수

이번 단계에서는 GPT를 사용하지 않는다.

키워드 기반 기본 중요도만 계산한다.

### 8.1 기본 점수

```text
공시, 수주, 공급계약, 실적, 배당, 자사주, 유상증자, 무상증자: +5
증설, CAPA, 공장, 인수합병, M&A: +4
정부, 정책, 규제, 세제, 보조금: +4
기술, 특허, 인증, 양산, 임상: +3
시장, 코스피, 코스닥, 환율, 금리, 유가: +3
반도체, HBM, 전력, ESS, 태양광, 2차전지, 로봇, 원전, 방산, 바이오: +2
```

### 8.2 감점

```text
특징주: -2
단순 급등: -2
단순 급락: -2
봉사활동, 기부, 행사, 사진, 광고: -4
```

### 8.3 저장

계산 결과는 `news.importance_score`에 저장한다.

이번 단계에서는 다음 필드는 아직 비워둘 수 있다.

```text
gpt_summary
gpt_filter_result
gpt_filter_reason
```

단, status 필드는 필요하면 기본값을 넣는다.

---

## 9. 뉴스 수집 API 구현

다음 API를 구현한다.

```text
GET  /api/news
GET  /api/news/summary
GET  /api/news/{news_id}
POST /api/news/collect/market
GET  /api/news/collect/jobs
GET  /api/news/collect/jobs/{job_id}
```

### 9.1 GET /api/news

지원 필터:

```text
keyword
stock_code
market_scope
event_type
filter_status
min_importance_score
is_alert_target
published_from
published_to
```

### 9.2 GET /api/news/summary

응답 예시:

```text
- total_news_count
- today_news_count
- linked_stock_news_count
- gpt_summary_target_count
- alert_target_count
- avg_importance_score
```

### 9.3 POST /api/news/collect/market

동작:

```text
1. news_collect_jobs row 생성
2. 네이버 금융 시장 뉴스 수집 실행
3. 파싱
4. 중복 처리
5. 종목 매칭
6. news 저장
7. news_stock_links 저장
8. news_collect_job_items 저장
9. job 결과 갱신
```

요청 body 예시:

```json
{
  "pages": 1,
  "max_items": 50
}
```

---

## 10. 뉴스 화면 연결

대상 화면:

```text
frontend/src/pages/main/news/
```

### 10.1 구현 기능

다음 기능을 구현한다.

```text
- 뉴스 목록 조회
- 키워드 검색
- 종목코드 필터
- 중요도 필터
- 발행일 필터
- 뉴스 상세 보기
- 뉴스 수집 실행 버튼
- 수집 job 결과 표시
- 요약 KPI 표시
```

### 10.2 목록 표시 컬럼

```text
- 발행시각
- 제목
- 출처
- 관련 종목
- 중요도
- 중복 횟수
- 필터 상태
- GPT 요약 상태
```

### 10.3 상세 보기

상세 보기에는 다음을 표시한다.

```text
- 제목
- URL
- 출처
- 발행시각
- 원문 요약/preview
- 관련 종목
- 중요도
- 중복 정보
- 매칭 키워드
```

---

## 11. 테스트 항목

### 11.1 Backend 테스트

다음을 확인한다.

```text
- /api/news/summary 200 응답
- /api/news 목록 조회 200 응답
- /api/news/collect/market 실행 성공
- news_collect_jobs 생성 확인
- news_collect_job_items 생성 확인
- news row 생성 또는 중복 갱신 확인
- news_stock_links 생성 확인
- 중복 수집 시 duplicate_count 증가 확인
```

### 11.2 Frontend 테스트

다음을 확인한다.

```text
- 뉴스 화면 접근
- 뉴스 목록 조회
- 뉴스 수집 버튼 동작
- 수집 결과 표시
- 검색/필터 동작
- 뉴스 상세 보기 동작
- npm run build 성공
```

### 11.3 Regression

기존 기능이 깨지지 않았는지 확인한다.

```text
- /health
- /api/auth/status
- 설정 API
- 종목 API
- 수집 종목 관리 API
- Frontend build
```

---

## 12. 문서 갱신

작업 완료 후 다음 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 다음 문서를 새로 작성한다.

```text
docs/NEWS_COLLECTION_REPORT.md
```

`NEWS_COLLECTION_REPORT.md`에는 다음 내용을 기록한다.

```markdown
# NEWS COLLECTION REPORT

## 1. 작업 개요

## 2. 구현한 API

## 3. 구현한 수집 구조

## 4. 중복 처리 방식

## 5. 종목 매칭 방식

## 6. Frontend 연결 결과

## 7. 테스트 결과

## 8. 확인 필요 항목

## 9. 다음 단계 제안
```

---

## 13. 완료 조건

이번 작업 완료 조건은 다음이다.

```text
- 실제 KODEX 구성종목 파일 import 검증 또는 파일 부재 시 확인 필요 항목 기록
- 수집 조건 규칙 기본 seed 추가
- 네이버 금융 뉴스 수집 client 구조 구현
- 시장 뉴스 수집 API 구현
- 뉴스 중복 처리 구현
- 수집 대상 종목 매칭 구현
- news_stock_links 저장 구현
- 뉴스 화면 실제 API 연결
- Backend 테스트 통과
- Frontend build 통과
- CODEX_PROGRESS.md 갱신
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 사용자에게 다음과 같이 보고한다.

```text
뉴스 수집 구조 및 뉴스 화면 연결 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
