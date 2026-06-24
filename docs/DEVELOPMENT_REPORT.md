# DEVELOPMENT REPORT

## 1. 작업 개요

- 프로젝트명: stock-analyze
- 작업 기준 문서:
  - INVESTMENT_SYSTEM_PLAN_v1.2.md
  - MVP_DB_SCHEMA_v1.2.md
- 작업 범위: 1차 MVP 기반 구조, DB 스키마 검증, 설정/종목/수집 종목 관리 API 및 화면 연결, 네이버 금융 뉴스 수집 구조, 뉴스 API 및 뉴스 화면 연결
- 작업 완료 여부: 완료

## 2. 완료한 작업

- [x] 기준 문서 확인
  - 설명: 1차 MVP 확정 기능과 27개 DB 테이블 범위를 확인했다.
  - 관련 파일: AGENTS.md, docs/INVESTMENT_SYSTEM_PLAN_v1.2.md, docs/MVP_DB_SCHEMA_v1.2.md
- [x] Backend/Frontend 기본 구조 구축
  - 설명: FastAPI, SQLAlchemy, Alembic, Vue 3, Vite, Element Plus 기반 구조를 생성했다.
  - 관련 파일: backend/, frontend/
- [x] DB 모델 및 마이그레이션 구현
  - 설명: 27개 MVP 테이블, 주요 외래키, 인덱스, UNIQUE 제약을 구현하고 SQLite/Alembic 실행을 확인했다.
  - 관련 파일: backend/app/db/models.py, backend/alembic/versions/
- [x] 설정 API CRUD 및 화면 연결
  - 설명: app_settings, scheduled_jobs, news_keyword_settings, alert_settings API와 설정 화면을 연결했다.
  - 관련 파일: backend/app/domains/settings/, frontend/src/pages/main/settings/
- [x] DB 스키마 검증 및 named UNIQUE 인덱스 보정
  - 설명: 27개 테이블/필드/인덱스/제외 테이블/seed를 검증하고 named UNIQUE 인덱스를 보정했다.
  - 관련 파일: docs/SCHEMA_VALIDATION_REPORT.md, backend/alembic/versions/20260624_0002_named_unique_indexes.py
- [x] 종목 API CRUD 및 화면 연결
  - 설명: 종목 목록/상세/생성/수정/비활성화/관심 설정/검색/필터 API와 종목 화면을 연결했다.
  - 관련 파일: backend/app/domains/stocks/, frontend/src/pages/main/stocks/
- [x] KODEX 구성종목 import 구조 및 수집 종목 관리 구현
  - 설명: CSV/XLS/XLSX import 구조, 수집 종목 관리 API, 재계산 로직, 수집 종목 관리 화면을 구현했고 실제 XLS 파일 import를 검증했다.
  - 관련 파일: backend/app/domains/collection/, backend/seeds/import_index_constituents.py, frontend/src/pages/main/collection/
- [x] 수집 조건 규칙 seed 추가
  - 설명: KODEX 200, KODEX 코스닥150, 관심, 보유, 알림, 시가총액 상위 조건 기본 규칙을 추가했다.
  - 관련 파일: backend/app/db/init_db.py
- [x] 네이버 금융 뉴스 수집 구조 구현
  - 설명: 네이버 금융 뉴스 client/parser/type, 중복 처리, 종목 매칭, 중요도 계산, 수집 job 기록을 구현했다.
  - 관련 파일: backend/app/external/naver/, backend/app/domains/news/
- [x] 뉴스 API 및 뉴스 화면 연결
  - 설명: 뉴스 목록/요약/상세/수집/job API와 KPI, 필터, 테이블, 상세 drawer, 수집 버튼 화면을 연결했다.
  - 관련 파일: backend/app/domains/news/, frontend/src/pages/main/news/
