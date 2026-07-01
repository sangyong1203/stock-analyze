# MVP MANUAL QA REPORT

## 1. Work overview

- Verification target: current MVP after `CODEX_TASK_1.16`
- This task focused on manual QA intent, sample data flow validation, encoding checks, and cleanup verification
- No feature expansion, schema change, or migration work was performed

## 2. Screen QA result

Target routes:

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

Result:

- Route entry responses for all target pages returned HTTP 200
- Frontend HTML shell loaded correctly for all checked routes
- Browser runtime was not available in the current Codex session, so visual layout and real click-flow inspection were not automated here

## 3. Sample data flow verification result

- Created one test fund pool
- Created one deposit transaction
- Created one Samsung Electronics buy trade
- Verified holdings summary changed to one active holding
- Verified portfolio summary reflected cash decrease and market value increase
- Created one price alert and verified dry-run result
- Ran non-sending alert evaluate path and confirmed skipped alert history creation
- Created one trade memo
- Created one trade tag and linked it
- Created one trade-news link
- Verified dashboard reflected recent trade, memo, and alert history
- Removed all test data and verified summaries returned to baseline

## 4. Encoding check result

Checked surfaces:

- stock name
- news title
- news source
- alert history title and message
- dashboard recent news
- dashboard recent trade stock name
- alerts stock name

Result:

- All checked API-visible samples were readable Korean text where expected
- No replacement character `�` was found in the verified samples
- No encoding fix was applied because the issue was not reproduced in validated data paths

## 5. Found issues

- Browser runtime limitation:
  - no attached browser instance was available for actual visual QA in this session

## 6. Fixed issues

- None
- This task remained verification-only

## 7. Deferred items

- Visual layout, button interaction, and empty-state inspection should be repeated in a real browser if UI-level confidence is required
- If mojibake appears later in UI, investigate source ingestion, DB storage, API response encoding, and frontend rendering separately

## 8. Next step suggestion

- Run a short manual browser pass for dashboard, news, trades, alerts, and settings pages
- Keep future encoding work evidence-based and avoid mutating live data unless the issue is reproduced
