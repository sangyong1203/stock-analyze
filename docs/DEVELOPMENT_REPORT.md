# DEVELOPMENT REPORT

## 1. 작업 개요

- 프로젝트명: stock-analyze
- 작업 기준 문서:
  - INVESTMENT_SYSTEM_PLAN_v1.2.md
  - MVP_DB_SCHEMA_v1.2.md
  - CODEX_TASK_1.6.md
- 작업 범위: 1차 MVP 기반 구조, DB 스키마 검증, 종목/수집/뉴스/GPT/알림 후보 기능, 뉴스 알림 Gmail 발송 구조
- 작업 완료 여부: 완료

## 2. 완료한 작업

- [x] 1차 MVP 기반 구조 구현
  - 설명: FastAPI, SQLAlchemy, Alembic, Vue 3, Vite, Element Plus 기반 구조를 구성했다.
  - 관련 파일: backend/, frontend/

- [x] 27개 MVP DB 테이블 및 마이그레이션 구현
  - 설명: 기준 문서의 27개 테이블, 주요 인덱스, UNIQUE 제약, 외래키, SQLite 호환 구조를 구현하고 검증했다.
  - 관련 파일: backend/app/db/models.py, backend/alembic/versions/, docs/SCHEMA_VALIDATION_REPORT.md

- [x] 종목 API CRUD 및 종목 화면 실제 API 연결
  - 설명: 종목 목록/상세/생성/수정/비활성화/관심종목/검색/필터/보유 여부 계산을 구현했다.
  - 관련 파일: backend/app/domains/stocks/, frontend/src/pages/main/stocks/

- [x] KODEX 구성종목 import 및 수집 종목 관리 구현
  - 설명: CSV/XLS/XLSX import, KODEX 200/코스닥150 실제 XLS import, 수집 대상 관리 API와 화면을 구현했다.
  - 관련 파일: backend/app/domains/collection/, backend/seeds/import_index_constituents.py, frontend/src/pages/main/collection/

- [x] 네이버 금융 뉴스 수집 구조 구현
  - 설명: 뉴스 수집 client/parser/type, 중복 처리, 종목 매핑, 중요도 계산, 수집 job 기록을 구현했다.
  - 관련 파일: backend/app/external/naver/, backend/app/domains/news/, frontend/src/pages/main/news/

- [x] GPT 뉴스 요약/필터 구조 구현
  - 설명: GPT 요약 대상 산출, OpenAI 호출 client, summary/filter dry-run 및 실행 API, API key 누락 오류 처리를 구현했다.
  - 관련 파일: backend/app/external/openai/, backend/app/domains/news/, docs/GPT_NEWS_PROCESSING_REPORT.md

- [x] GPT 결과 검토 및 뉴스 알림 후보 산출 구현
  - 설명: GPT 결과 검토 API, 수동 보정 UI, alert_settings 기반 뉴스 알림 후보 재계산/조회/요약 API를 구현했다.
  - 관련 파일: backend/app/domains/news/, frontend/src/pages/main/news/, docs/NEWS_ALERT_CANDIDATE_REPORT.md

- [x] 뉴스 알림 Gmail 발송 구조 구현
  - 설명: Gmail SMTP client, dry-run, 실제 발송 API, alert_histories 성공/실패 기록, 일별/시간별 제한, 중복 발송 방지, 알림 화면 연결을 구현했다.
  - 관련 파일: backend/app/external/gmail/, backend/app/domains/news/, frontend/src/pages/main/alerts/, docs/NEWS_ALERT_SEND_REPORT.md

## 3. 생성한 파일

| 파일 | 설명 |
| ---- | ---- |
| backend/app/external/gmail/types.py | Gmail 발송 메시지 타입 |
| docs/NEWS_COLLECTION_REPORT.md | 뉴스 수집 구조 리포트 |
| docs/GPT_NEWS_PROCESSING_REPORT.md | GPT 뉴스 처리 구조 리포트 |
| docs/NEWS_ALERT_CANDIDATE_REPORT.md | 뉴스 알림 후보 산출 리포트 |
| docs/NEWS_ALERT_SEND_REPORT.md | 뉴스 알림 Gmail 발송 구조 리포트 |
| docs/SCHEMA_VALIDATION_REPORT.md | DB 스키마 검증 리포트 |
| docs/COLLECTION_TARGET_REPORT.md | 수집 대상 관리 리포트 |

