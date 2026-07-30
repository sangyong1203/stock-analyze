# PLAYWRIGHT STAGE 3 REPORT

## 1. 작업 개요

- 단계: 3단계 종목 / 수집 종목
- 방식: 실제 Vue 화면 + 실제 FastAPI + 별도 SQLite 테스트 DB
- API Mock: 사용하지 않음
- 운영 DB: 사용하지 않음
- GPT 기능: 사용하지 않음
- 실제 KRX 가격 수집: 실행하지 않음

## 2. 종목 테스트 결과

| 시나리오 | 결과 |
|---|---|
| 전체 활성 종목 조회 | 통과 |
| 코드/이름 검색 | 통과 |
| KOSPI/KOSDAQ 시장 필터 | 통과 |
| 관심종목 필터 | 통과 |
| 보유 여부 계산 | 통과 |
| 종목 KPI | 통과 |
| 종목 등록과 6자리 코드 정규화 | 통과 |
| 종목 수정과 별칭 저장 | 통과 |
| 관심 설정/해제 | 통과 |
| 종목 비활성화 | 통과 |

## 3. 수집 종목 테스트 결과

초기 기준값:

| 항목 | 값 |
|---|---:|
| 전체 후보 | 7 |
| 수집 활성 | 4 |
| 뉴스 수집 | 4 |
| 알림 대상 | 1 |
| 수동 포함 | 1 |
| 수동 제외 | 1 |

검증 결과:

| 시나리오 | 결과 |
|---|---|
| 우선순위/수집 여부/키워드 API 필터 | 통과 |
| 화면 KPI 및 검색/제외 필터 | 통과 |
| 수동 포함 | 통과 |
| 수동 제외 | 통과 |
| 수집 설정 초기화 | 통과 |
| 재계산: 7건 처리, 5건 활성, 수동 제외 1건 | 통과 |
| 규칙 등록 | 통과 |
| 규칙 수정 | 통과 |
| 규칙 비활성화 | 통과 |
| 규칙 삭제 | 통과 |

## 4. 발견한 실제 결함과 수정

### 수동 포함/제외 API HTTP 500

원인:

```text
repository.list_collection_stocks()
→ (rows, total_count) 반환
→ get_collection_stock_detail()이 반환값 전체를 행 목록으로 순회
→ ValueError: too many values to unpack
```

조치:

- `repository.get_collection_stock(stock_id)` 직접 조회 함수 추가
- `get_collection_stock_detail()`이 직접 조회 결과를 직렬화하도록 수정
- 수동 포함/제외 및 전체 회귀 재실행 통과

## 5. 선택자 교정 이력

- Element Plus 제목 중복은 heading level로 구분
- Select는 실제 `.el-select` 요소 기준으로 조작
- Dialog form-item은 정확한 라벨의 부모에서 input을 탐색
- 이는 애플리케이션 결함이 아니라 테스트 선택자 문제였음

## 6. 최종 테스트 결과

```text
Stage 3: 7 passed
Stage 1-2 regression: 10 passed
Total: 17 passed (28.6s)
Frontend build: passed
Python compile: passed
```

## 7. 산출물

```text
frontend/e2e/stocks.spec.ts
frontend/e2e/collection.spec.ts
frontend/playwright-report/index.html
frontend/test-results/.../stocks-filters.png
frontend/test-results/.../collection-filters.png
```

## 8. 제외 항목

- `KRX 가격 수집` 버튼
  - 외부 KRX API를 호출하고 가격 데이터를 변경하므로 결정적 화면 통합 테스트에서 제외
- GPT 기능 전체

## 9. 미완료 항목

- 4단계 뉴스 (GPT 제외)
- 5단계 포트폴리오 / 거래
- 6단계 알림 (실제 Gmail 발송 제외)
- 7단계 차트
- 8단계 메모 / 설정 (GPT 제외)

## 10. 확인 필요 항목

- 없음

## 11. 다음 단계

- 사용자 승인 후 4단계 뉴스 테스트만 진행한다.

## 12. 완료 문구

Playwright 테스트 DB 기반 통합 테스트 3단계 작업을 완료했습니다.
