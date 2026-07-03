# CODEX PROGRESS

## Current phase

- Phase: price collect to holdings recalculation link verification
- Task document: `docs/CODEX_TASK_2.16.md`
- Status: automatic holdings recalculation was missing, linked with minimal fix, and verified through daily API, range API, and manual job run

## Completed major work

- Reviewed:
  - `docs/CODEX_TASK_2.16.md`
  - `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
  - `docs/MVP_DB_SCHEMA_v1.2.md`
- Confirmed existing behavior before fix:
  - KRX daily/range collect updated `stock.current_price`
  - holdings recalculation was not automatically chained from price collect
  - portfolio/dashboard correctness therefore depended on a separate manual holdings recalculation step
- Evaluated fix scope:
  - change was localized to `backend/app/domains/prices/service.py`
  - no schema or migration required
- Applied minimal fix:
  - after non-dry-run `collect_krx_daily_prices(...)`, call `recalculate_holdings(db)`
  - after non-dry-run `collect_krx_range_prices(...)`, call `recalculate_holdings(db)`
- Restarted backend server on `127.0.0.1:8000`
- Verified automatic link with live APIs:
  - before collect, latest holding `created_at = 2026-07-03T06:32:52.947762`
  - after daily collect, latest holding `created_at = 2026-07-03T06:50:34.752168`
  - after range collect, latest holding `created_at = 2026-07-03T06:50:42.187389`
  - after scheduled job manual run, latest holding `created_at = 2026-07-03T06:50:48.772086`
- Reconfirmed downstream summaries stayed aligned:
  - holdings count `4`
  - portfolio holding count `4`
  - dashboard portfolio holding count `4`
  - total market value `2283500.00`
- Added:
  - `docs/PRICE_REFRESH_RECALCULATION_LINK_REPORT.md`
  - `docs/CODEX_TASK_2.16_REPORT.md`

## Verification result

| Item | Result |
|---|---|
| `POST /api/prices/collect/krx/daily` | 200 |
| `POST /api/prices/collect/krx/range` | 200 |
| `POST /api/jobs/4/run` | 200 |
| `GET /api/holdings` | 200 |
| `GET /api/holdings/summary` | 200 |
| `GET /api/portfolio/summary` | 200 |
| `GET /api/dashboard/summary` | 200 |
| `python -m compileall app` | passed |

## Current validated operation state

- automatic holdings recalculation after KRX non-dry-run collect: enabled
- verified paths:
  - daily API
  - range API
  - scheduled job manual run
- holdings, portfolio, dashboard summaries remained aligned after each path

## Confirmation-needed items

- Item: automatic chaining currently recalculates all holdings after every non-dry-run price collect
- Reason: this is the smallest safe change within current MVP structure
- Recommendation: keep this behavior unless performance tuning becomes necessary later
- Current implementation status: linked and verified

## Next step suggestions

- Use the linked path for normal live price refresh operations
- If later needed, optimize recalculation scope by affected pool or touched stock set as a separate task
