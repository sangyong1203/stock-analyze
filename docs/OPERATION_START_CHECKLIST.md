# OPERATION START CHECKLIST

## 1. Start-of-day check

- Confirm `backend/stock_analyze.db` exists and the latest backup file is present in `backend/backups/`
- Confirm backend health:
  - `GET /health`
- Confirm Google OAuth readiness:
  - `GET /api/auth/status`

## 2. Data freshness check

- Check price freshness:
  - `GET /api/prices/summary`
- Do not rely on dashboard, portfolio, or alerts if `latest_price_date` is not the current trading date
- Check news freshness:
  - `GET /api/news/summary`
  - `GET /api/news/gpt/status`
- Do not rely on news alert candidates if market/news collection has not run for the day

## 3. Collection and recalculation check

- Confirm recent scheduled job results:
  - `GET /api/jobs/summary`
- If needed, rerun:
  - KRX daily price collection
  - news collection
  - GPT summary/filter
  - news alert candidate recalculation
- Recheck:
  - `/api/holdings/summary`
  - `/api/portfolio/summary`

## 4. Alert readiness check

- Check price alerts summary:
  - `GET /api/price-alerts/summary`
- Check alert settings:
  - `GET /api/settings/alert-settings`
- Do not run real send operations unless today’s data refresh is complete
- Do not perform Gmail send tests during routine verification

## 5. UI check

- Open and verify:
  - `/dashboard`
  - `/portfolio`
  - `/alerts`
  - `/news`
  - `/settings`
- If a protected route redirects to `/login`, complete Google OAuth login first

## 6. Backup rule

- Create a fresh backup before any major manual operation:
  - initial portfolio input
  - bulk price collection
  - bulk alert cleanup
  - important settings changes

## 7. Stop conditions

- Stop operation if price data is stale
- Stop operation if news collection is stale
- Stop operation if holdings and portfolio summaries are inconsistent
- Stop operation if repeated alert sends or failed histories appear unexpectedly
