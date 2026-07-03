# CODEX PROGRESS

## Current phase

- Phase: initial portfolio current-price validation
- Task document: `docs/CODEX_TASK_2.5.md`
- Status: latest price validation completed, KRX daily refresh completed, holdings recalculation completed, reporting in progress completed

## Completed major work

- Reviewed immediate task context documents only:
  - `docs/DEVELOPMENT_REPORT.md`
  - `docs/NON_ETF_INITIAL_PORTFOLIO_INPUT_REPORT.md`
- Verified current initial portfolio scope remains the same 4 non-ETF holdings:
  - `006400`
  - `034020`
  - `028050`
  - `035420`
- Confirmed holdings calculation basis:
  - `holdings.current_price` is recalculated from `stocks.current_price`
  - `market_value` and `unrealized_profit_loss` are derived from that price basis
- Verified pre-refresh price data state:
  - `/api/prices/summary.latest_price_date = 2025-06-24`
  - held stocks also pointed to `2025-06-24` latest `stock_prices` rows
- Tested KRX daily collection with dry-run:
  - `2025-06-25`: fetched successfully
  - `2025-06-30`: fetched successfully
  - `2025-07-03`: fetched successfully
  - `2026-07-03`: fetched `0`
- Confirmed the latest practical KRX trade date for this validation run is `2025-07-03`
- Executed existing KRX daily collection for `2025-07-03`
  - fetched `2758`
  - inserted `2758`
  - updated `0`
  - stock created `1`
- Re-ran holdings recalculation after the price refresh completed
- Verified final post-refresh state by API and DB:
  - `/api/prices/summary.latest_price_date = 2025-07-03`
  - quantities unchanged
  - average prices unchanged
  - total cost basis unchanged at `5,108,090`
  - holdings current prices aligned with latest `stock_prices.close`
  - portfolio summary totals aligned with holdings totals
- Added `docs/INITIAL_PORTFOLIO_PRICE_VALIDATION_REPORT.md`
- Added `docs/CODEX_TASK_2.5_REPORT.md`

## Verification result

| Item | Result |
|---|---|
| `python -m compileall app` | success |
| `npm run build` | success |
| `/api/prices/summary` | 200 |
| `/api/holdings` | 200 |
| `/api/holdings/summary` | 200 |
| `/api/portfolio/summary` | 200 |
| `/api/dashboard/summary` | 200 |
| KRX dry-run `2025-07-03` | success |
| KRX actual collect `2025-07-03` | success |
| holdings recalculate after collect | success |

## Current validated data state

- Latest price date:
  - `2025-07-03`
- Held stocks:
  - `006400` quantity `5`, average price `596970`, current price `185300`, market value `926500`
  - `034020` quantity `10`, average price `105215`, current price `61900`, market value `619000`
  - `028050` quantity `10`, average price `55809`, current price `23200`, market value `232000`
  - `035420` quantity `2`, average price `256500`, current price `253000`, market value `506000`
- Holdings summary:
  - `holding_count = 4`
  - `total_market_value = 2283500.00`
  - `total_unrealized_profit_loss = -2824590.00`
- Portfolio summary:
  - `total_invested_amount = 5108090.00`
  - `total_market_value = 2283500.00`
  - `total_unrealized_profit_loss = -2824590.00`
  - `holding_count = 4`

## Confirmation-needed items

- Item: browser page verification remained partial
- Reason: even on the dev server, the in-app browser showed `Failed to fetch`, so rendered KPI values could not be trusted from UI inspection
- Recommendation: if browser-level QA is still required, re-run in a browser/runtime context that can fetch the backend API without the current failure
- Current implementation status: API and DB verification completed, browser verification partial

## Next step suggestions

- Use the refreshed `2025-07-03` price basis as the current operational baseline
- If the next task depends on UI QA, resolve the frontend browser fetch failure first or test from the user's normal local browser session