## 4. 수정한 파일

| 파일 | 수정 내용 |
| ---- | --------- |
| backend/app/core/config.py | OpenAI 및 Gmail SMTP 환경변수 구조 추가 |
| backend/.env.example | OpenAI/Gmail SMTP 환경변수 예시 추가 |
| backend/app/db/models.py | 27개 MVP 모델 및 관계 구성 |
| backend/app/db/init_db.py | 기본 seed 및 collection_rules seed 구성 |
| backend/app/domains/stocks/ | 종목 CRUD API 구현 |
| backend/app/domains/collection/ | 수집 종목 관리 및 KODEX import 구현 |
| backend/app/domains/news/ | 뉴스 수집, GPT 처리, 알림 후보, Gmail 발송 API 구현 |
| backend/app/external/naver/ | 네이버 금융 뉴스 client/parser 구현 |
| backend/app/external/openai/ | OpenAI Responses API client 구현 |
| backend/app/external/gmail/ | Gmail SMTP client 구현 |
| frontend/src/pages/main/stocks/ | 종목 화면 실제 API 연결 |
| frontend/src/pages/main/collection/ | 수집 종목 관리 화면 실제 API 연결 |
| frontend/src/pages/main/news/ | 뉴스/GPT/알림 후보 화면 연결 |
| frontend/src/pages/main/alerts/ | 알림 발송 화면 실제 API 연결 |
| docs/CODEX_PROGRESS.md | 최신 작업 진행 결과 반영 |
| docs/DEVELOPMENT_REPORT.md | 최신 완료 결과 반영 |

## 5. 구현한 Backend 항목

- FastAPI 구조: `backend/app/main.py`에서 도메인별 라우터 구성
- DB 연결: `backend/app/db/session.py`에서 SQLite 연결 설정
- SQLAlchemy 모델: `backend/app/db/models.py`에 27개 MVP 테이블 구현
- Alembic: 초기 MVP 스키마와 named UNIQUE index 보정 마이그레이션 구성
- API 라우터: settings, stocks, collection, news, alerts 관련 API 구현
- Seed 구조: app_settings, scheduled_jobs, news_keyword_settings, alert_settings, collection_rules 기본 seed 구현
- 외부 연동 구조: 네이버 금융 뉴스, OpenAI, Gmail SMTP client 구조 구현
- 뉴스 알림 발송: dry-run, 실제 발송, 발송 이력, 중복 방지, 발송 제한 구현

## 6. 구현한 Frontend 항목

- 라우터: 1차 MVP 메뉴 라우팅 구성
- 레이아웃: MainLayout, AuthLayout, EmptyLayout 구성
- 메뉴: 대시보드, 종목, 수집 종목 관리, 뉴스, 포트폴리오, 거래 기록, 알림 관리, 차트, 메모/태그, 설정
- 화면 골격: Element Plus 기반 KPI, 필터, 테이블, drawer/form UI 구성
- API 연결 상태: 설정, 종목, 수집 종목 관리, 뉴스, GPT 처리, 뉴스 알림 후보, 알림 Gmail 발송 화면 실제 API 연결 완료

## 7. DB 구현 결과

- 생성한 테이블 수: 27개 MVP 테이블 + alembic_version
- 생성한 테이블 목록: users, app_settings, scheduled_jobs, system_logs, stocks, index_constituents, stock_prices, price_snapshots, corporate_actions, stock_collection_settings, collection_rules, news, news_stock_links, news_keyword_settings, news_collect_jobs, news_collect_job_items, fund_pools, fund_transactions, trades, trade_news_links, holdings, price_alerts, alert_settings, alert_histories, memos, tags, tag_links
- 생성한 인덱스: 기준 문서 지정 named index 및 UNIQUE index 반영
- 마이그레이션 파일: backend/alembic/versions/20260624_0001_initial_mvp_schema.py, backend/alembic/versions/20260624_0002_named_unique_indexes.py
- SQLite DB 생성 여부: 생성 및 검증 완료

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

### Gmail SMTP 설정