- [x] 뉴스 GPT 요약/재필터링 구조 구현
  - 설명: 실제 네이버 금융 parser를 보정하고 GPT 요약 대상 산출, GPT 요약/재필터링 dry-run 및 실행 API, API key 누락 오류 처리, 뉴스 화면 GPT 상태 UI를 구현했다.
  - 관련 파일: backend/app/domains/news/, backend/app/external/openai/, frontend/src/pages/main/news/, docs/GPT_NEWS_PROCESSING_REPORT.md
- [x] GPT 검수 및 뉴스 알림 후보 산출 구조 구현
  - 설명: GPT 결과 검수 API, 수동 보정 UI, alert_settings 기반 뉴스 알림 후보 재계산/조회/요약 API와 화면을 구현했다. Gmail 발송은 구현하지 않았다.
  - 관련 파일: backend/app/domains/news/, frontend/src/pages/main/news/, docs/NEWS_ALERT_CANDIDATE_REPORT.md

## 3. 생성한 파일

| 파일 | 설명 |
| ---- | ---- |
| backend/app/external/naver/news_client.py | 네이버 금융 뉴스 HTTP client |
| backend/app/external/naver/parser.py | 네이버 금융 뉴스 목록 HTML parser |
| backend/app/external/naver/types.py | 네이버 뉴스 수집 결과 타입 |
| backend/app/external/openai/types.py | OpenAI text response 타입 |
| docs/NEWS_COLLECTION_REPORT.md | 뉴스 수집 구조 및 화면 연결 보고서 |
| docs/GPT_NEWS_PROCESSING_REPORT.md | GPT 뉴스 처리 구조 보고서 |
| docs/NEWS_ALERT_CANDIDATE_REPORT.md | 뉴스 알림 후보 산출 구조 보고서 |
| docs/CODEX_TODO.md | 작업 체크리스트 |
| docs/CODEX_PROGRESS.md | 작업 체크포인트 |
| docs/SCHEMA_VALIDATION_REPORT.md | DB 스키마 검증 보고서 |
| docs/COLLECTION_TARGET_REPORT.md | 수집 대상 산출 작업 보고서 |

## 4. 수정한 파일

| 파일 | 수정 내용 |
| ---- | --------- |
| backend/app/db/init_db.py | 기본 seed에 collection_rules 추가 및 기존 기본 규칙 보정 |
| backend/app/db/models.py | 뉴스/뉴스 링크/job/job item relationship 추가 |
| backend/app/domains/news/ | 뉴스 수집, 조회, 요약, job API 구현 |
| backend/app/domains/collection/service.py | index_member 조건 규칙 처리, `.xls` import, KODEX 헤더 행 탐지, KOSDAQ summary 보완 |
| backend/requirements.txt | `.xls` import용 `xlrd` 의존성 추가 |
| backend/seeds/import_index_constituents.py | `KODEX_KOSDAQ_150` index code 허용 |
| backend/app/external/naver/__init__.py | NaverFinanceNewsClient export |
| backend/app/external/naver/parser.py | 실제 네이버 금융 HTML articleSubject/articleSummary 기반 parser 보정 |
| backend/app/external/openai/client.py | OpenAI Responses API 기반 뉴스 text client 구현 |
| backend/app/core/config.py | OpenAI 뉴스 요약/필터 모델 환경변수 추가 |
| backend/.env.example | OPENAI_NEWS_SUMMARY_MODEL, OPENAI_NEWS_FILTER_MODEL 예시 키 추가 |
| frontend/src/pages/main/news/ | 뉴스 화면 실제 API 연결 및 GPT 상태 UI 추가 |
| backend/app/domains/news/ | GPT 검수 API, 수동 보정, 뉴스 알림 후보 재계산/조회/요약 API 추가 |
| frontend/src/pages/main/news/ | GPT 검수 목록, 수동 보정 form, 알림 후보 KPI/목록/재계산 UI 추가 |
| docs/CODEX_PROGRESS.md | 뉴스 수집 단계 진행 결과 반영 |
| docs/DEVELOPMENT_REPORT.md | 최신 완료 결과 반영 |

## 5. 구현한 Backend 항목

