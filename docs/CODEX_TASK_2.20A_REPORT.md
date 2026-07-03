# CODEX_TASK_2.20A REPORT

## Work overview

- Task scope: verify Google OAuth environment variable items only
- Constraint kept:
  - no real client secret output
  - no real login test
  - no backend or frontend code change
  - no schema change
  - no migration

## Reference documents

- `docs/CODEX_TASK_2.20A.md`
- `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- `docs/MVP_DB_SCHEMA_v1.2.md`

## Completed work

- Checked the current code path for Google OAuth related settings
- Confirmed the backend settings file location and `.env` loading behavior
- Confirmed the `.env` and `.env.example` file locations
- Confirmed the auth status check logic for Google OAuth readiness
- Updated `backend/.env.example` to show placeholder values for Google OAuth fields
- Documented which `.env` items the user must fill manually

## Backend implementation result

- No backend code change
- Verified setting source:
  - `backend/app/core/config.py`
- Verified auth readiness check:
  - `backend/app/domains/auth/service.py`

## DB implementation result

- No schema change
- No new table
- No migration

## Required Google OAuth env items

Use these keys in `backend/.env`:

```text
GOOGLE_CLIENT_ID=your-google-oauth-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-oauth-client-secret
GOOGLE_ALLOWED_EMAIL=your-google-account@example.com
```

## User input required

- `GOOGLE_CLIENT_ID`
  - paste the OAuth client ID issued by Google Cloud
- `GOOGLE_CLIENT_SECRET`
  - paste the OAuth client secret issued by Google Cloud
- `GOOGLE_ALLOWED_EMAIL`
  - enter the single Google account email allowed to sign in for this personal MVP

## Test result

- Code setting names confirmed:
  - `GOOGLE_CLIENT_ID`
  - `GOOGLE_CLIENT_SECRET`
  - `GOOGLE_ALLOWED_EMAIL`
- `.env` loading location confirmed:
  - `backend/.env`
- `.env.example` location confirmed:
  - `backend/.env.example`
- Auth readiness logic confirmed:
  - OAuth ready requires both client ID and client secret
  - allowed email ready requires allowed email value
- No real client value was printed in this task
- No real login test was executed in this task

## Incomplete items

- Real Google OAuth credentials still need to be entered by the user in `backend/.env`
- Actual login test was intentionally not executed in this task

## Confirmation-needed items

- None

## Final completion statement

CODEX_TASK_2.20A Google OAuth `.env` item verification completed.
