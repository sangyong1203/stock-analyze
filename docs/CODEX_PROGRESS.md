# CODEX PROGRESS

## Current phase

- Phase: memo / tag CRUD and trade-news link validation
- Task document: `docs/CODEX_TASK_1.13.md`
- Status: implementation and verification complete

## Completed major work

- Added memo CRUD API for `stock`, `trade`, `news`, and `general`
- Added tag CRUD API and `tag_links` link / unlink / list API
- Added trade-news link API on both trade and news views
- Added trade detail drawer support for memo, tag, and related news management
- Added news detail drawer support for related trade, memo, and tag management
- Added backend `tags` domain and router registration
- Fixed `DELETE /api/tags/link` route order issue found during verification
- Backend compile passed
- Frontend build passed

## Verification result

| Item | Result |
|---|---|
| `GET /api/memos` | success |
| `POST /api/memos` | success |
| `GET /api/memos/{memo_id}` | success |
| `PATCH /api/memos/{memo_id}` | success |
| `DELETE /api/memos/{memo_id}` | success |
| `GET /api/tags` | success |
| `POST /api/tags` | success |
| `PATCH /api/tags/{tag_id}` | success |
| `DELETE /api/tags/{tag_id}` | success |
| `POST /api/tags/link` | success |
| `DELETE /api/tags/link` | success |
| `GET /api/tags/links` | success |
| `GET /api/trades/{trade_id}/news` | success |
| `POST /api/trades/{trade_id}/news` | success |
| `DELETE /api/trades/{trade_id}/news/{news_id}` | success |
| `GET /api/news/{news_id}/trades` | success |
| `python -m compileall backend/app` | success |
| `npm run build` | success |
| Regression API | all 200 on verification run |

## Confirmation-needed items

- Item: stock page memo / tag UI was not expanded in this task
- Related document: `docs/CODEX_TASK_1.13.md`
- Reason: the task explicitly allowed stock page work to remain minimal if trade / news coverage was prioritized
- Possible options: add stock detail memo / tag UI later, or keep stock target handling API-only
- Recommendation: keep current scope and add stock page support only if the next task requires it
- Current implementation status: deferred

- Item: some existing stock / news names are still broken in DB encoding
- Related document: `docs/DEVELOPMENT_REPORT.md`
- Reason: verification data inherited mojibake from existing live DB rows
- Possible options: separate master-data cleanup, or keep current behavior until source data is normalized
- Recommendation: handle encoding cleanup as a separate maintenance task
- Current implementation status: deferred

## Next step suggestions

- Add stock detail memo / tag UI only if the next task needs stock-side workflow parity
- Separate existing DB text encoding cleanup from feature work
