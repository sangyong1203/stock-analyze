# CODEX PROGRESS

## Current phase

- Phase: Google OAuth environment variable verification
- Task document: `docs/CODEX_TASK_2.20A.md`
- Status: code-side env names, file locations, placeholder example values, and user-input-required items documented without exposing real secrets or running login

## Completed major work

- Reviewed:
  - `docs/CODEX_TASK_2.20A.md`
  - `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
  - `docs/MVP_DB_SCHEMA_v1.2.md`
- Verified Google OAuth related setting names from code:
  - `GOOGLE_CLIENT_ID`
  - `GOOGLE_CLIENT_SECRET`
  - `GOOGLE_ALLOWED_EMAIL`
- Verified settings source file:
  - `backend/app/core/config.py`
- Verified auth readiness logic:
  - `backend/app/domains/auth/service.py`
  - `oauth_configured` depends on both client ID and client secret
  - `allowed_email_configured` depends on allowed email
- Verified `.env` file locations:
  - `backend/.env`
  - `backend/.env.example`
- Updated `backend/.env.example` Google OAuth entries to explicit placeholder format
- Added:
  - `docs/CODEX_TASK_2.20A_REPORT.md`

## Verification result

| Item | Result |
|---|---|
| Google OAuth env names found in code | yes |
| `.env` location confirmed | `backend/.env` |
| `.env.example` location confirmed | `backend/.env.example` |
| Real client values printed | no |
| Real login test executed | no |

## Current validated configuration notes

- Required Google OAuth keys for this MVP:
  - `GOOGLE_CLIENT_ID`
  - `GOOGLE_CLIENT_SECRET`
  - `GOOGLE_ALLOWED_EMAIL`
- Placeholder format is now present in `backend/.env.example`
- User still needs to enter the real Google OAuth values manually in `backend/.env`

## Confirmation-needed items

- Item: actual Google OAuth login remains unverified
- Reason: this task was limited to env item confirmation and documentation only
- Recommendation: run login verification in a separate explicit task after real values are entered
- Current implementation status: pending external credential input

## Next step suggestions

- Fill the three Google OAuth values in `backend/.env`
- After credential input, verify `/api/auth/status` again
- Run actual login test only in a separate explicit task
