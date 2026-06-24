# Stock Analyze

개인용 한국 주식 투자 분석 시스템입니다.

현재 상태는 1차 MVP 개발을 위한 기본 골격입니다.

- Backend: FastAPI, SQLAlchemy, Alembic, SQLite
- Frontend: Vue 3, TypeScript, Vite, Element Plus, Pinia, Vue Router, ECharts
- UI 기준: Professional Trading Workspace, 상승 빨강 / 하락 파랑

## 1. Backend 실행

```bash
cd backend
python -m pip install -r requirements.txt
python -m alembic upgrade head
python seeds/seed_defaults.py
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Backend 확인 URL:

```text
http://127.0.0.1:8000/health
```

정상 응답:

```json
{"status":"ok"}
```

## 2. Frontend 실행

새 터미널에서 실행합니다.

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Frontend 접속 URL:

```text
http://127.0.0.1:5173
```

## 3. DB 마이그레이션

SQLite DB는 Backend 폴더 기준으로 생성됩니다.

```bash
cd backend
python -m alembic upgrade head
```

기본 seed 데이터 적용:

```bash
python seeds/seed_defaults.py
```

Seed 포함 항목:

- app_settings 기본값
- scheduled_jobs 기본값
- news_keyword_settings 기본값
- alert_settings 기본값

## 4. 빌드 확인

Frontend production build 확인:

```bash
cd frontend
npm run build
```

Backend Python import/문법 확인:

```bash
cd backend
python -m compileall app
```

## 5. 현재 구현 범위

- 27개 MVP DB 테이블 SQLAlchemy 모델
- Alembic 초기 마이그레이션
- SQLite DB 생성 확인
- 기본 seed 구조
- Backend API 골격
- Frontend 메뉴/화면 골격
- 설정 API CRUD
- 설정 화면 실제 API 연결
- 종목 API CRUD
- 종목 화면 실제 API 연결
- KODEX 구성종목 CSV/XLS/XLSX import 구조
- 수집 종목 관리 API
- 수집 종목 관리 화면 실제 API 연결
- 좌측 메뉴 + 상단 상태 바 기반 투자 분석 UI

## 6. 현재 구현된 설정 API

```text
GET  /api/settings/app-settings
POST /api/settings/app-settings
PUT  /api/settings/app-settings/{setting_id}

GET  /api/settings/scheduled-jobs
POST /api/settings/scheduled-jobs
PUT  /api/settings/scheduled-jobs/{job_id}

GET    /api/settings/news-keywords
POST   /api/settings/news-keywords
PUT    /api/settings/news-keywords/{keyword_id}
DELETE /api/settings/news-keywords/{keyword_id}

GET /api/settings/alert-settings
PUT /api/settings/alert-settings/{setting_id}
```

## 7. 현재 구현된 종목 API

```text
GET    /api/stocks
GET    /api/stocks/search?q=검색어
POST   /api/stocks
GET    /api/stocks/{stock_id}
PUT    /api/stocks/{stock_id}
DELETE /api/stocks/{stock_id}
PATCH  /api/stocks/{stock_id}/favorite
```

`DELETE /api/stocks/{stock_id}`는 실제 삭제가 아니라 `is_active=false` 비활성화 처리입니다.

## 8. 현재 구현된 수집 관리 API

```text
POST /api/collection/index-constituents/import
GET  /api/collection/index-constituents
GET  /api/collection/index-constituents/summary

GET    /api/collection/stocks
GET    /api/collection/stocks/summary
PATCH  /api/collection/stocks/{stock_id}
POST   /api/collection/stocks/{stock_id}/include
POST   /api/collection/stocks/{stock_id}/exclude
POST   /api/collection/stocks/recalculate

GET    /api/collection/rules
POST   /api/collection/rules
PATCH  /api/collection/rules/{rule_id}
DELETE /api/collection/rules/{rule_id}
```

KODEX 구성종목 로컬 파일 import:

```bash
cd backend
python seeds/import_index_constituents.py --file ..\data\KODEX_200.xls --index-code KODEX_200 --index-name "KODEX 200" --effective-date 2026-06-24 --source kodex_xls
python seeds/import_index_constituents.py --file ..\data\KODEX_KOSDAQ_150.xls --index-code KODEX_KOSDAQ_150 --index-name "KODEX 코스닥150" --effective-date 2026-06-24 --source kodex_xls
```

## 9. 아직 필요한 설정

아래 항목은 실제 연동 전 별도 설정이 필요합니다.

- Google OAuth client ID / secret / 허용 이메일
- KRX Open API 인증 정보
- Gmail SMTP 계정 정보
- OpenAI API key
- `OPENAI_NEWS_SUMMARY_MODEL`, `OPENAI_NEWS_FILTER_MODEL` 모델명
- KODEX 구성종목 파일 갱신 주기

## 10. 참고 문서

- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`
- `docs/CODEX_TODO.md`
- `docs/CODEX_PROGRESS.md`
- `docs/DEVELOPMENT_REPORT.md`
- `docs/SCHEMA_VALIDATION_REPORT.md`
- `docs/COLLECTION_TARGET_REPORT.md`
