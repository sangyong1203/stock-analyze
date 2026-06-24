# NEWS COLLECTION REPORT

## 1. 작업 개요

- 작업 목표: 수집 대상 종목 기반 네이버 금융 시장 뉴스 수집 구조와 뉴스 화면 API 연결 구현
- 기준 문서: AGENTS.md, INVESTMENT_SYSTEM_PLAN_v1.2.md, MVP_DB_SCHEMA_v1.2.md, DEVELOPMENT_REPORT.md, COLLECTION_TARGET_REPORT.md, SCHEMA_VALIDATION_REPORT.md
- DB 변경: 신규 테이블 없음, 기존 27개 MVP 테이블 사용
- 실제 KODEX 파일 검증: `data/KODEX_200.xls`, `data/KODEX_KOSDAQ_150.xls` import 완료

## 2. 구현한 API

| Method | Path | 설명 |
| ------ | ---- | ---- |
| GET | `/api/news` | 뉴스 목록 조회 및 keyword, stock_code, market_scope, event_type, filter_status, min_importance_score, is_alert_target, published_from, published_to 필터 |
| GET | `/api/news/summary` | 전체/오늘/종목 연결/GPT 요약 대상/알림 후보/평균 중요도 KPI |
| GET | `/api/news/{news_id}` | 뉴스 상세 조회 |
| POST | `/api/news/collect/market` | 네이버 금융 시장 뉴스 수집 실행 |
| GET | `/api/news/collect/jobs` | 뉴스 수집 job 목록 조회 |
| GET | `/api/news/collect/jobs/{job_id}` | 뉴스 수집 job 상세 및 item 조회 |

## 3. 구현한 수집 구조

- `backend/app/external/naver/news_client.py`: 네이버 금융 뉴스 목록 요청, timeout, user-agent, charset 처리
- `backend/app/external/naver/parser.py`: 뉴스 링크 기반 HTML 파싱, 제목/URL 추출, URL 중복 제거
- `backend/app/external/naver/types.py`: `NaverNewsItem` 타입 정의
- `backend/app/domains/news/service.py`: 수집 실행, 중복 처리, 종목 매칭, 중요도 계산, DB 저장, job 기록
- 저장 테이블: `news`, `news_stock_links`, `news_collect_jobs`, `news_collect_job_items`

## 4. 중복 처리 방식

- `url_hash = sha1(normalized_url)` 기준으로 동일 기사 판단
- `title_hash = sha1(normalized_title)`가 같고 최근 24시간 내 생성된 뉴스는 중복 후보로 처리
- 중복이면 신규 row를 만들지 않고 기존 `news` row의 `duplicate_count`, `source_count`, `sources_json`, `last_published_at`, `importance_score`, `matched_keywords_json`을 갱신
- 신규이면 `news_group_key = date + main_entity + event_type` 형식으로 생성
- 별도 `news_duplicates` 테이블은 만들지 않음

## 5. 종목 매칭 방식

- 대상: `stock_collection_settings.collect_enabled = true`이고 `stocks.is_active = true`인 종목
- 기준: 제목/요약에 종목명, 종목코드, `aliases_json` 값 포함 여부
- 저장: 매칭 시 `news_stock_links`에 `relation_type = "mentioned"`, `relation_score = 1`, `source_stock_code = null`로 저장
- 보유 여부나 고급 분석 점수는 이번 단계에서 사용하지 않음

## 6. Frontend 연결 결과

- 대상 화면: `frontend/src/pages/main/news/NewsPage.vue`
- 구현 기능: 뉴스 KPI, 목록 조회, 키워드 검색, 종목코드 필터, market_scope 필터, 중요도 필터, 발행일 필터, 뉴스 수집 버튼, 최근 job 결과 표시, 상세 drawer
- 표시 컬럼: 발행시각, 제목, 출처, 관련 종목, 중요도, 중복 횟수, 필터 상태, GPT 요약 상태
- 상세 표시: 제목, URL, 출처, 발행시각, 중요도, 중복 정보, 관련 종목, 매칭 키워드, 요약/preview

## 7. 테스트 결과

- `python -m alembic upgrade head`: 성공
- `python seeds/seed_defaults.py`: 성공
- `python -m compileall app`: 성공
- `npm run build`: 성공
- `/api/news/summary`: 200 응답 확인
- `/api/news`: 200 응답 확인
- `/api/news/collect/market`: 테스트용 수집 결과 주입으로 성공 확인
- `news_collect_jobs`: 생성 확인
- `news_collect_job_items`: 생성 확인
- `news`: 신규 row 생성 확인
- `news_stock_links`: 매칭 종목 link 생성 확인
- 중복 수집: 동일 URL 재수집 시 `duplicate_count` 증가 확인
- Regression: `/health`, `/api/auth/status`, `/api/settings`, `/api/stocks`, `/api/collection/stocks/summary` 200 응답 확인
- KODEX XLS import: KODEX 200 200건, KODEX 코스닥150 150건 active 구성종목 확인

## 8. 확인 필요 항목

- 항목: KODEX 파일 갱신 주기
- 이유: 현재 검증은 제공된 로컬 XLS 파일 기준이다.
- 제안: 새 파일 수령 시 동일 import 명령과 새 effective_date로 갱신한다.

- 항목: 네이버 금융 HTML 파싱 안정성
- 이유: 현재 구조는 링크 패턴 기반 parser이며 네이버 HTML 구조 변경 시 누락 가능성이 있다.
- 제안: 운영 수집 로그를 기준으로 필요한 selector/패턴을 추가한다.

- 항목: GPT 요약/필터링
- 이유: 이번 단계는 GPT를 호출하지 않고 keyword 기반 중요도만 저장한다.
- 제안: 다음 단계에서 `gpt_summary_status = pending` 대상만 요약 job으로 처리한다.

## 9. 다음 단계 제안

- 네이버 금융 실제 운영 수집 실행 및 parser 보정
- GPT 요약/재필터링 job 구현
- KRX 가격 데이터 수집 구조 구현
- KRX 가격 데이터 수집 구조 구현
