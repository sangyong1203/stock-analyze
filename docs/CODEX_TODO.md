# CODEX TODO

## 1. 기준 문서 확인

- [x] INVESTMENT_SYSTEM_PLAN_v1.2.md 읽기
- [x] MVP_DB_SCHEMA_v1.2.md 읽기
- [x] 1차 MVP 개발 범위 확인
- [x] 확인 필요 항목 정리

## 2. 프로젝트 구조 확인

- [x] 현재 프로젝트 파일 구조 확인
- [x] Backend 구조 확인
- [x] Frontend 구조 확인
- [x] docs 폴더 확인
- [x] 기존 파일 보호 필요 항목 확인

## 3. Backend 기본 구조

- [x] FastAPI 앱 기본 구조 확인 또는 생성
- [x] DB 연결 설정
- [x] SQLAlchemy Base 설정
- [x] Alembic 설정
- [x] 환경설정 파일 구조 생성
- [x] 공통 응답/에러 처리 구조 생성

## 4. DB 모델 구현

- [x] users
- [x] app_settings
- [x] scheduled_jobs
- [x] system_logs
- [x] stocks
- [x] index_constituents
- [x] stock_prices
- [x] price_snapshots
- [x] corporate_actions
- [x] stock_collection_settings
- [x] collection_rules
- [x] news
- [x] news_stock_links
- [x] news_keyword_settings
- [x] news_collect_jobs
- [x] news_collect_job_items
- [x] fund_pools
- [x] fund_transactions
- [x] trades
- [x] trade_news_links
- [x] holdings
- [x] price_alerts
- [x] alert_settings
- [x] alert_histories
- [x] memos
- [x] tags
- [x] tag_links

## 5. DB 인덱스/제약조건

- [x] 필수 UNIQUE 인덱스 반영
- [x] 조회용 인덱스 반영
- [x] 외래키 관계 반영
- [x] SQLite 기준 호환성 확인

## 6. Alembic 마이그레이션

- [x] 초기 마이그레이션 생성
- [x] 마이그레이션 실행 확인
- [x] SQLite DB 생성 확인

## 7. Seed 데이터 구조

- [x] 기본 app_settings seed 구조 생성
- [x] 기본 scheduled_jobs seed 구조 생성
- [x] 기본 news_keyword_settings seed 구조 생성
- [x] 기본 alert_settings seed 구조 생성
- [x] KODEX 200 / KODEX 코스닥150 구성종목 seed 구조 준비

## 8. Backend API 골격

- [x] 인증 API 골격
- [x] 종목 API 골격
- [x] 수집 종목 관리 API 골격
- [x] 뉴스 API 골격
- [x] 포트폴리오 API 골격
- [x] 거래 기록 API 골격
- [x] 알림 API 골격
- [x] 차트 데이터 API 골격
- [x] 메모/태그 API 골격
- [x] 설정 API 골격

## 9. Frontend 기본 구조

- [x] Vue Router 메뉴 구조 생성
- [x] MainLayout 생성
- [x] 대시보드 화면 골격
- [x] 종목 화면 골격
- [x] 수집 종목 관리 화면 골격
- [x] 뉴스 화면 골격
- [x] 포트폴리오 화면 골격
- [x] 거래 기록 화면 골격
- [x] 알림 관리 화면 골격
- [x] 차트 화면 골격
- [x] 메모/태그 화면 골격
- [x] 설정 화면 골격

## 10. 실행 확인

- [x] Backend 실행 확인
- [x] Frontend 실행 확인
- [x] DB 생성 확인
- [x] Alembic migration 확인
- [x] 기본 API 응답 확인

## 11. 문서 갱신

- [x] CODEX_PROGRESS.md 갱신
- [x] DEVELOPMENT_REPORT.md 작성
- [x] 완료/미완료/확인 필요 항목 정리
