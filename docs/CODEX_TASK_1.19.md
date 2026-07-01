# CODEX_TASK_1.19

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

MVP 기능 구현, 통합 검증, 브라우저 화면 QA는 완료됐습니다.

이번 작업은 **MVP 1차 완료 정리 / 운영 전 체크리스트 / 후속 과제 정리**입니다.

## 작업 목표

1. 현재 MVP 구현 범위를 최종 정리한다.
2. 완료된 기능과 보류된 기능을 구분한다.
3. 운영 전 확인해야 할 체크리스트를 작성한다.
4. 후속 작업 후보를 우선순위별로 정리한다.
5. 불필요하거나 충돌하는 문서 내용을 정리한다.
6. 새 기능 추가는 하지 않는다.
7. 새 테이블과 마이그레이션은 만들지 않는다.

## 작업 항목

다음 문서를 기준으로 최종 상태를 정리한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
docs/MVP_INTEGRATION_CHECK_REPORT.md
docs/MVP_BROWSER_QA_REPORT.md
```

기준 문서를 반복해서 다시 읽지 않는다.
필요한 완료 보고서만 확인한다.

## 정리할 완료 범위

아래 기능이 MVP 1차에 포함됐는지 정리한다.

```text
1. 기본 프로젝트 구조
2. 27개 MVP DB 테이블
3. 종목 관리
4. KODEX 구성종목 import
5. KRX 가격 수집
6. 차트 / MA / RSI / MACD
7. 네이버 뉴스 수집
8. GPT 뉴스 요약 / 필터 구조
9. 뉴스 알림 후보 / Gmail 발송
10. 가격 알림 / Gmail 발송
11. 거래 기록 / 자금 / 보유 / 손익
12. 메모 / 태그 / 거래-뉴스 연결
13. 대시보드
14. scheduled_jobs 기반 수동 job runner
15. 통합 regression
16. 브라우저 화면 QA
```

## 보류 / 후속 과제 정리

아래 항목을 별도 섹션으로 정리한다.

```text
- OpenAI quota / GPT filter 실제 성공 재검증
- 종목명 / 뉴스명 인코딩 정합성 점검
- ECharts 재적용 여부
- Frontend bundle chunk-size warning 최적화
- 장기간 job background 실행
- job config 편집 UI
- 종목 상세 메모 / 태그 UI
- 거래 당시 price_snapshot 자동 생성
- trade_news_links 입력 UX 고도화
- 알림 quick-entry
- 실사용 데이터 입력 후 대시보드 재확인
```

## 운영 전 체크리스트

아래 체크리스트를 작성한다.

```text
1. backend/.env 확인
2. Gmail SMTP 실제 발송 설정 확인
3. KRX_AUTH_KEY 확인
4. OpenAI API key / billing / quota 확인
5. SQLite DB 백업 위치 확인
6. KRX 가격 수집 기준일 확인
7. 뉴스 수집 dry-run 확인
8. 알림 발송은 dry-run 후 limit 1로만 실제 발송
9. 주요 화면 브라우저 확인
10. npm run build 확인
```

## 문서 생성

새 문서를 작성한다.

```text
docs/MVP_COMPLETION_REPORT.md
```

구성:

```markdown
# MVP COMPLETION REPORT

## 1. MVP 1차 완료 선언

## 2. 구현 완료 기능

## 3. Backend 구성 요약

## 4. Frontend 구성 요약

## 5. DB 구성 요약

## 6. 외부 연동 요약

## 7. 검증 완료 항목

## 8. 운영 전 체크리스트

## 9. 보류 항목

## 10. 후속 작업 우선순위

## 11. 최종 판단
```

## DEVELOPMENT_REPORT.md 갱신

`DEVELOPMENT_REPORT.md`는 길게 누적하지 말고 이번 작업 결과만 짧게 정리한다.

포함 내용:

```text
- MVP 1차 완료 정리 작업 완료
- MVP_COMPLETION_REPORT.md 생성
- 새 기능 / 새 테이블 / 새 마이그레이션 없음
- 운영 전 체크리스트 작성
- 후속 작업 우선순위 정리
```

## 검증 항목

```text
- 기존 문서 충돌 여부 확인
- CODEX_PROGRESS.md 최신 상태 확인
- DEVELOPMENT_REPORT.md 갱신 확인
- MVP_COMPLETION_REPORT.md 작성 확인
- 새 코드 기능 추가 없음 확인
- 새 테이블 / 새 마이그레이션 없음 확인
```

필요하면 아래 최소 regression만 확인한다.

```text
/health
/api/auth/status
/api/dashboard/summary
/api/jobs/summary
/api/prices/summary
```

## 주의

```text
- 새 기능 추가하지 않는다.
- 코드 구조를 변경하지 않는다.
- 새 DB 테이블을 만들지 않는다.
- 새 마이그레이션을 만들지 않는다.
- 문서 정리 작업에 집중한다.
- 후속 과제는 구현하지 말고 목록화만 한다.
```

작업 완료 후 다음과 같이 보고하세요.

```text
MVP 1차 완료 정리 작업 완료했습니다.
DEVELOPMENT_REPORT.md와 MVP_COMPLETION_REPORT.md를 확인해 주세요.
```
