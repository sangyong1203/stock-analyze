# NEWS ALERT CANDIDATE REPORT

## 1. 작업 개요

- 작업 목표: GPT 결과 검수 API/UI와 Gmail 발송 전 뉴스 알림 후보 산출 구조 구현
- 기준 문서: AGENTS.md, INVESTMENT_SYSTEM_PLAN_v1.2.md, MVP_DB_SCHEMA_v1.2.md, DEVELOPMENT_REPORT.md, GPT_NEWS_PROCESSING_REPORT.md, NEWS_COLLECTION_REPORT.md
- DB 변경: 신규 테이블 없음, 기존 `news`, `alert_settings`, `news_stock_links`, `stocks` 등 MVP 테이블 사용
- Gmail 발송: 이번 범위에서는 구현하지 않음

## 2. 구현한 API

| Method | Path | 설명 |
| ------ | ---- | ---- |
| GET | `/api/news/gpt/review` | GPT 결과 검수 목록 조회 |
| PATCH | `/api/news/gpt/review/{news_id}` | GPT 필터 결과, 사유, 알림 후보 여부, 필터 상태 수동 보정 |
| POST | `/api/news/alerts/candidates/recalculate` | `alert_settings` 기준 뉴스 알림 후보 재계산 |
| GET | `/api/news/alerts/candidates` | 뉴스 알림 후보 목록 조회 |
| GET | `/api/news/alerts/summary` | 뉴스 알림 후보 요약 통계 |

## 3. 알림 후보 산출 기준

다음 조건 중 하나 이상이면 `news.is_alert_target = true`로 갱신한다.

- `importance_score >= alert_settings.min_importance_score`
- `duplicate_count >= alert_settings.min_duplicate_count`
- `source_count >= alert_settings.min_source_count`
- `gpt_filter_result in ["important", "price_impact"]`
- `event_type in alert_settings.event_types_json`
- 보유종목, 관심종목, 가격 알림 설정 종목 관련 뉴스

`alert_settings.enabled` 또는 `alert_settings.news_alert_enabled`가 꺼져 있으면 후보 재계산은 수행하지 않는다.

## 4. GPT 검수 기능

- 검수 목록 필터: `gpt_summary_status`, `gpt_filter_result`, `min_importance_score`, `stock_code`, `keyword`, `published_from`, `published_to`
- 수동 보정 필드: `gpt_filter_result`, `gpt_filter_reason`, `is_alert_target`, `filter_status`
- 별도 검수 이력 테이블은 만들지 않음
- `gpt_filter_result` 허용값: `important`, `price_impact`, `unnecessary`, `failed`

## 5. Frontend 연결 결과

- 기존 뉴스 화면에 GPT 검수 목록 섹션 추가
- 상세 drawer에 GPT 결과 수동 보정 form 추가
- `is_alert_target` 수동 체크/해제 기능 추가
- `filter_status` 수동 변경 기능 추가
- 알림 후보 재계산 버튼 추가
- 알림 후보 KPI와 후보 목록 테이블 추가
- 기존 검색/종목/중요도/GPT 필터 조건을 검수 목록과 알림 후보 목록에도 공유

## 6. 테스트 결과

- `/api/news/gpt/targets`: 200 응답
- `/api/news/gpt/status`: 200 응답
- `/api/news/gpt/summary/run` dry_run=true: 200 응답
- `/api/news/gpt/filter/run` dry_run=true: 200 응답
- API key 없음 dry_run=false: 400 응답, `OPENAI_API_KEY` 오류 확인
- `/api/news/gpt/review`: 200 응답, 14건 조회
- `/api/news/gpt/review/{news_id}` PATCH: 200 응답
- `/api/news/alerts/candidates/recalculate`: 200 응답, processed 14, alert_target 2
- `/api/news/alerts/candidates`: 200 응답, 2건 조회
- `/api/news/alerts/summary`: 200 응답
- Frontend build: `npm run build` 성공
- Regression: `/health`, `/api/auth/status`, `/api/settings`, `/api/stocks`, `/api/collection/stocks/summary`, `/api/news`, `/api/news/summary` 200 응답

## 7. 확인 필요 항목

- 항목: OpenAI 실제 호출 검증
- 이유: 현재 환경에 `OPENAI_API_KEY`, `OPENAI_NEWS_SUMMARY_MODEL`, `OPENAI_NEWS_FILTER_MODEL`이 설정되어 있지 않다.
- 제안: 환경변수 설정 후 summary/filter 각각 limit 5로 실제 호출 검증

- 항목: Gmail SMTP 발송 구조
- 이유: 이번 단계는 후보 산출까지만 구현하며 실제 이메일 발송은 포함하지 않는다.
- 제안: 다음 단계에서 `alert_histories` 생성과 Gmail SMTP 발송을 구현

- 항목: 알림 후보 기준 튜닝
- 이유: 현재 기준은 문서 기준의 1차 산출이며 실제 사용 중 과다/과소 알림 여부를 확인해야 한다.
- 제안: 후보 목록을 검수한 뒤 `alert_settings` 기준값과 event type 목록을 조정

## 8. 다음 단계 제안

- OpenAI 환경변수 설정 후 GPT 실제 요약/재필터링 소량 검증
- 알림 후보 기준 수동 검수 및 threshold 조정
- Gmail SMTP 발송 및 `alert_histories` 기록 구현
