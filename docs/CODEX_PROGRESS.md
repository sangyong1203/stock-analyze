# CODEX PROGRESS

## 현재 작업 상태

- 현재 단계: GPT 검수 및 뉴스 알림 후보 산출 구조 완료
- 마지막 작업 시간: 2026-06-24
- 전체 진행률: 100%
- 현재 작업 중인 파일: backend/app/domains/news/, frontend/src/pages/main/news/, docs/

## 완료한 작업

- [x] 기준 문서 확인
  - 설명: AGENTS.md, 투자 분석 시스템 계획서, MVP DB 스키마, 기존 개발/검증/수집 대상 보고서를 기준으로 작업 범위를 확인했다.
  - 관련 파일: AGENTS.md, docs/INVESTMENT_SYSTEM_PLAN_v1.2.md, docs/MVP_DB_SCHEMA_v1.2.md, docs/DEVELOPMENT_REPORT.md, docs/COLLECTION_TARGET_REPORT.md, docs/SCHEMA_VALIDATION_REPORT.md
- [x] 실제 KODEX XLS import 검증
  - 설명: `data/KODEX_200.xls`, `data/KODEX_KOSDAQ_150.xls`를 실제 import했고 active 구성종목 350건(KODEX 200 200건, KODEX 코스닥150 150건)을 확인했다.
  - 관련 파일: data/KODEX_200.xls, data/KODEX_KOSDAQ_150.xls, backend/seeds/import_index_constituents.py
- [x] collection_rules 기본 seed 추가
  - 설명: KODEX 200, KODEX 코스닥150, 관심, 보유, 알림, 시가총액 상위 조건 기본 규칙을 반복 실행 가능하게 추가했다.
  - 관련 파일: backend/app/db/init_db.py, backend/seeds/README.md
- [x] 네이버 금융 뉴스 수집 client 구조 구현
  - 설명: 네이버 금융 뉴스 목록 요청, HTML 파싱, 수집 결과 타입 구조를 구현했다.
  - 관련 파일: backend/app/external/naver/news_client.py, backend/app/external/naver/parser.py, backend/app/external/naver/types.py
- [x] 뉴스 수집 서비스 구현
  - 설명: URL/제목 정규화, hash 생성, 24시간 중복 처리, 수집 대상 종목 매칭, 키워드 기반 중요도 계산, news/news_stock_links/news_collect_jobs/news_collect_job_items 저장 흐름을 구현했다.
  - 관련 파일: backend/app/domains/news/service.py, backend/app/domains/news/repository.py, backend/app/domains/news/schemas.py
- [x] 뉴스 API 구현
  - 설명: 뉴스 목록, 요약, 상세, 시장 뉴스 수집, 수집 job 목록/상세 API를 구현했다.
  - 관련 파일: backend/app/domains/news/router.py
- [x] 뉴스 화면 실제 API 연결
  - 설명: KPI, 검색/종목코드/범위/중요도/발행일 필터, 뉴스 수집 버튼, 수집 결과 표시, 목록 테이블, 상세 drawer를 실제 API와 연결했다.
  - 관련 파일: frontend/src/pages/main/news/
- [x] 실행 및 회귀 검증
  - 설명: Alembic migration, seed, backend compile, 뉴스 API 수집/중복/링크/job 검증, 기존 health/auth/settings/stocks/collection API 회귀 검증, frontend build를 확인했다.
  - 관련 파일: backend/, frontend/
- [x] 뉴스 수집 보고서 작성
  - 설명: 구현한 API, 수집 구조, 중복 처리, 종목 매칭, 테스트 결과, 확인 필요 항목을 별도 문서로 정리했다.
  - 관련 파일: docs/NEWS_COLLECTION_REPORT.md
- [x] XLS importer 보완
  - 설명: KODEX 실제 파일처럼 첫 줄 제목, 둘째 줄 헤더인 `.xls` 파일을 읽을 수 있도록 `xlrd` 기반 XLS 지원과 헤더 행 탐지를 추가했다.
  - 관련 파일: backend/app/domains/collection/service.py, backend/requirements.txt
