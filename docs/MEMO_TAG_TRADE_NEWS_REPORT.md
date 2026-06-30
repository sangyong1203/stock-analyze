# MEMO TAG TRADE NEWS REPORT

## 1. Work overview

- Implemented memo CRUD, tag CRUD, `tag_links`, and `trade_news_links` handling
- Kept the work inside the confirmed MVP schema
- Did not add new tables or migrations

## 2. Implemented API

- `GET /api/memos`
- `POST /api/memos`
- `GET /api/memos/{memo_id}`
- `PATCH /api/memos/{memo_id}`
- `DELETE /api/memos/{memo_id}`
- `GET /api/tags`
- `POST /api/tags`
- `PATCH /api/tags/{tag_id}`
- `DELETE /api/tags/{tag_id}`
- `POST /api/tags/link`
- `DELETE /api/tags/link`
- `GET /api/tags/links`
- `GET /api/trades/{trade_id}/news`
- `POST /api/trades/{trade_id}/news`
- `DELETE /api/trades/{trade_id}/news/{news_id}`
- `GET /api/news/{news_id}/trades`

## 3. Memo structure

- Memo types supported: `stock`, `trade`, `news`, `general`
- Target validation is performed before persistence
- Trade and news page detail flows now consume the memo API directly

## 4. Tag structure

- Tag target types supported: `stock`, `trade`, `news`, `memo`
- Tag master data and target linking are separated
- `DELETE /api/tags/link` required a route order fix during verification

## 5. Trade-news link structure

- Link storage uses existing `trade_news_links`
- One trade can list linked news rows
- One news row can list linked trades
- Link and unlink operations are available from both page workflows

## 6. Frontend connection result

- Trades page:
  - memo create / update / delete
  - tag create / link / unlink
  - related news search / link / unlink
- News page:
  - related trade link / unlink
  - memo create / update / delete
  - tag create / link / unlink

## 7. Test result

- `python -m compileall backend/app`: success
- `npm run build`: success
- Verification ran on a copied live DB file
- Memo CRUD: success
- Tag CRUD: success
- Stock / trade / news tag link: success
- Trade-news link / unlink: success
- Regression APIs: all 200

## 8. Confirmation-needed items

- Some source rows still contain broken text encoding in existing DB data
- Stock page memo / tag UI was intentionally left out of this task

## 9. Next step suggestion

- Add stock page memo / tag UI only when stock-side workflow becomes required
- Run a separate existing-data normalization task if mojibake needs cleanup
