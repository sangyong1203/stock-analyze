# CODEX_TASK_2.14 REPORT

## Summary

- Organized GPT filter failure handling for OpenAI quota `429` cases
- Restored failed filter rows to the existing filter-run retry queue
- Kept failed rows blocked from news alert sending

## Key result

- Failed filter row `news_id = 3` is now included again in `POST /api/news/gpt/filter/run` dry-run targets
- News alert dry-run remains:
  - `sendable_count = 0`

## Files

- Backend:
  - `backend/app/domains/news/repository.py`
- Documents:
  - `docs/CODEX_PROGRESS.md`
  - `docs/DEVELOPMENT_REPORT.md`
  - `docs/GPT_FILTER_FAILURE_POLICY_REPORT.md`

## Validation

- `GET /api/news/gpt/targets`: passed
- `GET /api/news/gpt/review?gpt_filter_result=failed`: passed
- `POST /api/news/gpt/filter/run` dry-run: passed
- `POST /api/news/alerts/send/dry-run`: passed
- `python -m compileall app`: passed
- `npm run build`: passed

## Completion

CODEX_TASK_2.14 GPT filter 실패 뉴스 재처리 정책 정리 완료했습니다.
실제 Gmail 발송은 수행하지 않았습니다.
`DEVELOPMENT_REPORT.md`를 확인해 주세요.
