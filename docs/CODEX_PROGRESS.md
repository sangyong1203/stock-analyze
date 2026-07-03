# CODEX PROGRESS

## Current phase

- Phase: first operation data input preparation
- Task document: `docs/CODEX_TASK_2.2.md`
- Status: DB backup, baseline verification, and first-operation input guide complete

## Completed major work

- Reviewed current operation-readiness and MVP completion documents
- Created a pre-operation SQLite backup under `storage/backups/`
- Verified backup integrity by checking:
  - source DB path
  - backup file creation
  - non-zero backup size
  - size match between source DB and backup DB
- Confirmed that no live operating data was provided by the user in this session
- Kept the instructed constraint:
  - no guessed fund amount
  - no guessed stock code
  - no guessed quantity
  - no guessed average price
- Rechecked baseline portfolio-related APIs before any real input:
  - `/api/funds/summary`
  - `/api/holdings/summary`
  - `/api/portfolio/summary`
  - `/api/dashboard/summary`
  - `/api/trades`
- Reconfirmed current baseline is still empty for funds, holdings, portfolio, and trades
- Added `docs/FIRST_OPERATION_DATA_INPUT_GUIDE.md`
- Added `docs/CODEX_TASK_2.2_REPORT.md`

## Verification result

| Item | Result |
|---|---|
| DB backup created | success |
| Backup file size | non-zero |
| Source vs backup size match | success |
| `python -m compileall app` | success |
| `npm run build` | success |
| `/health` | 200 |
| `/api/auth/status` | 200 |
| `/api/funds/summary` | 200 |
| `/api/holdings/summary` | 200 |
| `/api/portfolio/summary` | 200 |
| `/api/dashboard/summary` | 200 |
| `/api/trades` | 200 |
| Real operating data input | not performed |

## Confirmation-needed items

- Item: real first-operation data was not provided by the user
- Reason: the task explicitly forbids arbitrary live-data entry
- Current result:
  - no fund pool created
  - no deposit entered
  - no holdings input performed
  - no trade input performed
- Recommendation: use `docs/FIRST_OPERATION_DATA_INPUT_GUIDE.md` and provide actual values only when ready

- Item: browser-side verification for `/portfolio`, `/trades`, `/dashboard` could not be completed in this session
- Reason: in-app browser page loads repeatedly timed out in the current session
- Recommendation: perform one short human browser pass when entering real data

## Next step suggestions

- When real initial values are ready, follow `docs/FIRST_OPERATION_DATA_INPUT_GUIDE.md` in order
- Keep the created pre-operation backup untouched until the first real input cycle is finished and verified
