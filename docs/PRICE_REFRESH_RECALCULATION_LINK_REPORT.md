# PRICE REFRESH RECALCULATION LINK REPORT

## Scope

- Task: `docs/CODEX_TASK_2.16.md`
- Goal: verify whether KRX price collection automatically leads into holdings recalculation, and connect it if missing

## Result

- Before fix:
  - price collection updated `stock.current_price`
  - holdings recalculation was separate
- After fix:
  - non-dry-run daily collect triggers holdings recalculation
  - non-dry-run range collect triggers holdings recalculation
  - scheduled job manual run also inherits the same link

## Verified paths

1. Daily API

- `POST /api/prices/collect/krx/daily`
- latest holding `created_at` advanced after execution

2. Range API

- `POST /api/prices/collect/krx/range`
- latest holding `created_at` advanced after execution

3. Scheduled job manual run

- `POST /api/jobs/4/run`
- latest holding `created_at` advanced after execution

## Summary alignment

- `GET /api/holdings/summary`
- `GET /api/portfolio/summary`
- `GET /api/dashboard/summary`

All remained aligned after the automatic recalculation:

- holding count `4`
- total market value `2283500.00`

## Notes

- Dry-run behavior was not changed
- No schema change
- No migration
