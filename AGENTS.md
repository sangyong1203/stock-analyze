# Codex 개발 지시 프롬프트 v1.0

## 0. 작업 목표

이 프로젝트는 개인용 투자 분석 시스템이다.

아래 두 문서를 최상위 기준 문서로 삼아 개발을 진행한다.

기준 문서:

1. `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
   - 투자 분석 시스템 개발 계획서 v1.2

2. `docs/MVP_DB_SCHEMA_v1.2.md`
   - 투자 분석 시스템 1차 MVP DB 테이블 확정안 v1.2

두 문서에 확정된 내용만 기준으로 개발한다.
문서에 없는 기능은 임의로 추가하지 않는다.

---

## 1. 핵심 지시 사항

다음 원칙을 반드시 지킨다.

- 기준 문서 2개를 먼저 읽고 개발 범위를 파악한다.
- 분석/논의 과정이 아니라 최종 확정 내용만 기준으로 개발한다.
- 문서에 없는 기능은 임의로 추가하지 않는다.
- 추가 구현이 필요해 보이는 항목은 직접 구현하지 말고 `확인 필요 항목`으로 기록한다.
- 기존 파일이 있다면 최대한 유지하고, 불필요한 구조 변경을 하지 않는다.
- 삭제, 대규모 구조 변경, 기술 스택 변경은 하지 않는다.
- 한 번에 모든 기능을 무리하게 만들지 말고 단계별로 진행한다.
- 작업 전 `docs/CODEX_TODO.md`를 작성한다.
- 작업 중 `docs/CODEX_PROGRESS.md`는 체크포인트 기준으로 갱신한다.
- 작업 완료 후 `docs/DEVELOPMENT_REPORT.md`를 작성한다.
- 모든 작업 완료 후 사용자에게 “모든 지시 내용 작업 완료”라고 명확히 보고한다.

---

## 2. 기술 스택 기준

기준 문서에 따라 아래 기술 스택을 사용한다.

### Frontend

- Vue 3
- TypeScript
- Vite
- Element Plus
- Pinia
- Vue Router
- ECharts

### Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic

### Database

- SQLite

### 외부 연동 예정

- Google OAuth
- Gmail SMTP
- KRX Open API
- 네이버 금융 뉴스
- 네이버 증권 현재가 스냅샷
- OpenAI GPT mini
- GPT-5 계열 모델

DART 공시/기업정보 전용 저장 테이블은 1차 MVP DB에 포함하지 않는다.

---

## 3. 먼저 생성해야 할 문서

프로젝트의 `docs/` 폴더에 아래 문서를 생성한다.

```text
docs/CODEX_TODO.md
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

---

## 4. CODEX_TODO.md 작성 지시

개발 전에 반드시 `docs/CODEX_TODO.md`를 작성한다.

`CODEX_TODO.md`에는 다음 항목을 체크박스 형태로 작성한다.