```env
GMAIL_SMTP_HOST=smtp.gmail.com
GMAIL_SMTP_PORT=587
GMAIL_SMTP_USERNAME=
GMAIL_SMTP_APP_PASSWORD=
ALERT_RECIPIENT_EMAIL=
```

## 9. 테스트 결과

- Backend compile: `python -m compileall app` 성공
- DB migration: `python -m alembic upgrade head` 성공
- Seed: `python seeds/seed_defaults.py` 성공
- KODEX 실제 파일 import: `data/KODEX_200.xls` 200건, `data/KODEX_KOSDAQ_150.xls` 150건 성공
- 기본 API: `/health`, `/api/auth/status`, `/api/settings`, `/api/stocks`, `/api/collection/stocks/summary` 200 응답 확인
- 뉴스 API: `/api/news`, `/api/news/summary`, `/api/news/collect/market`, `/api/news/collect/jobs` 정상 확인
- GPT API: `/api/news/gpt/targets`, `/api/news/gpt/status`, summary dry-run, filter dry-run 200 응답 확인
- OpenAI 실제 요약: summary limit 1 성공, `gpt_summary_status = done` 저장 확인
- OpenAI 실제 필터: filter limit 1 호출은 OpenAI `insufficient_quota` 오류로 실패 처리 확인
- 뉴스 알림 후보 API: `/api/news/alerts/candidates/recalculate`, `/api/news/alerts/candidates`, `/api/news/alerts/summary` 정상 확인
- 뉴스 알림 발송 dry-run: `/api/news/alerts/send/dry-run` 200 응답 확인
- 뉴스 알림 실제 발송: Gmail 환경변수 설정 후 `/api/news/alerts/send` 실제 SMTP 발송 성공, sent 2, failed 0 확인
- 발송 이력 기록: `alert_histories` sent 2건 기록 확인
- 발송 제한 보정: 검증 중 `limit: 1` 요청이 연결 종목 2건을 발송하는 동작을 확인했고, 이후 요청 limit이 발송 단위 기준으로 적용되도록 보정
- 발송 환경변수 오류 처리: 환경변수 미설정 상태에서 `Missing Gmail SMTP settings: GMAIL_SMTP_USERNAME, GMAIL_SMTP_APP_PASSWORD, ALERT_RECIPIENT_EMAIL` 400 응답 확인
- 발송 이력 API: `/api/news/alerts/histories`, `/api/news/alerts/histories/summary` 200 응답 확인
- Frontend build: `npm run build` 성공
- 오류 여부: 최종 검증 기준 오류 없음

## 10. 미완료 항목

- 항목: OpenAI GPT 필터 실제 성공 검증
- 이유: OpenAI quota 부족으로 filter limit 1 실제 호출이 실패 처리됐다.
- 다음 작업 제안: OpenAI billing/quota 확인 후 filter limit 1부터 재검증한다.

## 11. 확인 필요 항목

- 항목: Gmail 수신 확인
- 확인이 필요한 이유: SMTP 발송 API와 sent 이력 기록은 성공했으나, 실제 수신함 도착 여부는 메일함에서 확인해야 한다.
- 제안: `ALERT_RECIPIENT_EMAIL` 수신함에서 뉴스 알림 메일 도착 여부를 확인한다.

- 항목: 발송 제한 운영값
- 확인이 필요한 이유: 현재는 `alert_settings` 기본값을 사용한다.
- 제안: 실제 알림 빈도에 맞춰 `max_daily_alerts`, `max_hourly_alerts`를 조정한다.

- 항목: OpenAI quota/billing
- 확인이 필요한 이유: GPT 필터 실제 호출에서 `insufficient_quota`가 발생했다.
- 제안: quota 복구 후 필터 실제 호출을 재검증한다.

## 12. 다음 단계 제안

- 다음 단계 1: Gmail 수신함에서 실제 알림 메일 도착 확인 및 발송 제한 운영값 조정
- 다음 단계 2: 발송 이력 기반 알림 화면 보완
- 다음 단계 3: KRX 가격 데이터 수집 구조 구현

## 13. 최종 완료 선언

모든 지시 내용 작업 완료 여부:

- [x] 완료
- [ ] 일부 미완료

최종 메시지:

“뉴스 알림 Gmail 발송 구조 작업 완료했습니다. DEVELOPMENT_REPORT.md를 확인해 주세요.”
