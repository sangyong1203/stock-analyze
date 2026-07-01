# MVP INTEGRATION CHECK REPORT

## 1. Work overview

- Verification target: current MVP implementation after `CODEX_TASK_1.15`
- This task focused on integration verification and issue cleanup only
- No feature expansion, schema change, or migration work was performed

## 2. Backend API verification result

- Core regression APIs returned HTTP 200 in the current live DB environment
- Verified groups:
  - auth and health
  - settings and jobs
  - stocks and collection
  - prices and charts
  - news, GPT status, and alert dry-run endpoints
  - funds, trades, holdings, and portfolio
  - memos, tags, and dashboard

Key summary values:

- `jobs.total_count`: `8`
- `jobs.failed_count`: `0`
- `prices.total_price_rows`: `352427`
- `prices.latest_price_date`: `2025-06-24`
- `prices.latest_updated_stocks_count`: `2757`
- `news.total_news_count`: `18`
- `news.alert_target_count`: `2`
- `price_alerts.total_count`: `0`

## 3. Frontend page verification result

- Route entry checks succeeded for:
  - `/dashboard`
  - `/stocks`
  - `/collection`
  - `/news`
  - `/portfolio`
  - `/trades`
  - `/alerts`
  - `/charts`
  - `/memos`
  - `/settings`
- `npm run build` passed
- This report treats frontend verification as integration-level validation, not pixel-level UI review

## 4. DB verification result

- `python -m alembic current`: `20260624_0002 (head)`
- MVP tables present: `27 / 27`
- Extra tables added: `0`
- `stock_prices` duplicate groups on `stock_id + date + timeframe`: `0`
- `price_alerts` rows: `0`
- `alert_histories` rows: `2`
- `trades` rows: `0`
- `holdings` rows: `0`
- `fund_transactions` rows: `0`
- `tag_links` orphan rows: `0`
- `trade_news_links` orphan rows: `0`

## 5. Job runner verification result

- Jobs endpoints are reachable and summary data is populated
- Current summary shows `8` supported jobs and `0` failed jobs
- Recent run history confirms the following jobs completed successfully in the current environment:
  - `krx_price_daily`
  - `naver_news_collect`
  - `gpt_news_summary`
  - `news_alert_candidate`
  - `price_alert_evaluate`
- This task did not add new runner behavior and did not force additional Gmail live-send scenarios

## 6. Confirmation-needed items

- A browser-backed visual inspection was not available in this Codex session
- Some Korean text had previously appeared mojibake in tool output, but the current DB-side quick checks did not prove storage corruption
- Holdings, trades, and funds are currently empty in the live DB, so this task verified endpoint integrity rather than fresh transactional recalculation flows

## 7. MVP completion assessment

- MVP integration remains internally consistent within the current verification scope
- No schema drift was found
- No duplicate stock price rows were found for the enforced key grouping
- No orphan link integrity issue was found
- Build and compile checks passed

## 8. Next step suggestion

- Run a short manual browser sanity pass if UI-level confidence is needed before release
- Reproduce any suspected encoding issue from the actual UI or ingestion path before attempting data cleanup