```markdown
# CODEX TODO

## 1. 기준 문서 확인

- [ ] INVESTMENT_SYSTEM_PLAN_v1.2.md 읽기
- [ ] MVP_DB_SCHEMA_v1.2.md 읽기
- [ ] 1차 MVP 개발 범위 확인
- [ ] 확인 필요 항목 정리

## 2. 프로젝트 구조 확인

- [ ] 현재 프로젝트 파일 구조 확인
- [ ] Backend 구조 확인
- [ ] Frontend 구조 확인
- [ ] docs 폴더 확인
- [ ] 기존 파일 보호 필요 항목 확인

## 3. Backend 기본 구조

- [ ] FastAPI 앱 기본 구조 확인 또는 생성
- [ ] DB 연결 설정
- [ ] SQLAlchemy Base 설정
- [ ] Alembic 설정
- [ ] 환경설정 파일 구조 생성
- [ ] 공통 응답/에러 처리 구조 생성

## 4. DB 모델 구현

- [ ] users
- [ ] app_settings
- [ ] scheduled_jobs
- [ ] system_logs
- [ ] stocks
- [ ] index_constituents
- [ ] stock_prices
- [ ] price_snapshots
- [ ] corporate_actions
- [ ] stock_collection_settings
- [ ] collection_rules
- [ ] news
- [ ] news_stock_links
- [ ] news_keyword_settings
- [ ] news_collect_jobs
- [ ] news_collect_job_items
- [ ] fund_pools
- [ ] fund_transactions
- [ ] trades
- [ ] trade_news_links
- [ ] holdings
- [ ] price_alerts
- [ ] alert_settings
- [ ] alert_histories
- [ ] memos
- [ ] tags
- [ ] tag_links

## 5. DB 인덱스/제약조건

- [ ] 필수 UNIQUE 인덱스 반영
- [ ] 조회용 인덱스 반영
- [ ] 외래키 관계 반영
- [ ] SQLite 기준 호환성 확인

## 6. Alembic 마이그레이션

- [ ] 초기 마이그레이션 생성
- [ ] 마이그레이션 실행 확인
- [ ] SQLite DB 생성 확인

## 7. Seed 데이터 구조

- [ ] 기본 app_settings seed 구조 생성
- [ ] 기본 scheduled_jobs seed 구조 생성
- [ ] 기본 news_keyword_settings seed 구조 생성
- [ ] 기본 alert_settings seed 구조 생성
- [ ] KODEX 200 / KODEX 코스닥150 구성종목 seed 구조 준비

## 8. Backend API 골격

- [ ] 인증 API 골격
- [ ] 종목 API 골격
- [ ] 수집 종목 관리 API 골격
- [ ] 뉴스 API 골격
- [ ] 포트폴리오 API 골격
- [ ] 거래 기록 API 골격
- [ ] 알림 API 골격
- [ ] 차트 데이터 API 골격
- [ ] 메모/태그 API 골격
- [ ] 설정 API 골격

## 9. Frontend 기본 구조

- [ ] Vue Router 메뉴 구조 생성
- [ ] MainLayout 생성
- [ ] 대시보드 화면 골격
- [ ] 종목 화면 골격
- [ ] 수집 종목 관리 화면 골격
- [ ] 뉴스 화면 골격
- [ ] 포트폴리오 화면 골격
- [ ] 거래 기록 화면 골격
- [ ] 알림 관리 화면 골격
- [ ] 차트 화면 골격
- [ ] 메모/태그 화면 골격
- [ ] 설정 화면 골격

## 10. 실행 확인

- [ ] Backend 실행 확인
- [ ] Frontend 실행 확인
- [ ] DB 생성 확인
- [ ] Alembic migration 확인
- [ ] 기본 API 응답 확인

## 11. 문서 갱신

- [ ] CODEX_PROGRESS.md 갱신
- [ ] DEVELOPMENT_REPORT.md 작성
- [ ] 완료/미완료/확인 필요 항목 정리
```

---

## 5. CODEX_PROGRESS.md 작성 지시

`docs/CODEX_PROGRESS.md`는 실시간 로그 파일이 아니라 작업 체크포인트 문서다.

매 파일 수정마다 갱신하지 않는다.

다음 조건에서만 갱신한다.

- 새로운 Phase를 시작할 때
- Phase 하나를 완료했을 때
- 주요 작업 묶음을 완료했을 때
- DB 모델, 마이그레이션, API 골격, Frontend 메뉴 구조처럼 중요한 산출물이 생겼을 때
- 실행 확인, 테스트, 마이그레이션 결과가 나왔을 때
- 막힌 항목이 생겼을 때
- 확인 필요 항목이 생겼을 때
- 작업을 중단하기 전
- 전체 작업 완료 직전

작은 코드 수정, import 정리, 단순 오타 수정, 스타일 수정처럼 미세한 변경마다 갱신하지 않는다.

갱신 시에는 다음 형식을 사용한다.

