# KRX RANGE COLLECTION REPORT

## 1. 작업 개요

- 작업 문서: `docs/CODEX_TASK_1.9.md`
- 목표: 기존 KRX 일별 수집 로직을 재사용해 날짜 범위 수집 API를 추가하고, 중복 없는 upsert와 최신 가격 보호 조건을 보완한다.
- 신규 테이블/마이그레이션: 없음

## 2. 구현 내용

- `POST /api/prices/collect/krx/range` API 추가
- `date_from ~ date_to` 범위 검증 및 최대 220일 제한 추가
- 날짜별 수집 결과 응답 구조 추가
- 기존 일별 수집 흐름을 `_collect_for_date()`로 공통화
- `stocks.current_price`, `change_rate`, `market_cap`이 더 최신 일자보다 과거 일자로 덮이지 않도록 보호
- 날짜 단위 commit 처리로 장기간 수집 시 트랜잭션 범위를 축소
- SQLite write lock 또는 로그 저장 실패가 수집 전체를 즉시 중단시키지 않도록 예외 처리 보강
- SQLite upsert 경로를 chunk 단위로 처리하도록 보완

## 3. 수정 파일

- `backend/app/domains/prices/router.py`
- `backend/app/domains/prices/schemas.py`
- `backend/app/domains/prices/repository.py`
- `backend/app/domains/prices/service.py`

## 4. 검증 결과

- `python -m compileall app`: 성공
- `npm run build`: 성공
- live DB summary 확인:
  - `total_price_rows=352427`
  - `latest_price_date=2025-06-24`
  - `duplicate_groups=0`
- live DB 짧은 실제 적재 검증:
  - 기간: `20250623 ~ 20250624`
  - 결과: `fetched_count=5514`, `inserted_count=0`, `updated_count=5514`, `stock_created_count=0`, `error_count=0`
  - 날짜별 결과:
    - `20250623`: fetched 2757, inserted 0, updated 2757
    - `20250624`: fetched 2757, inserted 0, updated 2757
- 모의 KRX 검증:
  - 첫 수집: inserted 2, updated 0, skipped_empty 1
  - 동일 기간 재수집: inserted 0, updated 2
  - 과거 일자 재수집: historical row는 update되지만 `stocks.current_price`는 최신 일자 값 유지 확인
- 실제 KRX dry-run 검증:
  - 기간: `20241216 ~ 20241218`
  - 결과: `requested_date_count=3`, `fetched_count=8218`, `error_count=0`

## 5. 미완료 항목

- 전체 장기간 재수집의 최종 응답 시간은 여전히 길 수 있음
- 운영 기준으로는 장기간 범위 적재를 백그라운드 job 또는 날짜 분할 실행 방식으로 다루는 편이 안전함

## 6. 확인 필요 항목

- 항목: 장기간 range 재수집 실행 방식
- 관련 문서: `docs/CODEX_TASK_1.9.md`
- 애매한 이유: 짧은 실제 적재 검증은 통과했지만 장기간 전체 재수집은 처리 시간이 길다
- 가능한 선택지: 날짜 분할 실행, 백그라운드 job 실행, 운영 시간대 분산 실행
- 추천안: 운영에서는 짧은 기간 단위로 분할 실행하거나 scheduled job으로 처리
- 현재 구현 여부: 짧은 live DB 실적재 검증 완료
