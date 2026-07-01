# CODEX_TASK_1.17

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

MVP 통합 검증은 완료됐습니다.

이번 작업은 **MVP 수동 QA / 데이터 정합성 / 인코딩 점검**입니다.

## 작업 목표

1. 주요 화면을 실제 브라우저 기준으로 육안 점검한다.
2. 한글 깨짐, 레이아웃 깨짐, API 오류, 빈 데이터 표시 문제를 확인한다.
3. 실제 샘플 데이터를 최소로 입력해 대시보드/거래/보유/알림 흐름을 확인한다.
4. 종목명/뉴스명 mojibake가 실제 UI에서 재현되는지 확인한다.
5. 새 기능 추가는 하지 않는다.
6. 새 테이블과 마이그레이션은 만들지 않는다.

## 작업 항목

다음 화면을 브라우저에서 직접 확인한다.

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

각 화면에서 확인할 것:

```text
1. 화면 진입 가능 여부
2. 주요 API 오류 여부
3. 로딩/빈 데이터/오류 상태 표시
4. 한글 텍스트 깨짐 여부
5. 버튼/폼/테이블 레이아웃 깨짐 여부
6. 실제 사용 흐름상 막히는 부분
```

## 샘플 데이터 QA

운영 데이터에 영향을 최소화하기 위해 테스트 데이터를 만들고 마지막에 정리한다.

확인 흐름:

```text
1. 테스트용 fund pool 생성
2. 입금 1건 등록
3. 삼성전자 매수 거래 1건 등록
4. holdings 재계산
5. portfolio summary와 dashboard 반영 확인
6. 가격 알림 1건 생성
7. price-alert dry-run 확인
8. 거래 메모 1건 생성
9. 거래 태그 1건 연결
10. 거래-뉴스 연결 1건 테스트
11. dashboard에 최근 거래/메모/알림 반영 확인
12. 테스트 데이터 정리
```

실제 Gmail 발송은 하지 않는다.
필요하면 dry-run만 사용한다.

## 인코딩 점검

다음 데이터에서 한글 깨짐 여부를 확인한다.

```text
1. stocks.name
2. news.title
3. news.source
4. alert_histories.title/message
5. dashboard recent_news
6. trades/portfolio 종목명 표시
7. alerts 종목명 표시
```

한글 깨짐이 있으면 바로 수정하지 말고 원인을 분리해서 기록한다.

```text
- KRX 응답 파싱 문제인지
- DB 저장 문제인지
- API 응답 인코딩 문제인지
- Frontend 렌더링 문제인지
```

## Backend 검증

```text
python -m compileall app
```

주요 API 확인:

```text
/health
/api/auth/status
/api/dashboard/summary
/api/stocks
/api/news
/api/prices/summary
/api/portfolio/summary
/api/price-alerts/summary
/api/jobs/summary
```

## Frontend 검증

```text
npm run build
```

브라우저에서 주요 화면 육안 확인 후 결과를 기록한다.

## 문서 갱신

작업 완료 후 다음 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 새 문서를 작성한다.

```text
docs/MVP_MANUAL_QA_REPORT.md
```

포함 내용:

```markdown
# MVP MANUAL QA REPORT

## 1. 작업 개요

## 2. 화면별 QA 결과

## 3. 샘플 데이터 흐름 검증 결과

## 4. 인코딩 점검 결과

## 5. 발견한 문제

## 6. 수정한 문제

## 7. 보류 항목

## 8. 다음 단계 제안
```

## 주의

- 기준 문서를 반복해서 다시 읽지 않는다.
- 새 기능을 추가하지 않는다.
- 새 DB 테이블을 만들지 않는다.
- 새 마이그레이션을 만들지 않는다.
- 테스트 데이터는 마지막에 정리한다.
- 실제 Gmail 발송은 하지 않는다.
- 이번 작업은 QA와 정리 중심이다.

작업 완료 후 다음과 같이 보고하세요.

```text
MVP 수동 QA / 데이터 정합성 / 인코딩 점검 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