- FastAPI 구조: `backend/app/main.py`와 도메인별 라우터 구성
- DB 연결: `backend/app/db/session.py`에서 SQLite 연결 설정
- SQLAlchemy 모델: `backend/app/db/models.py`에 27개 MVP 테이블 구현, 뉴스 관계 로딩용 relationship 추가
- Alembic: `20260624_0001_initial_mvp_schema.py`, `20260624_0002_named_unique_indexes.py` 실행 확인
- API 라우터: settings CRUD, stocks CRUD, collection 관리 API, news 수집/조회/GPT 처리/검수/알림 후보 API 구현
- Seed 구조: app_settings, scheduled_jobs, news_keyword_settings, alert_settings, collection_rules 기본 seed 구현
- 뉴스 수집: 네이버 금융 목록 수집, 실제 HTML 파싱 보정, URL/제목 hash, 24시간 중복 처리, 종목 매칭, keyword 중요도 계산, job/item 기록 구현
- GPT 처리: 요약 대상 산출, OpenAI GPT 요약/재필터링 client 구조, dry-run, API key 누락 오류 처리 구현
- 알림 후보: alert_settings 기준 뉴스 알림 후보 재계산, 후보 목록/요약 조회, 수동 검수 보정 구현

## 6. 구현한 Frontend 항목

- 라우터: `frontend/src/router/routes.ts`에 10개 MVP 메뉴 라우팅 구현
- 레이아웃: `MainLayout`, `AuthLayout`, `EmptyLayout` 생성
- 메뉴: 대시보드, 종목, 수집 종목 관리, 뉴스, 포트폴리오, 거래 기록, 알림 관리, 차트, 메모/태그, 설정
- 화면 골격: Element Plus 기반 KPI, 필터, 테이블, drawer UI 구성
- API 연결 상태: 설정, 종목, 수집 종목 관리, 뉴스 화면 실제 API 연결 완료, 뉴스 GPT 상태/필터/실행/검수/알림 후보 UI 연결 완료

## 7. DB 구현 결과

- 생성한 테이블 수: 27개 MVP 테이블 + alembic_version 1개
- 생성한 테이블 목록: users, app_settings, scheduled_jobs, system_logs, stocks, index_constituents, stock_prices, price_snapshots, corporate_actions, stock_collection_settings, collection_rules, news, news_stock_links, news_keyword_settings, news_collect_jobs, news_collect_job_items, fund_pools, fund_transactions, trades, trade_news_links, holdings, price_alerts, alert_settings, alert_histories, memos, tags, tag_links
- 생성한 인덱스: 문서 지정 named index 및 UNIQUE 인덱스 반영
- 마이그레이션 파일: backend/alembic/versions/20260624_0001_initial_mvp_schema.py, backend/alembic/versions/20260624_0002_named_unique_indexes.py
- SQLite DB 생성 여부: 생성 확인 완료

## 8. 실행 방법

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

### Migration

```bash
cd backend
python -m alembic upgrade head
python seeds/seed_defaults.py
```

## 9. 테스트 결과

