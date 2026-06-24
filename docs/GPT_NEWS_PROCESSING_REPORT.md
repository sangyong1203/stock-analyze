# GPT NEWS PROCESSING REPORT

## 1. 작업 개요

- 작업 목표: 네이버 금융 실제 운영 수집 parser 검증/보정, GPT 요약 대상 산출, GPT 요약/재필터링 job API와 뉴스 화면 연결
- 기준 문서: AGENTS.md, INVESTMENT_SYSTEM_PLAN_v1.2.md, MVP_DB_SCHEMA_v1.2.md, DEVELOPMENT_REPORT.md, COLLECTION_TARGET_REPORT.md, NEWS_COLLECTION_REPORT.md
- DB 변경: 신규 테이블 없음, 기존 `news` 테이블의 GPT 관련 필드 사용

## 2. 구현한 API

| Method | Path | 설명 |
| ------ | ---- | ---- |
| GET | `/api/news/gpt/targets` | GPT 요약/필터 처리 대상 상태 집계 |
| GET | `/api/news/gpt/status` | GPT 처리 결과 통계 |
| POST | `/api/news/gpt/summary/run` | GPT mini 요약 job 실행 또는 dry-run |
| POST | `/api/news/gpt/filter/run` | GPT-5 계열 재필터링 job 실행 또는 dry-run |
| GET | `/api/news/gpt/review` | GPT 결과 검수 목록 조회 |
| PATCH | `/api/news/gpt/review/{news_id}` | GPT 필터 결과/사유/알림 후보/필터 상태 수동 보정 |

## 3. GPT 요약 대상 산출 기준

다음 중 하나 이상이면 `is_gpt_summary_target = true`, `gpt_summary_status = pending`으로 설정한다.

- `importance_score >= 6`
- `duplicate_count >= 3`
- `source_count >= 3`
- `event_type`이 earnings, disclosure, contract, supply_contract, rights_issue, bonus_issue, buyback, dividend, capacity_expansion, mna, legal_risk, technology 중 하나
- `is_alert_target = true`

대상이 아니면 `gpt_summary_status = skipped`로 둔다.

## 4. GPT 요약 구조

- 외부 client: `backend/app/external/openai/client.py`
- 환경변수: `OPENAI_API_KEY`, `OPENAI_NEWS_SUMMARY_MODEL`
- dry-run: 실제 OpenAI 호출 없이 대상 목록 반환
- 실행: API key와 모델명이 있을 때 OpenAI Responses API 호출
- 성공 저장 필드: `gpt_summary`, `gpt_summary_model`, `gpt_summary_status = done`, `gpt_summary_at`
- 실패 저장 필드: `gpt_summary_status = failed`

## 5. GPT 재필터링 구조

- 외부 client: `backend/app/external/openai/client.py`
- 환경변수: `OPENAI_API_KEY`, `OPENAI_NEWS_FILTER_MODEL`
- 대상: `gpt_summary_status = done`이거나 `content_preview/original_summary`가 있는 뉴스 중 `gpt_filter_result`가 비어 있는 항목
- 분류값: `important`, `price_impact`, `unnecessary`
- 성공 저장 필드: `gpt_filter_result`, `gpt_filter_reason`, `gpt_filter_model`, `gpt_filter_at`
- 실패 저장 필드: `gpt_filter_result = failed`, `gpt_filter_reason`

## 6. Frontend 연결 결과

- GPT 처리 KPI 표시: 요약 완료, 필터 완료, 중요/영향
- GPT 요약 대상 필터, 요약 상태 필터, GPT 필터 결과 필터 추가
- GPT 요약 dry-run/실행 버튼 추가
- GPT 재필터 dry-run/실행 버튼 추가
- 목록 컬럼에 GPT 대상 여부, GPT 요약 상태, GPT 필터 결과 표시
- 상세 drawer에 GPT 요약, 모델, 처리 시간, 필터 결과, 필터 사유, 필터 모델, 필터 시간 표시

## 7. 테스트 결과

- 실제 네이버 금융 수집: `/api/news/collect/market` pages 1, max_items 10 성공
- parser 추출: 실제 HTML에서 articleSubject/articleSummary 기반 제목, URL, 언론사, 발행시각, preview 추출 확인
- news 저장: 신규 뉴스 row 생성 확인
- 중복 재수집: 동일 페이지 재수집 시 duplicate_count 증가 확인
- news_stock_links: 수집 대상 종목 매칭 링크 생성 확인
- `/api/news/gpt/targets`: 200 응답
- `/api/news/gpt/status`: 200 응답
- summary dry-run: 200 응답
- filter dry-run: 200 응답
- API key 없음: dry_run=false 요청 시 `OPENAI_API_KEY is not configured` 400 응답
- OpenAI 환경변수 설정 후 실제 요약 실행: `OPENAI_API_KEY`, `OPENAI_NEWS_SUMMARY_MODEL`, `OPENAI_NEWS_FILTER_MODEL` 로드 확인, summary limit 1 성공
- 실제 요약 저장 확인: `gpt_summary`, `gpt_summary_model = gpt-5.4-mini`, `gpt_summary_status = done`, `gpt_summary_at` 저장
- 실제 재필터 실행: filter limit 1 요청은 OpenAI API quota 부족으로 실패했고 `gpt_filter_result = failed`, `gpt_filter_reason`에 `insufficient_quota` 오류 저장
- GPT 검수 API: `/api/news/gpt/review` 200 응답, PATCH 수동 보정 200 응답
- Frontend build: `npm run build` 성공
- Regression: `/health`, `/api/auth/status`, `/api/settings`, `/api/stocks`, `/api/collection/stocks/summary`, `/api/news`, `/api/news/summary` 200 응답

## 8. 확인 필요 항목

- 항목: OpenAI quota/billing
- 이유: API key와 모델명은 정상 로드되고 요약 호출은 성공했지만, 재필터 호출에서 `insufficient_quota` 오류가 발생했다.
- 제안: OpenAI 프로젝트 billing/quota를 확인한 뒤 filter limit 1부터 재실행한다.

- 항목: GPT 필터 결과 품질 기준
- 이유: 재필터링 분류값 구조는 구현했지만 운영 품질 기준은 실제 결과를 보고 보정해야 한다.
- 제안: 초기 20건 수동 검토 후 prompt와 분류 기준을 조정한다.

## 9. 다음 단계 제안

- OpenAI quota/billing 확인 후 GPT 재필터링 limit 1 재검증
- GPT 요약 결과 5건 확장 검증
- GPT 재필터링 결과 수동 검수 및 prompt 보정
- 뉴스 알림 후보 발송 구조 구현
