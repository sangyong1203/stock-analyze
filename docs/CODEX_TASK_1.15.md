# CODEX_TASK_1.15

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

대시보드 / 투자 리포트 화면은 완료됐습니다.

이번 작업은 **자동 수집 / scheduled_jobs 기반 실행 구조 구현**입니다.

## 작업 목표

1. 기존 `scheduled_jobs` 테이블을 사용해 자동 실행 대상 job을 관리한다.
2. KRX 가격 수집, 뉴스 수집, GPT 처리, 알림 평가/발송을 job 단위로 실행한다.
3. 수동 실행 API와 job 상태 조회 API를 구현한다.
4. 실행 결과와 오류를 `system_logs` 또는 기존 job 필드에 기록한다.
5. Frontend에서 job 목록, 실행, 상태 확인을 할 수 있게 한다.
6. 새 DB 테이블과 마이그레이션은 만들지 않는다.

## 작업 전 확인

직전 `DEVELOPMENT_REPORT.md`의 완료/미완료/확인 필요 항목만 확인한다.

이번 작업에서 필요한 기존 구조만 확인한다.

```text
scheduled_jobs
system_logs
stock_prices
news_collect_jobs
news_collect_job_items
news
price_alerts
alert_histories
```

관련 도메인:

```text
backend/app/domains/prices/
backend/app/domains/news/
backend/app/domains/alerts/
backend/app/domains/settings/
backend/app/main.py
frontend/src/pages/main/settings/
frontend/src/pages/main/dashboard/
```

주의:

```text
- 기준 문서를 반복해서 다시 읽지 않는다.
- 새 DB 테이블을 만들지 않는다.
- 새 마이그레이션을 만들지 않는다.
- 실제 OS cron이나 외부 scheduler는 이번 작업 범위에서 제외한다.
- MVP에서는 “수동 실행 가능한 scheduled job runner”를 우선 구현한다.
```

## Backend 작업 항목

권장 도메인:

```text
backend/app/domains/jobs/
```

필요 API:

```text
GET  /api/jobs
GET  /api/jobs/{job_id}
POST /api/jobs/{job_id}/run
POST /api/jobs/run
GET  /api/jobs/summary
```

가능하면 job 생성/수정은 기존 settings 구조와 맞춘다.
이미 scheduled_jobs seed가 있으면 우선 그 값을 사용한다.

## 지원할 job type

최소 지원:

```text
krx_price_daily
krx_price_range
naver_news_collect
gpt_news_summary
gpt_news_filter
news_alert_candidate
news_alert_send
price_alert_evaluate
```

## job 실행 기준

### 1. KRX 단일 일자 가격 수집

```text
job_type = krx_price_daily
```

동작:

```text
- 마지막 완료 영업일 또는 job config의 bas_date 사용
- /api/prices/collect/krx/daily 로직 재사용
- KOSPI / KOSDAQ 수집
```

### 2. KRX 기간 가격 수집

```text
job_type = krx_price_range
```

동작:

```text
- config의 date_from/date_to 사용
- 너무 긴 범위는 기존 220일 제한 유지
- 기존 range 수집 로직 재사용
```

### 3. 네이버 뉴스 수집

```text
job_type = naver_news_collect
```

동작:

```text
- 기존 뉴스 수집 로직 재사용
- 시장 뉴스 수집 우선
- 결과 job/item 기록 유지
```

### 4. GPT 뉴스 요약

```text
job_type = gpt_news_summary
```

동작:

```text
- 기존 GPT summary target 기준 재사용
- limit 설정 가능
- OpenAI quota 오류는 실패로 기록하고 전체 runner는 중단하지 않는다
```

### 5. GPT 뉴스 필터

```text
job_type = gpt_news_filter
```

동작:

```text
- 기존 GPT filter 로직 재사용
- insufficient_quota 발생 시 failed 기록
```

### 6. 뉴스 알림 후보 계산

