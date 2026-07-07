# CODEX PROGRESS

## Current phase

- Phase: frontend auth persistence and protected-route minimum wiring
- Task document: `docs/CODEX_TASK_2.21.md`
- Status: frontend auth persistence, protected routes, logout, and backend redirect handoff verified

## Completed major work

- Reviewed:
  - `docs/CODEX_TASK_2.21.md`
  - `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
  - `docs/MVP_DB_SCHEMA_v1.2.md`
- Confirmed pre-task frontend state:
  - login success opened dashboard but auth state was not persisted on frontend
  - protected routes were not guarded
  - logout action was not present
- Added frontend auth utility using localStorage
- Added router guard for minimum protected routes:
  - `/dashboard`
  - `/portfolio`
  - `/alerts`
  - `/news`
  - `/settings`
- Added login redirect handling through `/login?redirect=...`
- Added logout action in `MainLayout`
- Added backend OAuth redirect cookie support so post-login return path can be restored
- Rebuilt frontend successfully
- Revalidated backend auth readiness and frontend route behavior
- Added:
  - `docs/CODEX_TASK_2.21_REPORT.md`

## Verification result

| Item | Result |
|---|---|
| Frontend build | passed |
| `/api/auth/status` ready flags | true / true |
| Unauthenticated `/dashboard` redirect | passed |
| OAuth success saves auth state | passed |
| Reload keeps dashboard access | passed |
| Logout clears auth state | passed |
| `/portfolio` redirect after logout | passed |
| Real Gmail sent | no |

## Current validated configuration notes

- Frontend auth persistence key:
  - `stock-analyze-authenticated`
- Backend login route now accepts optional relative redirect:
  - `/api/auth/google/login?redirect=/portfolio`
- OAuth success redirect still uses frontend `auth=success` marker, then frontend strips it from final URL

## Confirmation-needed items

- None

## Next step suggestions

- Upgrade to server-side auth validation only when a later task explicitly requires stronger access control
