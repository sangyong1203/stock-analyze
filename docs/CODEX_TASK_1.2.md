# Codex 다음 작업 지시 프롬프트 v1.2

## 0. 작업 목표

이전 작업에서 다음 항목이 완료되었다.

- DB 스키마 검증
- named UNIQUE 인덱스 보정
- 설정 API CRUD 및 설정 화면 연결
- 종목 API CRUD 및 종목 화면 연결

이번 작업의 목표는 다음이다.

1. KODEX 200 / KODEX 코스닥150 구성종목 import 구조를 구현한다.
2. 수집 종목 관리 API를 구현한다.
3. 최종 수집 대상 산출 로직을 구현한다.
4. 수집 종목 관리 화면을 실제 API와 연결한다.

기준 문서:

```text
AGENTS.md
docs/INVESTMENT_SYSTEM_PLAN_v1.2.md
docs/MVP_DB_SCHEMA_v1.2.md
docs/DEVELOPMENT_REPORT.md
docs/SCHEMA_VALIDATION_REPORT.md
```

문서에 없는 기능은 임의로 추가하지 않는다.

---

## 1. 작업 범위

이번 작업의 중심 도메인은 다음이다.

```text
backend/app/domains/collection/
frontend/src/pages/main/collection/
backend/app/db/models.py
backend/seeds/
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 종목 도메인과 지수 구성종목 테이블을 함께 사용한다.

```text
backend/app/domains/stocks/
index_constituents
stock_collection_settings
collection_rules
stocks
holdings
price_alerts
```

---

## 2. KODEX 구성종목 import 구조 구현

### 2.1 목적

KODEX 200 / KODEX 코스닥150 구성종목 데이터를 `index_constituents` 테이블에 적재할 수 있는 구조를 만든다.

### 2.2 구현 항목

Backend에 import service를 구현한다.

```text
- KODEX 200 구성종목 CSV/Excel import
- KODEX 코스닥150 구성종목 CSV/Excel import
- 종목코드 기준 stocks 테이블과 연결
- stocks에 없는 종목은 기본 종목정보 생성
- index_constituents에 구성종목 저장
- 중복 import 방지
- 기존 구성종목 is_active 처리
```

### 2.3 파일 위치 권장

```text
backend/app/domains/collection/
  router.py
  service.py
  repository.py
  schemas.py

backend/seeds/
  import_index_constituents.py
```

### 2.4 API 골격

다음 API를 구현한다.

```text
POST /api/collection/index-constituents/import
GET  /api/collection/index-constituents
GET  /api/collection/index-constituents/summary
```

파일 업로드가 아직 복잡하면, 1차에서는 서버 로컬 파일 경로 기반 import도 허용한다.
단, 향후 파일 업로드 방식으로 확장 가능하게 service를 분리한다.

---

## 3. 수집 종목 관리 API 구현

### 3.1 목적

실제 뉴스/가격/알림 수집 대상 종목을 관리한다.

대상 테이블:

```text
stock_collection_settings
collection_rules
index_constituents
stocks
holdings
price_alerts
```

### 3.2 구현 API

다음 API를 구현한다.

```text
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

### 3.3 목록 조회 필터

수집 종목 목록은 다음 필터를 지원한다.

```text
- collect_enabled
- collect_news
- collect_alert_enabled
- priority
- collect_reason
- market
- index_code
- is_favorite
- keyword
```

### 3.4 응답에 포함할 계산값

수집 종목 목록 응답에는 다음 값을 포함한다.

```text
- stock_id
- stock_code
- stock_name
- market
- sector
- market_cap
- current_price
- is_favorite
- is_holding_calculated
- collect_enabled
- collect_news
- collect_price_snapshot
- collect_alert_enabled
- priority
- collect_reason
- manual_override
- manual_include
- manual_exclude
- last_collected_at
```

주의:

```text
is_holding_calculated는 holdings 기준으로 계산한다.
stocks 테이블에 is_holding 필드를 추가하지 않는다.
```

---

## 4. 최종 수집 대상 산출 로직 구현

### 4.1 우선순위

최종 수집 대상 산출 우선순위는 기준 문서에 따라 다음을 따른다.

```text
수동 제외 > 수동 포함 > 보유종목 > 관심종목 > 알림 설정 종목 > 조건 규칙
```

### 4.2 산출 로직

`POST /api/collection/stocks/recalculate` 실행 시 다음을 수행한다.

```text
1. 모든 활성 종목을 기준으로 후보를 조회한다.
2. index_constituents와 collection_rules를 기준으로 기본 후보군을 만든다.
3. holdings 기준 보유종목을 반영한다.
4. stocks.is_favorite 기준 관심종목을 반영한다.
5. price_alerts 기준 알림 설정 종목을 반영한다.
6. manual_include를 우선 반영한다.
7. manual_exclude를 최우선 제외 처리한다.
8. stock_collection_settings를 생성 또는 갱신한다.
```

### 4.3 collect_reason 처리

`collect_reason`은 다음 값 중 하나를 사용한다.

```text
manual_exclude
manual_include
holding
favorite
alert
index_rule
market_cap_rule
```

여러 조건이 겹칠 경우 우선순위가 높은 사유를 저장한다.

---

## 5. 수집 종목 관리 화면 연결

대상 화면:

```text
frontend/src/pages/main/collection/
```

### 5.1 구현 항목

다음 기능을 구현한다.

```text
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
```

### 5.2 KPI 예시

```text
- 전체 후보 종목 수
- 수집 활성 종목 수
- 뉴스 수집 대상 수
- 알림 대상 수
- 수동 포함 수
- 수동 제외 수
```

---

## 6. 테스트 항목

다음 테스트를 수행한다.

### 6.1 Backend

```text
- index_constituents 목록 조회
- index_constituents summary 조회
- collection stocks 목록 조회
- collection stocks summary 조회
- manual include 동작
- manual exclude 동작
- collection recalculate 동작
- collection rules CRUD 동작
```

### 6.2 Frontend

```text
- 수집 종목 관리 화면 접근
- 목록 조회 성공
- 필터 동작
- 수동 포함/제외 버튼 동작
- 재계산 버튼 동작
- build 성공
```

### 6.3 Regression

기존 기능이 깨지지 않았는지 확인한다.

```text
- /health
- /api/auth/status
- 설정 API
- 종목 API
- Frontend build
```

---

## 7. 문서 갱신

작업 완료 후 다음 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 다음 문서를 새로 작성한다.

```text
docs/COLLECTION_TARGET_REPORT.md
```

`COLLECTION_TARGET_REPORT.md`에는 다음 내용을 기록한다.

```markdown
# COLLECTION TARGET REPORT

## 1. 작업 개요

## 2. 구현한 API

## 3. 구현한 Frontend 기능

## 4. 수집 대상 산출 우선순위

## 5. 테스트 결과

## 6. 확인 필요 항목

## 7. 다음 단계 제안
```

---

## 8. 완료 조건

이번 작업 완료 조건은 다음이다.

```text
- KODEX 구성종목 import 구조 구현
- 수집 종목 관리 API 구현
- 최종 수집 대상 산출 로직 구현
- 수집 종목 관리 화면 실제 API 연결
- Backend 테스트 통과
- Frontend build 통과
- CODEX_PROGRESS.md 갱신
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 사용자에게 다음과 같이 보고한다.

```text
수집 종목 관리 및 KODEX 구성종목 import 구조 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
