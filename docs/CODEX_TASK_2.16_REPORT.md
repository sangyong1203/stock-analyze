# CODEX_TASK_2.16 REPORT

## Summary

- Verified that KRX price collection did not automatically trigger holdings recalculation before the fix
- Linked non-dry-run KRX collection to holdings recalculation with a minimal backend change
- Verified the link through daily API, range API, and scheduled job manual run

## Key result

- Holdings `created_at` advanced automatically after:
  - daily collect
  - range collect
  - job manual run
- Holdings, portfolio, and dashboard summaries remained aligned

## Files

- Backend:
  - `backend/app/domains/prices/service.py`
- Documents:
  - `docs/CODEX_PROGRESS.md`
  - `docs/DEVELOPMENT_REPORT.md`
  - `docs/PRICE_REFRESH_RECALCULATION_LINK_REPORT.md`

## Validation

- `POST /api/prices/collect/krx/daily`: passed
- `POST /api/prices/collect/krx/range`: passed
- `POST /api/jobs/4/run`: passed
- `GET /api/holdings/summary`: passed
- `GET /api/portfolio/summary`: passed
- `GET /api/dashboard/summary`: passed
- `python -m compileall app`: passed

## Completion

CODEX_TASK_2.16 가격 수집 후 holdings 자동 재계산 연결 검증 완료했습니다.
`DEVELOPMENT_REPORT.md`를 확인해 주세요.