```markdown
# CODEX PROGRESS

## 현재 작업 상태

- 현재 단계:
- 마지막 작업 시간:
- 전체 진행률:
- 현재 작업 중인 파일:

## 완료한 작업

- [x] 작업명
  - 설명:
  - 관련 파일:

## 진행 중인 작업

- [ ] 작업명
  - 현재 상태:
  - 남은 작업:

## 남은 작업

- [ ] 작업명

## 막힌 항목

- 항목:
- 원인:
- 필요한 확인:

## 생성한 파일

- 파일 경로:
- 설명:

## 수정한 파일

- 파일 경로:
- 수정 내용:

## 확인 필요 항목

- 항목:
- 이유:
- 제안:
```

---

## 6. DEVELOPMENT_REPORT.md 작성 지시

모든 작업이 끝나면 `docs/DEVELOPMENT_REPORT.md`를 작성한다.

아래 형식을 반드시 사용한다.

````markdown
# DEVELOPMENT REPORT

## 1. 작업 개요

- 프로젝트명:
- 작업 기준 문서:
  - INVESTMENT_SYSTEM_PLAN_v1.2.md
  - MVP_DB_SCHEMA_v1.2.md
- 작업 범위:
- 작업 완료 여부:

## 2. 완료한 작업

- [x] 작업명
  - 설명:
  - 관련 파일:

## 3. 생성한 파일

| 파일 | 설명 |
| ---- | ---- |
| path | 설명 |

## 4. 수정한 파일

| 파일 | 수정 내용 |
| ---- | --------- |
| path | 설명      |

## 5. 구현한 Backend 항목

- FastAPI 구조:
- DB 연결:
- SQLAlchemy 모델:
- Alembic:
- API 라우터:
- Seed 구조:

## 6. 구현한 Frontend 항목

- 라우터:
- 레이아웃:
- 메뉴:
- 화면 골격:
- API 연결 상태:

## 7. DB 구현 결과

- 생성한 테이블 수:
- 생성한 테이블 목록:
- 생성한 인덱스:
- 마이그레이션 파일:
- SQLite DB 생성 여부:

## 8. 실행 방법

### Backend

```bash
명령어 작성
```

### Frontend

```bash
명령어 작성
```

### Migration

```bash
명령어 작성
```

## 9. 테스트 결과

- Backend 실행:
- Frontend 실행:
- DB migration:
- 기본 API 테스트:
- 오류 여부:

## 10. 미완료 항목

- 항목:
- 이유:
- 다음 작업 제안:

## 11. 확인 필요 항목

- 항목:
- 확인이 필요한 이유:
- 제안:

## 12. 다음 단계 제안

- 다음 단계 1:
- 다음 단계 2:
- 다음 단계 3:

## 13. 최종 완료 선언

모든 지시 내용 작업 완료 여부:

- [ ] 완료
- [ ] 일부 미완료

최종 메시지:

“요청받은 기준 문서 기반 작업을 완료했습니다. DEVELOPMENT_REPORT.md를 확인해 주세요.”
````

---

## 7. Backend 개발 기준

Backend는 도메인 단위로 나누어 구현한다.

추천 구조:

```text
backend/
  app/
    main.py
    core/
      config.py
      security.py
    db/
      base.py
      session.py
      init_db.py
    domains/
      auth/
      stocks/
      prices/
      collection/
      news/
      portfolio/
      trades/
      alerts/
      charts/
      memos/
      settings/
    common/
      schemas.py
      errors.py
      responses.py
    external/
      krx/
      naver/
      gmail/
      openai/
```

도메인별 기본 파일 구조:

```text
domains/{domain}/
  models.py
  schemas.py
  router.py
  service.py
  repository.py
```

과도하게 파일을 쪼개지 않는다.
단, 모델/스키마/라우터/서비스/저장소는 분리한다.

---

## 8. Frontend 개발 기준

Frontend는 메뉴 단위로 구성한다.

추천 구조:

```text
frontend/
  src/
    main.ts
    App.vue
    router/
      index.ts
      routes.ts
    layouts/
      MainLayout.vue
      AuthLayout.vue
      EmptyLayout.vue
    pages/
      login/
      main/
        dashboard/
        stocks/
        collection/
        news/
        portfolio/
        trades/
        alerts/
        charts/
        memos/
        settings/
    shared/
      components/
      composables/
      constants/
      types/
      utils/
```