```text
job_type = news_alert_candidate
```

동작:

```text
- 기존 news alert candidates recalculate 로직 재사용
```

### 7. 뉴스 알림 발송

```text
job_type = news_alert_send
```

동작:

```text
- 기존 Gmail 뉴스 알림 발송 로직 재사용
- 발송 제한 / 중복 방지 유지
```

### 8. 가격 알림 평가

```text
job_type = price_alert_evaluate
```

동작:

```text
- 기존 price-alert evaluate 로직 재사용
- 당일 중복 발송 방지 유지
```

## scheduled_jobs 처리 기준

기존 필드 안에서 아래 개념을 처리한다.

```text
name
job_type
enabled
schedule_type
config_json
last_run_at
last_status
last_message
next_run_at
created_at
updated_at
```

기존 모델 필드명이 다르면 기존 필드명에 맞춘다.

`config_json` 예시:

```json
{
  "markets": ["KOSPI", "KOSDAQ"],
  "limit": 10,
  "dry_run": false
}
```

필드가 부족하면 임의 추가하지 말고 `확인 필요 항목`에 기록한다.

## job 실행 결과

`POST /api/jobs/{job_id}/run` 응답 예시:

```json
{
  "job_id": 1,
  "job_type": "price_alert_evaluate",
  "status": "success",
  "started_at": "2026-07-01T09:00:00",
  "finished_at": "2026-07-01T09:00:05",
  "message": "sent 1, skipped 2",
  "result": {}
}
```

실패 시:

```json
{
  "status": "failed",
  "message": "OpenAI insufficient_quota",
  "result": {}
}
```

## Frontend 작업 항목

대상 후보:

```text
frontend/src/pages/main/settings/
frontend/src/pages/main/dashboard/
```

구현 항목:

```text
- 자동 작업 목록 표시
- enabled 상태 표시
- job type 표시
- last_run_at / last_status / last_message 표시
- 수동 실행 버튼
- 실행 결과 표시
- 실패 사유 표시
- loading / error / empty 상태 처리
```

가능하면 대시보드에 최근 job 상태 요약 카드도 추가한다.

## 검증 항목

Backend:

```text
- python -m compileall app 성공
- /api/jobs 200
- /api/jobs/summary 200
- krx_price_daily 수동 실행 또는 dry-run 성공
- naver_news_collect 수동 실행 성공
- news_alert_candidate 수동 실행 성공
- price_alert_evaluate dry-run 또는 실제 실행 성공
- OpenAI quota 오류가 발생해도 job failed로 기록되고 서버는 정상 유지
```

Frontend:

```text
- 설정 또는 job 화면에서 작업 목록 표시
- 수동 실행 버튼 동작
- 실행 결과 표시
- npm run build 성공
```

Regression:

```text
/health
/api/auth/status
/api/prices/summary
/api/dashboard/summary
/api/portfolio/summary
/api/price-alerts/summary
/api/news/alerts/send/dry-run
```

## 문서 갱신

작업 완료 후 다음 문서를 짧게 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 새 문서를 작성한다.

```text
docs/SCHEDULED_JOB_REPORT.md
```

포함 내용:

```markdown
# SCHEDULED JOB REPORT

## 1. 작업 개요

## 2. 구현한 API

## 3. 지원 job type

## 4. job 실행 방식

## 5. Frontend 연결 결과

## 6. 테스트 결과

## 7. 확인 필요 항목

## 8. 다음 단계 제안
```

## 완료 조건

```text
- scheduled_jobs 기반 job 목록 조회 구현
- job 수동 실행 API 구현
- KRX / 뉴스 / GPT / 알림 관련 job type 연결
- 실행 결과와 오류 기록
- Frontend job 관리 화면 연결
- Backend compile 성공
- Frontend build 성공
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 다음과 같이 보고하세요.

```text
자동 수집 / scheduled_jobs 기반 실행 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
