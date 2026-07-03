# PRICE REFRESH OPERATION ROUTINE

## Purpose

This routine documents the verified operational order for reflecting fresh KRX prices into holdings, portfolio, dashboard, and price-alert dry-run.

## Operation order

1. KRX price collect execution order

- Run:
  - `POST /api/prices/collect/krx/daily`
  - or `POST /api/prices/collect/krx/range`
- In normal verification, use `dry_run=true` first.

2. Collect completion check API

- Check:
  - `GET /api/prices/summary`
- Confirm:
  - `latest_price_date`
  - `latest_updated_stocks_count`
  - no unexpected error in collect result

3. Holdings recalculate execution order

- Run:
  - `POST /api/holdings/recalculate`
- Reason:
  - KRX collect updates `stock.current_price`
  - holdings aggregate fields such as `current_price`, `market_value`, and `unrealized_profit_loss` are refreshed by holdings recalculation

4. Portfolio/dashboard check API

- Check:
  - `GET /api/holdings`
  - `GET /api/holdings/summary`
  - `GET /api/portfolio/summary`
  - `GET /api/dashboard/summary`
- Confirm:
  - holdings current prices match latest stock price rows
  - total market value aligns across holdings, portfolio, and dashboard

5. Price alert dry-run execution order

- Run:
  - `POST /api/price-alerts/evaluate/dry-run`
- Use this after holdings reflection and portfolio/dashboard review.
- Do not execute real Gmail send as part of routine verification.

6. Failure-time check items

- Check whether `GET /api/prices/summary` latest date did not advance as expected
- Check collect API result `error_count` and `errors`
- Check whether holdings were recalculated after price collection
- Check whether holdings `current_price` differs from latest `stock_prices` close row
- Check whether portfolio/dashboard still show stale market values after price refresh
- Check whether there are zero active price-alert rows when dry-run evaluates nothing