메뉴별 내부 구조:

```text
pages/main/{menu}/
  {Menu}Page.vue
  components/
  composables/
  service/
    {menu}.api.ts
    {menu}.types.ts
    {menu}.mapper.ts
    {menu}.store.ts
    {menu}.constants.ts
    {menu}.utils.ts
```

화면 전용 API, 타입, store, mapper, constants, utils는 해당 메뉴의 `service/` 아래에 둔다.

---

## 9. DB 구현 기준

`docs/MVP_DB_SCHEMA_v1.2.md`에 정의된 27개 테이블을 구현한다.

테이블 목록:

```text
users
app_settings
scheduled_jobs
system_logs

stocks
index_constituents
stock_prices
price_snapshots
corporate_actions

stock_collection_settings
collection_rules

news
news_stock_links
news_keyword_settings
news_collect_jobs
news_collect_job_items

fund_pools
fund_transactions
trades
trade_news_links
holdings

price_alerts
alert_settings
alert_histories

memos
tags
tag_links
```

반드시 반영할 것:

- 외래키 관계
- created_at / updated_at
- JSON 저장 필드
- 필수 인덱스
- UNIQUE 제약조건
- SQLite 호환성

---

## 10. 1차 구현 우선순위

처음부터 전체 기능을 완성하려고 하지 말고 아래 순서대로 진행한다.

### Phase 1. 프로젝트 기초

- 문서 확인
- TODO 작성
- Backend 구조 생성
- Frontend 구조 생성
- 환경설정 구조 생성

### Phase 2. DB 기초

- SQLAlchemy 모델 생성
- Alembic 설정
- 초기 마이그레이션 생성
- SQLite DB 생성 확인
- Seed 구조 생성

### Phase 3. Backend API 골격

- 종목 API
- 수집 종목 관리 API
- 뉴스 API
- 거래 API
- 포트폴리오 API
- 알림 API
- 차트 데이터 API
- 메모/태그 API
- 설정 API

### Phase 4. Frontend 화면 골격

- 메뉴 라우팅
- MainLayout
- 각 메뉴 페이지 골격
- 기본 테이블/폼/필터 UI

### Phase 5. 실행 확인 및 보고

- Backend 실행 확인
- Frontend 실행 확인
- Migration 확인
- 기본 API 확인
- CODEX_PROGRESS.md 갱신
- DEVELOPMENT_REPORT.md 작성

---

## 11. 구현하지 말아야 할 항목

아래 항목은 1차 MVP 범위가 아니므로 구현하지 않는다.

```text
auth_sessions
stock_indicators
trade_reviews
stock_scores
news_duplicates
disclosures
company_profiles
backtest_results
reports
```

DART 공시/기업정보 전용 저장 테이블은 1차 MVP DB에 포함하지 않는다.

---

## 12. 확인 필요 항목 처리 방식

개발 중 애매한 사항이 있으면 임의로 결정하지 않는다.

다음 방식으로 처리한다.

```markdown
## 확인 필요 항목

- 항목:
- 관련 문서:
- 애매한 이유:
- 가능한 선택지:
- 추천안:
- 현재 구현 여부: 보류
```

확인 필요 항목은 `docs/CODEX_PROGRESS.md`와 `docs/DEVELOPMENT_REPORT.md`에 모두 기록한다.

---

## 13. 완료 조건

작업 완료 조건은 다음과 같다.

- `docs/CODEX_TODO.md` 작성 완료
- `docs/CODEX_PROGRESS.md` 갱신 완료
- SQLAlchemy 모델 생성 완료
- Alembic 마이그레이션 생성 완료
- SQLite DB 생성 확인
- 기본 seed 구조 생성
- Backend API 골격 생성
- Frontend 메뉴/화면 골격 생성
- 실행 방법 문서화
- `docs/DEVELOPMENT_REPORT.md` 작성 완료
- 완료/미완료/확인 필요 항목 정리 완료

작업이 끝나면 사용자에게 다음과 같이 보고한다.

```text
모든 지시 내용 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
