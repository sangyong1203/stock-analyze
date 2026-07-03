# CODEX PROGRESS

## Current phase

- Phase: phase-2 operation readiness check
- Task document: `docs/CODEX_TASK_2.1.md`
- Status: environment readiness check, backup plan setup, dry-run verification, and reporting complete

## Completed major work

- Reviewed current completion documents:
  - `docs/DEVELOPMENT_REPORT.md`
  - `docs/MVP_COMPLETION_REPORT.md`
- Rechecked backend settings loading structure for:
  - local CORS support
  - Gmail SMTP config loading
  - OpenAI config loading
  - KRX auth key loading
  - SQLite DB path usage
- Verified current environment status without exposing sensitive values
- Confirmed current frontend API base behavior:
  - `VITE_API_BASE_URL` override supported
  - fallback base URL is `http://127.0.0.1:8000`
- Updated `backend/.env.example` to include `ALLOWED_ORIGINS`
- Created backup target directory placeholder:
  - `storage/backups/`
- Added `docs/OPERATION_READY_CHECKLIST.md`
- Added `docs/CODEX_TASK_2.1_REPORT.md`
- Reconfirmed dry-run and regression endpoints without actual send

## Verification result

| Item | Result |
|---|---|
| Gmail SMTP env status | configured |
| OpenAI env status | configured |
| KRX env status | configured |
| SQLite DB path | configured |
| Backup target directory placeholder | created |
| Auth runtime status | oauth not configured |
| `/health` | 200 |
| `/api/auth/status` | 200 |
| `/api/jobs/summary` | 200 |
| `/api/prices/summary` | 200 |
| `/api/news/summary` | 200 |
| `/api/price-alerts/summary` | 200 |
| `/api/news/alerts/send/dry-run` | 200 |
| `/api/price-alerts/evaluate/dry-run` | 200 |
| `python -m compileall app` | success |
| `npm run build` | success |

## Confirmation-needed items

- Item: Google OAuth environment variables are still missing in the current `.env`
- Related verification:
  - `GOOGLE_CLIENT_ID`
  - `GOOGLE_CLIENT_SECRET`
  - `GOOGLE_ALLOWED_EMAIL`
  - `/api/auth/status`
- Reason: auth runtime currently reports `oauth_configured=false` and `allowed_email_configured=false`
- Recommendation: configure OAuth only if login flow is required for the next real-user run
- Current implementation status: no code change needed in this task

- Item: `ALLOWED_ORIGINS` is absent from the current `.env`, but runtime still works via default value and legacy `ALLOWED_ORIGIN`
- Recommendation: adopt explicit `ALLOWED_ORIGINS` in real environment files for clarity

## Next step suggestions

- Before first live use, follow `docs/OPERATION_READY_CHECKLIST.md` in order
- Consider rotating any real secrets stored in local `.env` outside the app workflow if they were previously shared or exposed