- Backend compile: `python -m compileall app` 성공
- DB migration: `python -m alembic upgrade head` 성공
- Seed: `python seeds/seed_defaults.py` 성공, collection_rules 6개 기본 규칙 반복 실행 안정성 확인
- KODEX 실제 파일 import: `data/KODEX_200.xls` 200건, `data/KODEX_KOSDAQ_150.xls` 150건 성공
- KODEX 중복 방지: 재import 후 `index_constituents` total/active 350건 유지
- 수집 대상 재계산: active 구성종목 350건 기준 `collect_enabled_count` 350 확인
- 기본 API 테스트: `/health`, `/api/auth/status`, `/api/settings`, `/api/stocks`, `/api/collection/stocks/summary` 200 응답 확인
- 뉴스 API 테스트: `/api/news/summary`, `/api/news`, `/api/news/collect/market`, `/api/news/collect/jobs`, `/api/news/collect/jobs/{job_id}`, `/api/news/{news_id}` 성공
- 실제 네이버 운영 수집 테스트: `/api/news/collect/market` pages 1, max_items 10 성공, parser 제목/URL/언론사/발행시각/preview 추출 확인
- 뉴스 저장 테스트: 테스트용 네이버 수집 결과 주입으로 news 생성, news_stock_links 생성, news_collect_jobs/items 생성 확인
- 중복 테스트: 동일 기사 재수집 시 신규 row 없이 `duplicate_count` 증가 확인
- GPT API 테스트: `/api/news/gpt/targets`, `/api/news/gpt/status`, summary dry-run, filter dry-run 200 응답 확인
- GPT API key 오류 테스트: dry_run=false에서 `OPENAI_API_KEY is not configured` 400 응답 확인
- GPT 검수 API 테스트: `/api/news/gpt/review` 200 응답, `/api/news/gpt/review/{news_id}` PATCH 성공
- 뉴스 알림 후보 API 테스트: `/api/news/alerts/candidates/recalculate`, `/api/news/alerts/candidates`, `/api/news/alerts/summary` 성공
- 뉴스 알림 후보 재계산 결과: processed 14, alert_target 2
- Frontend build: `npm run build` 성공
- 오류 여부: 최종 검증 기준 오류 없음

## 10. 미완료 항목

- 항목: OpenAI 요약/재필터링 실제 호출
- 이유: 현재 환경에 OPENAI_API_KEY와 모델명이 없다.
- 다음 작업 제안: `.env` 설정 후 요약 5건, 재필터 5건 소량 실행 검증

- 항목: Gmail SMTP 실제 발송
- 이유: 이번 작업 범위는 알림 후보 산출까지만 포함한다.
- 다음 작업 제안: alert_histories 생성과 Gmail SMTP 발송 구현

- 항목: 외부 연동 운영 검증
- 이유: Google OAuth, KRX, Gmail SMTP, OpenAI 인증값이 아직 없다.
- 다음 작업 제안: 환경변수 확정 후 external client를 실제 운영 흐름으로 검증

## 11. 확인 필요 항목

- 항목: KODEX 파일 갱신 주기
- 확인이 필요한 이유: 현재 import는 제공된 로컬 XLS 파일 기준이며 운영 갱신 주기가 정해지지 않았다.
- 제안: 새 KODEX 파일 수령 시 동일 import 명령과 새 effective_date로 갱신

- 항목: 네이버 금융 HTML 구조 변경 대응
- 확인이 필요한 이유: 현재 parser는 네이버 금융 뉴스 링크 패턴 기반이다.
- 제안: 현재 articleSubject/articleSummary 기준으로 보정했으며 운영 수집 중 누락 패턴이 확인되면 parser 규칙을 추가 보완

- 항목: OpenAI 모델명 확정
- 확인이 필요한 이유: 작업 지시 기준 모델명은 코드에 고정하지 않고 환경변수로 받는다.
- 제안: `OPENAI_NEWS_SUMMARY_MODEL`, `OPENAI_NEWS_FILTER_MODEL` 값을 확정해 `.env`에 설정

- 항목: 알림 후보 기준 튜닝
- 확인이 필요한 이유: 현재 기준은 문서 기준의 1차 산출이며 실제 운영에서는 과다/과소 알림 여부를 확인해야 한다.
- 제안: 후보 목록 검수 후 alert_settings 기준값과 event_types_json을 조정

## 12. 다음 단계 제안

- 다음 단계 1: OpenAI 환경변수 설정 후 GPT 실제 호출 소량 검증
- 다음 단계 2: GPT 필터 결과 수동 검수 및 prompt 보정
- 다음 단계 3: Gmail SMTP 발송 및 alert_histories 기록 구현
- 다음 단계 4: KRX 가격 데이터 수집 구조 구현

## 13. 최종 완료 선언

모든 지시 내용 작업 완료 여부:

- [x] 완료
- [ ] 일부 미완료

최종 메시지:

“뉴스 수집 구조 및 뉴스 화면 연결 작업 완료했습니다. DEVELOPMENT_REPORT.md를 확인해 주세요.”
