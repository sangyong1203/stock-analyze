# CODEX_TASK_1.16

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

CODEX_TASK_1.15 자동 수집 / scheduled_jobs 기반 실행 구조는 완료됐습니다.

이번 작업은 **MVP 통합 검증 / 오류 정리 / 문서 정리**입니다.

## 작업 목표

1. 전체 MVP 기능을 통합 검증한다.
2. 주요 API regression을 확인한다.
3. 주요 Frontend 화면 접근과 build를 확인한다.
4. DB 중복 / 무결성 / 기본 데이터 상태를 확인한다.
5. 남은 확인 필요 항목을 정리한다.
6. 실제 기능 추가는 하지 않는다.
7. 새 DB 테이블과 마이그레이션은 만들지 않는다.

## 작업 전 확인

직전 `DEVELOPMENT_REPORT.md`의 완료/미완료/확인 필요 항목만 확인한다.

기준 문서를 반복해서 다시 읽지 않는다.

이번 작업은 신규 개발이 아니라 **검증과 정리**가 목적이다.

## 검증 대상 기능

아래 기능들이 정상 연결되어 있는지 확인한다.

```text
1. 설정 / scheduled_jobs
2. 종목 / 수집 종목 관리
3. KRX 가격 수집 / 가격 조회
4. 차트 / 기술지표 / 기간 필터
5. 뉴스 수집
6. GPT 뉴스 요약 / 필터 dry-run
7. 뉴스 알림 후보 / Gmail 발송 dry-run
8. 가격 알림 CRUD / dry-run
9. 거래 기록 / 자금 / 보유 / 손익
10. 메모 / 태그 / 거래-뉴스 연결
11. 대시보드
12. job runner
```

## Backend 검증 항목

다음 API를 확인한다.

```text
/health
/api/auth/status

/api/settings
/api/jobs
/api/jobs/summary

/api/stocks
/api/collection/stocks/summary

/api/prices/summary
/api/prices/markets/KOSPI/latest?limit=3
/api/prices/markets/KOSDAQ/latest?limit=3
/api/charts/stocks/2/ohlcv?limit=130

/api/news
/api/news/summary
/api/news/gpt/targets
/api/news/gpt/status
/api/news/alerts/summary
/api/news/alerts/send/dry-run

/api/price-alerts
/api/price-alerts/summary
/api/price-alerts/evaluate/dry-run

/api/funds/summary
/api/trades
/api/holdings/summary
/api/portfolio/summary

/api/memos
/api/tags
/api/dashboard/summary
```

## Job runner 검증

`CODEX_TASK_1.15`에서 batch run이 성공했으므로, 이번에는 안전성만 확인한다.

```text
1. /api/jobs 목록 확인
2. /api/jobs/summary 확인
3. 발송성 job의 기본 실행이 실제 발송인지 dry-run인지 확인
4. news_alert_send, price_alert_evaluate가 batch run에서 불필요하게 중복 발송하지 않는지 확인
5. alert_histories에 불필요한 중복 기록이 없는지 확인
```

주의:

```text
- 이번 통합 검증에서 실제 Gmail 발송은 기본적으로 하지 않는다.
- 필요하면 dry-run만 실행한다.
- 실제 발송이 필요한 경우 limit 1로만 수행하고 문서에 명확히 기록한다.
```

## DB 검증 항목

기존 DB 기준으로 아래를 확인한다.

```text
1. alembic current 확인
2. MVP 27개 테이블 존재 확인
3. 신규 테이블이 추가되지 않았는지 확인
4. stock_prices 중복 확인
   - stock_id + date + timeframe 중복 그룹 0건
5. price_alerts / alert_histories 기본 조회 가능
6. trades / holdings / fund_transactions 정합성 기본 확인
7. tag_links / trade_news_links 연결 데이터 무결성 확인
8. 깨진 종목명 / 뉴스명 인코딩 현황을 확인 필요 항목으로 정리
```

## Frontend 검증 항목

다음 화면 접근과 기본 렌더링을 확인한다.

```text
/dashboard
/stocks
/collection
/news
/portfolio
/trades
/alerts
/charts
/memos
/settings
```

확인 항목:

```text
1. 화면 진입 가능
2. API 오류 없는지 확인
3. 빈 데이터 상태 정상 표시
4. 주요 버튼이 렌더링되는지 확인
5. npm run build 성공
```

## 문서 정리

다음 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 새 문서를 작성한다.

```text
docs/MVP_INTEGRATION_CHECK_REPORT.md
```

포함 내용:

```markdown
# MVP INTEGRATION CHECK REPORT

## 1. 작업 개요

## 2. Backend API 검증 결과

## 3. Frontend 화면 검증 결과

## 4. DB 검증 결과

## 5. Job runner 검증 결과

## 6. 남은 확인 필요 항목

## 7. MVP 완료 판단

## 8. 다음 단계 제안
```

## 남은 확인 필요 항목 정리 기준

아래 항목은 기능 개발과 분리해서 정리한다.

```text
- OpenAI quota / GPT filter 실제 성공 여부
- 종목명 / 뉴스명 인코딩 깨짐
- ECharts 재적용 여부
- 장기간 job의 background 실행 필요성
- stock page memo/tag UI 확장 여부
- 거래 당시 price_snapshot 자동 생성 여부
- trade_news_links 입력 UX 추가 보완 여부
```

## 완료 조건

```text
- Backend compile 성공
- Frontend build 성공
- 주요 API regression 성공
- 주요 화면 접근 성공
- DB 중복 / 무결성 기본 검증 성공
- job runner 안전성 확인
- DEVELOPMENT_REPORT.md 갱신
- MVP_INTEGRATION_CHECK_REPORT.md 작성
```

작업 완료 후 다음과 같이 보고하세요.

```text
MVP 통합 검증 및 오류 정리 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
