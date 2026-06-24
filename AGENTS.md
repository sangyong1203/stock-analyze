# AGENTS.md

## 1. Project Overview

This repository is for developing a personal investment analysis system.

The system is built for private use and follows the confirmed 1st MVP scope.

Do not add features that are not confirmed in the reference documents.

---

## 2. Required Reference Documents

Before making changes, always read the following documents:

```text
docs/INVESTMENT_SYSTEM_PLAN_v1.2.md
docs/MVP_DB_SCHEMA_v1.2.md
```

These two documents are the source of truth for the current MVP.

Use only the confirmed content from these documents.

---

## 3. Core Development Rules

- Follow the confirmed MVP scope only.
- Do not implement features that are not defined in the reference documents.
- Do not add speculative features.
- Do not change the selected tech stack.
- Do not perform large project restructuring unless necessary.
- Do not remove existing files or code without a clear reason.
- Preserve existing structure when possible.
- Implement step by step.
- Keep code practical, maintainable, and MVP-focused.
- If something is unclear, record it as `확인 필요 항목` instead of deciding silently.
- Do not treat discussion history or draft ideas as confirmed requirements.

---

## 4. Tech Stack

### Frontend

```text
Vue 3
TypeScript
Vite
Element Plus
Pinia
Vue Router
ECharts
```

### Backend

```text
Python
FastAPI
SQLAlchemy
Alembic
Pydantic
```

### Database

```text
SQLite
```

### External Integrations Planned

```text
Google OAuth
Gmail SMTP
KRX Open API
Naver Finance News
Naver Finance Current Price Snapshot
OpenAI GPT mini
GPT-5 series model
```

DART disclosure/company profile storage tables are not included in the 1st MVP DB.

---

## 5. Required Work Tracking Documents

Maintain the following documents under `docs/`:

```text
docs/CODEX_TODO.md
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

### CODEX_TODO.md

Use this as the task checklist.

It should include:

```text
- Reference document review
- Project structure review
- Backend work
- DB model/migration work
- Seed work
- Backend API work
- Frontend structure/page work
- Execution/test checks
- Documentation/reporting
```

### CODEX_PROGRESS.md

This is not a real-time log file.

Do not update it after every small file change.

Update it only when:

```text
- A new Phase starts
- A Phase is completed
- A major task group is completed
- DB models, migrations, API skeletons, or Frontend menu structures are completed
- Execution, test, or migration results are available
- A blocker appears
- A confirmation-needed item appears
- Work is about to stop
- All work is nearly complete
```

Small changes such as import cleanup, minor typo fixes, simple style fixes, or one-field edits do not require progress document updates.

### DEVELOPMENT_REPORT.md

Write this after completing the instructed work.

It must include:

```text
- Work overview
- Reference documents
- Completed work
- Generated files
- Modified files
- Backend implementation result
- Frontend implementation result
- DB implementation result
- Execution method
- Test result
- Incomplete items
- Confirmation-needed items
- Next step suggestions
- Final completion statement
```

---

## 6. Backend Structure Rules

Backend should use a domain-based structure.

Recommended structure:

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

Each domain may use this structure:

```text
domains/{domain}/
  models.py
  schemas.py
  router.py
  service.py
  repository.py
```

Do not over-split files.

Separate models, schemas, routers, services, and repositories where appropriate.

---

## 7. Frontend Structure Rules

Frontend should use a menu-based structure.

Recommended structure:

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

Menu-specific files should be placed under each menu folder.

Recommended menu structure:

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

Screen-specific API, types, store, mapper, constants, and utils should live under the menu's `service/` folder.

---

## 8. DB Implementation Rules

Use `docs/MVP_DB_SCHEMA_v1.2.md` as the DB source of truth.

The 1st MVP DB contains 27 tables:

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

The implementation must include:

```text
- Foreign key relationships
- created_at / updated_at fields
- JSON storage fields
- Required indexes
- UNIQUE constraints
- SQLite compatibility
```

Do not create the following excluded tables unless the user confirms them later:

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

DART disclosure/company profile storage tables are excluded from the 1st MVP DB.

---

## 9. 1st MVP Development Priority

Follow this order unless the user gives a different task.

### Phase 1. Project Foundation

```text
- Read reference documents
- Review project structure
- Create/update CODEX_TODO.md
- Set up Backend structure
- Set up Frontend structure
- Set up environment configuration
```

### Phase 2. DB Foundation

```text
- SQLAlchemy models
- Alembic setup
- Initial migration
- SQLite DB creation check
- Seed structure
```

### Phase 3. Backend API

```text
- Auth API
- Stocks API
- Collection target API
- News API
- Portfolio API
- Trades API
- Alerts API
- Charts API
- Memos/Tags API
- Settings API
```

### Phase 4. Frontend Screens

```text
- Router
- MainLayout
- Menu pages
- Basic tables/forms/filters
- API connection per screen
```

### Phase 5. Validation and Report

```text
- Backend execution check
- Frontend execution check
- Migration check
- Basic API check
- CODEX_PROGRESS.md update
- DEVELOPMENT_REPORT.md update
```

---

## 10. Confirmation Needed Items

If an item is unclear, do not implement it silently.

Record it in:

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

Use this format:

```markdown
## 확인 필요 항목

- 항목:
- 관련 문서:
- 애매한 이유:
- 가능한 선택지:
- 추천안:
- 현재 구현 여부: 보류
```

---

## 11. Completion Rules

At the end of each instructed task, update:

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

The report must clearly separate:

```text
- Completed items
- Incomplete items
- Confirmation-needed items
- Next step suggestions
```

When all instructed work is complete, report to the user:

```text
모든 지시 내용 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```

---

## 12. Task-Specific Instructions

Do not append one-time task prompts directly into `AGENTS.md`.

For one-time tasks, use either:

```text
- Direct Codex chat instruction
- Separate file under docs/, such as docs/CODEX_TASK_YYYYMMDD_TASK_NAME.md
```

`AGENTS.md` should remain the permanent project rule file.
