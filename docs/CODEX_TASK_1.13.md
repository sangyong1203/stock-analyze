# CODEX_TASK_1.13

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

가격 알림 조건과 발송 구조는 완료됐습니다.

이번 작업은 **거래-뉴스 연결 / 메모·태그 구조 구현**입니다.

## 작업 목표

1. 거래 기록에 매수/매도 사유 메모를 연결한다.
2. 거래와 관련 뉴스를 연결한다.
3. 종목, 거래, 뉴스에 태그를 연결한다.
4. 메모/태그 CRUD를 구현한다.
5. 거래 화면과 뉴스 화면에서 메모/태그/뉴스 연결을 사용할 수 있게 한다.
6. 기존 DB 테이블만 사용한다.
7. 새 테이블과 마이그레이션은 만들지 않는다.

## 작업 전 확인

직전 `DEVELOPMENT_REPORT.md`의 완료/미완료/확인 필요 항목만 확인한다.

이번 작업에서 필요한 기존 모델만 확인한다.

```text
memos
tags
tag_links
trade_news_links
trades
news
stocks
```

주의:

```text
- 기준 문서를 반복해서 다시 읽지 않는다.
- 새 DB 테이블을 만들지 않는다.
- 새 마이그레이션을 만들지 않는다.
- 기존 필드 안에서 구현한다.
- 필드가 부족하거나 애매하면 임의 추가하지 말고 확인 필요 항목에 기록한다.
```

## Backend 작업 항목

대상 후보:

```text
backend/app/domains/memos/
backend/app/domains/tags/
backend/app/domains/trades/
backend/app/domains/news/
backend/app/main.py
```

## 1. 메모 API

권장 API:

```text
GET    /api/memos
POST   /api/memos
GET    /api/memos/{memo_id}
PATCH  /api/memos/{memo_id}
DELETE /api/memos/{memo_id}
```

지원 대상:

```text
stock
trade
news
general
```

기능:

```text
- 메모 생성
- 메모 수정
- 메모 삭제
- 대상별 메모 조회
- 종목별 메모 조회
- 거래별 메모 조회
- 뉴스별 메모 조회
```

## 2. 태그 API

권장 API:

```text
GET    /api/tags
POST   /api/tags
PATCH  /api/tags/{tag_id}
DELETE /api/tags/{tag_id}
POST   /api/tags/link
DELETE /api/tags/link
GET    /api/tags/links
```

지원 대상:

```text
stock
trade
news
memo
```

기능:

```text
- 태그 생성/수정/삭제
- 대상에 태그 연결
- 대상에서 태그 제거
- 대상별 태그 조회
```

## 3. 거래-뉴스 연결 API

권장 API:

```text
GET    /api/trades/{trade_id}/news
POST   /api/trades/{trade_id}/news
DELETE /api/trades/{trade_id}/news/{news_id}
GET    /api/news/{news_id}/trades
```

기능:

```text
- 거래에 관련 뉴스 연결
- 거래에서 뉴스 연결 제거
- 거래별 연결 뉴스 조회
- 뉴스별 연결 거래 조회
```

연결 기준:

```text
trade_news_links
```

## 4. 거래 화면 보완

대상:

```text
frontend/src/pages/main/trades/
```

구현 항목:

```text
- 거래 상세 또는 drawer에 메모 입력 영역 추가
- 거래에 태그 추가/제거
- 거래에 관련 뉴스 연결/해제
- 거래별 연결 뉴스 목록 표시
- 매수/매도 사유를 메모로 기록
```

## 5. 뉴스 화면 보완

대상:

```text
frontend/src/pages/main/news/
```

구현 항목:

```text
- 뉴스 상세에서 관련 거래 연결/조회
- 뉴스에 메모 추가
- 뉴스에 태그 추가/제거
```

## 6. 종목 화면 보완

대상:

```text
frontend/src/pages/main/stocks/
```

가능한 범위에서 구현:

```text
- 종목 메모 표시
- 종목 태그 표시
- 종목별 메모/태그 추가
```

복잡하면 거래/뉴스 화면 우선으로 구현하고, 종목 화면은 최소 연결만 한다.

## 검증 항목

Backend:

```text
- python -m compileall app 성공
- 메모 CRUD 성공
- 태그 CRUD 성공
- 거래에 메모 연결 성공
- 뉴스에 메모 연결 성공
- 종목에 메모 연결 성공
- 거래에 태그 연결/해제 성공
- 뉴스에 태그 연결/해제 성공
- 거래-뉴스 연결/해제 성공
- 거래별 연결 뉴스 조회 성공
- 뉴스별 연결 거래 조회 성공
```

Frontend:

```text
- 거래 화면에서 메모 작성/수정/삭제 확인
- 거래 화면에서 태그 추가/제거 확인
- 거래 화면에서 뉴스 연결/해제 확인
- 뉴스 화면에서 연결 거래 조회 확인
- npm run build 성공
```

Regression:

```text
/health
/api/auth/status
/api/prices/summary
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
docs/MEMO_TAG_TRADE_NEWS_REPORT.md
```

포함 내용:

```markdown
# MEMO TAG TRADE NEWS REPORT

## 1. 작업 개요

## 2. 구현한 API

## 3. 메모 구조

## 4. 태그 구조

## 5. 거래-뉴스 연결 구조

## 6. Frontend 연결 결과

## 7. 테스트 결과

## 8. 확인 필요 항목

## 9. 다음 단계 제안
```

## 완료 조건

```text
- 메모 CRUD 구현
- 태그 CRUD 구현
- tag_links 연결/해제 구현
- trade_news_links 연결/해제 구현
- 거래 화면 메모/태그/뉴스 연결
- 뉴스 화면 메모/태그/거래 연결
- Backend compile 성공
- Frontend build 성공
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 다음과 같이 보고하세요.

```text
거래-뉴스 연결, 메모, 태그 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