- [x] 네이버 금융 실제 운영 수집 검증 및 parser 보정
  - 설명: 실제 네이버 금융 HTML에서 메뉴 링크 오탐을 제거하고 articleSubject/articleSummary 기반으로 제목, URL, 언론사, 발행시각, preview를 추출하도록 보정했다.
  - 관련 파일: backend/app/external/naver/parser.py
- [x] GPT 요약 대상 산출 기준 구현
  - 설명: 중요도, 중복 수, 출처 수, 이벤트 유형, 알림 후보 기준으로 `is_gpt_summary_target`과 `gpt_summary_status`를 산출한다.
  - 관련 파일: backend/app/domains/news/service.py
- [x] OpenAI GPT 요약/재필터링 job API 구현
  - 설명: GPT 요약/재필터링 dry-run과 실행 API, API key 누락 시 400 오류, GPT 처리 통계 API를 구현했다.
  - 관련 파일: backend/app/domains/news/, backend/app/external/openai/
- [x] 뉴스 화면 GPT 상태 보완
  - 설명: GPT KPI, 요약 대상/상태/필터 결과 필터, dry-run/실행 버튼, 목록 컬럼, 상세 drawer GPT 필드를 추가했다.
  - 관련 파일: frontend/src/pages/main/news/
- [x] GPT 뉴스 처리 보고서 작성
  - 설명: GPT 대상 기준, 요약 구조, 재필터링 구조, 테스트 결과, 확인 필요 항목을 문서화했다.
  - 관련 파일: docs/GPT_NEWS_PROCESSING_REPORT.md
- [x] OpenAI 환경변수 점검 보완
  - 설명: dry_run=false 실행 시 API key/model 누락을 명확한 400 오류로 반환하고 dry_run=true는 key 없이도 대상 확인 가능하게 유지했다.
  - 관련 파일: backend/app/domains/news/service.py
- [x] GPT 결과 검수 API 구현
  - 설명: GPT 검수 목록 조회와 gpt_filter_result, gpt_filter_reason, is_alert_target, filter_status 수동 보정 API를 구현했다.
  - 관련 파일: backend/app/domains/news/router.py, backend/app/domains/news/service.py, backend/app/domains/news/schemas.py
- [x] 뉴스 알림 후보 산출 API 구현
  - 설명: alert_settings 기준으로 뉴스 알림 후보를 재계산하고 후보 목록/요약을 조회하는 API를 구현했다. Gmail 발송은 구현하지 않았다.
  - 관련 파일: backend/app/domains/news/
- [x] 뉴스 화면 검수/알림 후보 UI 보완
  - 설명: GPT 검수 목록, 수동 보정 form, 알림 후보 재계산 버튼, 알림 후보 KPI와 후보 목록을 뉴스 화면에 추가했다.
  - 관련 파일: frontend/src/pages/main/news/
- [x] 뉴스 알림 후보 보고서 작성
  - 설명: 알림 후보 산출 기준, API, UI 연결, 테스트 결과, 확인 필요 항목을 문서화했다.
  - 관련 파일: docs/NEWS_ALERT_CANDIDATE_REPORT.md

## 진행 중인 작업

- [x] 작업 완료
  - 현재 상태: 완료
  - 남은 작업: 없음

## 남은 작업

- [ ] 네이버 금융 실제 운영 수집 안정성 점검
- [ ] OpenAI API key/model 설정 후 실제 GPT 호출 검증
- [ ] Gmail SMTP 발송 및 alert_histories 기록 구현
- [ ] KRX 가격 데이터 수집 구조 구현

## 막힌 항목

- 항목: 없음
- 원인: 없음
- 필요한 확인: 없음

## 생성한 파일

