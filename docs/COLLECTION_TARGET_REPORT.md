# COLLECTION TARGET REPORT

## 1. 작업 개요

KODEX 200 / KODEX 코스닥150 구성종목 import 구조, 수집 종목 관리 API, 최종 수집 대상 재계산 로직, 수집 종목 관리 화면 API 연결을 구현했다. 이후 실제 KODEX XLS 파일을 import해 구조를 검증했다.

## 2. 구현한 API

```text
POST /api/collection/index-constituents/import
GET  /api/collection/index-constituents
GET  /api/collection/index-constituents/summary

GET    /api/collection/stocks
GET    /api/collection/stocks/summary
PATCH  /api/collection/stocks/{stock_id}
POST   /api/collection/stocks/{stock_id}/include
POST   /api/collection/stocks/{stock_id}/exclude
POST   /api/collection/stocks/recalculate

GET    /api/collection/rules
POST   /api/collection/rules
PATCH  /api/collection/rules/{rule_id}
DELETE /api/collection/rules/{rule_id}
```

## 3. 구현한 Frontend 기능

- 수집 종목 목록 조회
- 키워드 검색
- 시장 필터
- 수집 여부 필터
- 우선순위 필터
- 수집 사유 필터
- 수동 포함 버튼
- 수동 제외 버튼
- 수집 설정 수정
- 최종 수집 대상 재계산 버튼
- 요약 KPI 표시
- 수집 조건 규칙 목록 및 활성화 토글

## 4. 수집 대상 산출 우선순위

재계산 우선순위는 기준 문서와 동일하게 적용했다.

```text
수동 제외 > 수동 포함 > 보유종목 > 관심종목 > 알림 설정 종목 > 조건 규칙
```

`collect_reason`은 다음 값 중 우선순위가 높은 하나를 저장한다.

```text
manual_exclude
manual_include
holding
favorite
alert
index_rule
market_cap_rule
```

## 5. 테스트 결과

| 항목 | 결과 | 비고 |
|---|---:|---|
| KODEX XLS import | O | `data/KODEX_200.xls` 200건, `data/KODEX_KOSDAQ_150.xls` 150건 |
| KODEX header row detection | O | 첫 줄 제목, 둘째 줄 헤더 형식 인식 |
| KODEX duplicate prevention | O | 재import 후 total/active 350건 유지 |
| index_constituents 목록 조회 | O | 200 응답 |
| index_constituents summary 조회 | O | total 350, active 350, KODEX 200 200, KODEX 코스닥150 150 |
| collection stocks 목록 조회 | O | 200 응답 |
| collection stocks summary 조회 | O | collect_enabled 350 |
| manual include | O | 200 응답 |
| manual exclude | O | 200 응답 |
| collection recalculate | O | 200 응답 |
| collection rules CRUD | O | 생성/수정/삭제 성공 |
| Frontend build | O | `npm run build` 성공 |
| Regression | O | `/health`, auth, settings, stocks API 정상 |

## 6. 확인 필요 항목

- 항목: KODEX 파일 갱신 주기
- 이유: 현재 검증은 제공된 2026-06-24 로컬 XLS 파일 기준이다.
- 제안: 실제 운영에서는 새 파일을 받을 때 동일 스크립트로 import하고 effective_date를 갱신한다.

- 항목: 조건 규칙 UI의 생성/삭제 범위
- 이유: 이번 화면은 목록과 활성화 토글 중심으로 구현했다.
- 제안: 실제 수집 조건 운영 방식 확정 후 규칙 생성/편집 UI를 확장한다.

## 7. 다음 단계 제안

- KODEX 파일 갱신 운영 방식 확정
- 네이버 금융 실제 운영 수집 실행 및 parser 보정
- GPT 요약/재필터링 job 구현

## 8. 실제 import 실행 명령

```bash
cd backend
python seeds/import_index_constituents.py --file ..\data\KODEX_200.xls --index-code KODEX_200 --index-name "KODEX 200" --effective-date 2026-06-24 --source kodex_xls
python seeds/import_index_constituents.py --file ..\data\KODEX_KOSDAQ_150.xls --index-code KODEX_KOSDAQ_150 --index-name "KODEX 코스닥150" --effective-date 2026-06-24 --source kodex_xls
```
