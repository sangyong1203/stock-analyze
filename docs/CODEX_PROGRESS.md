# CODEX PROGRESS

## Current phase

- Phase: non-ETF initial portfolio input and validation
- Task document: `docs/CODEX_TASK_2.4.md`
- Status: backup completed, non-ETF input completed, API validation completed, browser preview check partially completed

## Completed major work

- Reviewed current task context and prior input report documents:
  - `docs/DEVELOPMENT_REPORT.md`
  - `docs/INITIAL_PORTFOLIO_INPUT_REPORT.md`
  - `docs/FIRST_OPERATION_DATA_INPUT_GUIDE.md`
- Reused the live DB state preserved after `CODEX_TASK_2.3`
- Verified pre-input baseline remained empty:
  - no fund pools
  - no fund transactions
  - no trades
  - no holdings
- Verified the four non-ETF stock codes already exist in `stocks`:
  - `006400`
  - `034020`
  - `028050`
  - `035420`
- Kept the five ETF codes excluded by user decision:
  - `368590`
  - `411060`
  - `442320`
  - `422420`
  - `487240`
- Verified task-specific backup file exists:
  - `storage/backups/stock_analyze_before_non_etf_initial_input_20260703_111724.db`
- Created fund pool:
  - `기본 투자계좌`
- Inserted initial deposit:
  - `5,108,090`
- Inserted four initial BUY trades on `2026-07-03`
- Verified holdings were recalculated automatically
- Verified ETF trades and ETF holdings were not created
- Added `docs/NON_ETF_INITIAL_PORTFOLIO_INPUT_REPORT.md`
- Added `docs/CODEX_TASK_2.4_REPORT.md`

## Verification result

| Item | Result |
|---|---|
| `python -m compileall app` | success |
| `npm run build` | success |
| `/health` | 200 |
| `/api/funds/summary` | 200 |
| `/api/trades` | 200 |
| `/api/holdings` | 200 |
| `/api/holdings/summary` | 200 |
| `/api/portfolio/summary` | 200 |
| `/api/dashboard/summary` | 200 |
| active fund pool count | 1 |
| trade row count | 4 |
| holding count | 4 |
| ETF trade rows | 0 |
| ETF holding rows | 0 |

## Current validated data state

- Fund pool:
  - `기본 투자계좌`
- Deposit:
  - `5,108,090`
- Trades:
  - `006400` quantity `5`, average price `596970`
  - `034020` quantity `10`, average price `105215`
  - `028050` quantity `10`, average price `55809`
  - `035420` quantity `2`, average price `256500`
- Funds summary:
  - `active_pool_count = 1`
  - `total_cash = 0`
  - `total_deposit_amount = 5108090.00`
  - `transaction_count = 5`
- Holdings summary:
  - `holding_count = 4`
  - `closed_holding_count = 0`
- Portfolio summary:
  - `holding_count = 4`
  - `total_invested_amount = 5108090.00`
  - `total_cash = 0`
- Dashboard summary:
  - `recent_trades` count includes the 4 inserted BUY rows
  - top holdings contain only the 4 non-ETF stocks

## Confirmation-needed items

- Item: in-app browser preview did not complete real data rendering verification
- Reason: `vite preview` page shell opened, but `/api/*` fetch failed in preview mode and screen-level value rendering could not be trusted from the preview browser pass
- Recommendation: if browser QA is required, rerun against the actual frontend runtime configuration used for API connectivity
- Current implementation status: API-level validation completed, browser preview validation partial

## Next step suggestions

- Use the current four-stock, non-ETF portfolio as the new baseline for the next operational input task
- If browser QA remains required, run a dedicated connected frontend session and recheck `/portfolio`, `/trades`, and `/dashboard`