- 파일 경로: backend/app/external/naver/news_client.py
- 설명: 네이버 금융 뉴스 HTTP client
- 파일 경로: backend/app/external/naver/parser.py
- 설명: 네이버 금융 뉴스 목록 HTML parser
- 파일 경로: backend/app/external/naver/types.py
- 설명: 네이버 뉴스 수집 결과 타입
- 파일 경로: docs/NEWS_COLLECTION_REPORT.md
- 설명: 뉴스 수집 구조 및 화면 연결 작업 보고서
- 파일 경로: backend/app/external/openai/types.py
- 설명: OpenAI text response 타입
- 파일 경로: docs/GPT_NEWS_PROCESSING_REPORT.md
- 설명: GPT 뉴스 처리 구조 보고서
- 파일 경로: docs/NEWS_ALERT_CANDIDATE_REPORT.md
- 설명: 뉴스 알림 후보 산출 구조 보고서

## 수정한 파일

- 파일 경로: backend/app/db/init_db.py
- 수정 내용: collection_rules 기본 seed 추가 및 기존 기본 규칙 보정
- 파일 경로: backend/app/domains/collection/service.py
- 수정 내용: index_member 규칙의 index_code 조건 처리, `.xls` import, KODEX 헤더 행 탐지, KOSDAQ index code summary 보완
- 파일 경로: backend/requirements.txt
- 수정 내용: `.xls` import용 `xlrd` 의존성 추가
- 파일 경로: backend/seeds/import_index_constituents.py
- 수정 내용: `KODEX_KOSDAQ_150` index code 허용
- 파일 경로: backend/app/domains/news/
- 수정 내용: 뉴스 수집/조회/요약/job API 구현
- 파일 경로: backend/app/db/models.py
- 수정 내용: 뉴스/뉴스 링크/job/job item SQLAlchemy relationship 추가
- 파일 경로: backend/app/external/naver/__init__.py
- 수정 내용: NaverFinanceNewsClient export
- 파일 경로: backend/app/external/naver/parser.py
- 수정 내용: 실제 네이버 금융 HTML articleSubject/articleSummary 구조 기반 parser 보정
- 파일 경로: backend/app/external/openai/client.py
- 수정 내용: OpenAI Responses API 기반 text client 구현
- 파일 경로: backend/app/core/config.py
- 수정 내용: OpenAI 뉴스 요약/필터 모델 환경변수 추가
- 파일 경로: backend/.env.example
- 수정 내용: OPENAI_NEWS_SUMMARY_MODEL, OPENAI_NEWS_FILTER_MODEL 예시 키 추가
- 파일 경로: frontend/src/pages/main/news/
- 수정 내용: 뉴스 화면 실제 API 연결, GPT 상태/필터/실행 UI, GPT 검수/알림 후보 UI 추가
- 파일 경로: backend/app/domains/news/
- 수정 내용: GPT 검수 API, 수동 보정, 알림 후보 재계산/조회/요약 API 추가
- 파일 경로: docs/DEVELOPMENT_REPORT.md
- 수정 내용: 뉴스 수집 구조 및 테스트 결과 반영

## 확인 필요 항목

- 항목: 네이버 금융 HTML 구조 변경 대응
- 이유: 현재 parser는 네이버 금융 뉴스 목록 HTML의 링크 패턴을 기준으로 구현되어 있어 운영 중 HTML 구조 변경 시 보완이 필요하다.
- 제안: 실제 운영 수집 로그를 보고 필요한 selector/파싱 규칙을 추가한다.

- 항목: OpenAI 요약/재필터링
- 이유: 현재 환경에 OPENAI_API_KEY와 모델명이 설정되지 않아 실제 호출은 검증하지 못했다.
- 제안: `.env`에 OPENAI_API_KEY, OPENAI_NEWS_SUMMARY_MODEL, OPENAI_NEWS_FILTER_MODEL 설정 후 소량 실행 검증한다.

- 항목: Gmail SMTP 발송
- 이유: CODEX_TASK_1.5 범위는 알림 후보 산출까지만 포함한다.
- 제안: 다음 단계에서 alert_histories 기록과 Gmail SMTP 발송을 구현한다.
