# CODEX PROGRESS

## Current phase

- Phase: MVP manual QA, sample data consistency check, and encoding verification
- Task document: `docs/CODEX_TASK_1.17.md`
- Status: verification, cleanup, and reporting complete

## Completed major work

- Attempted browser-based localhost QA through the available browser runtime path
- Confirmed no browser instance was attached in the current Codex session, so true visual automation could not proceed
- Re-checked backend health and major MVP APIs:
  - `/health`
  - `/api/auth/status`
  - `/api/dashboard/summary`
  - `/api/stocks`
  - `/api/news`
  - `/api/prices/summary`
  - `/api/portfolio/summary`
  - `/api/price-alerts/summary`
  - `/api/jobs/summary`
- Re-checked frontend route entry points for:
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
- Executed sample data QA flow on live DB:
  - created test fund pool
  - inserted deposit
  - inserted Samsung Electronics buy trade
  - verified holdings and portfolio summary update
  - created price alert
  - verified price-alert dry-run
  - executed non-sending evaluate path that recorded a skipped history
  - created trade memo
  - created trade tag and link
  - created trade-news link
  - verified dashboard recent trade, memo, and alert reflection
  - cleaned all test data
- Confirmed cleanup restored summary state back to the baseline
- Confirmed API-visible Korean text was readable in tested stock, news, alert, dashboard, trade, and alert surfaces
- Confirmed backend compile passed
- Confirmed frontend production build passed
- Added `docs/MVP_MANUAL_QA_REPORT.md`
- Added `docs/CODEX_TASK_1.17_REPORT.md`

## Verification result

| Item | Result |
|---|---|
| Browser runtime selection | no browser available in session |
| `python -m compileall app` | success |
| `npm run build` | success |
| Major regression APIs | all 200 |
| Frontend route entry checks | all 200 |
| Sample fund pool create | success |
| Sample deposit create | success |
| Sample buy trade create | success |
| Holdings summary after buy | `holding_count = 1` |
| Portfolio summary after buy | reflected |
| Price alert create | success |
| Price alert dry-run | success |
| Price alert evaluate without send | skipped history recorded |
| Trade memo create | success |
| Trade tag link create | success |
| Trade-news link create | success |
| Dashboard recent trade reflection | success |
| Dashboard recent memo reflection | success |
| Dashboard recent alert reflection | success |
| Test data cleanup | success |

## Confirmation-needed items

- Item: true browser-based visual inspection could not be completed in this session
- Related document: `docs/CODEX_TASK_1.17.md`
- Reason: browser runtime returned `No browser is available`
- Possible options: repeat manual UI pass later in a real browser, or accept the current route/API-level QA for this task
- Recommendation: treat this run as data-flow and integration QA, then perform a short human visual pass in VS Code or an external browser if visual confidence is required
- Current implementation status: no code change made for this limitation

- Item: sample encoding checks were clean on API and DB-visible paths, but frontend render-level mojibake still was not visually observed in a live browser
- Related document: `docs/CODEX_TASK_1.17.md`
- Reason: no browser instance was attached for final UI confirmation
- Possible options: re-open the app manually and confirm stocks/news/alerts/dashboard text rendering, or keep the current API-level conclusion
- Recommendation: keep as a follow-up visual confirmation item only if mojibake is later reproduced
- Current implementation status: no encoding fix applied because the issue was not reproduced in validated data paths

## Next step suggestions

- Run a short manual browser pass for dashboard, news, trades, alerts, and settings pages if UI-level release confidence is needed
- If mojibake is reproduced later, isolate source ingestion, DB storage, API response encoding, and frontend rendering before changing live data
