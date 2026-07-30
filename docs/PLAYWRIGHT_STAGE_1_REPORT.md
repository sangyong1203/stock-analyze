# PLAYWRIGHT STAGE 1 REPORT

## 1. 작업 개요

- 단계: 1단계 인증 및 공통 레이아웃
- 방식: 실제 Vue 화면 + 실제 FastAPI + 별도 SQLite 테스트 DB
- API Mock: 사용하지 않음
- 운영 DB: 사용하지 않음
- GPT 기능: 테스트 제외
- 실제 Gmail 발송: 실행하지 않음

## 2. 테스트 환경

```text
Playwright Test: 1.61.1
Browser: Chromium 149.0.7827.55
Frontend: http://127.0.0.1:5174
Backend: http://127.0.0.1:8001
Database: backend/stock_analyze_e2e.db
Workers: 1
```

테스트 실행 시 다음 순서로 환경을 자동 구성한다.

1. 기존 `stock_analyze_e2e.db` 안전 확인 후 삭제
2. Alembic migration 적용
3. 기본 seed 실행
4. FastAPI 테스트 서버 시작
5. Vue/Vite 테스트 서버 시작
6. Chromium 통합 테스트 실행

## 3. 테스트 DB 결과

| 항목 | 결과 |
|---|---|
| Alembic version | `20260624_0002` |
| MVP table count | `27` |
| app_settings | `12` |
| scheduled_jobs | `8` |
| news_keyword_settings | `9` |
| alert_settings | `1` |

## 4. 테스트 시나리오 결과

| 시나리오 | 결과 |
|---|---|
| FastAPI health/auth/dashboard API 및 테스트 DB 연결 | 통과 |
| 보호 화면 접근 시 로그인 리다이렉트와 원래 경로 보존 | 통과 |
| 로그인 성공 callback과 localStorage 인증 상태 저장 | 통과 |
| 공통 메뉴를 통한 10개 MVP route 이동 | 통과 |
| 사이드 메뉴 접기/펼치기 | 통과 |
| 로그아웃과 인증 상태 제거 | 통과 |

최종 결과:

```text
6 passed (11.9s)
```

## 5. 실행 중 발견 및 조치 사항

### URL assertion 수정

- 최초 실행: 5 passed, 1 failed
- 실제 URL: `/login?redirect=/dashboard`
- 테스트 예상 URL: `/login?redirect=%2Fdashboard`
- 애플리케이션 결함이 아닌 테스트 예상값 문제로 확인
- 실제 Vue Router 동작에 맞게 assertion 수정 후 전체 재실행 통과

### 접근성 보완

- 사이드바 아이콘 버튼에 접근 가능한 이름이 없었음
- `메뉴 접기` / `메뉴 펼치기` 동적 `aria-label` 추가
- 역할과 이름 기반 Playwright 선택자로 검증 통과

## 6. 산출물

```text
frontend/playwright.config.ts
frontend/e2e/global-setup.ts
frontend/e2e/auth-layout.spec.ts
frontend/playwright-report/index.html
frontend/test-results/.../authenticated-dashboard.png
```

실패 시에만 trace, screenshot, video가 유지되며, 성공 결과에는 인증 후 대시보드 스크린샷을 별도 첨부한다.

## 7. 빌드 결과

- `npm run build`: 통과
- 기존 대형 chunk 경고는 유지됨
- 이번 테스트 단계에서 성능 구조 변경은 수행하지 않음

## 8. 미완료 항목

- 2단계 대시보드 상세 통합 테스트
- 3단계 종목 / 수집 종목 통합 테스트
- 4단계 뉴스 통합 테스트
- 5단계 포트폴리오 / 거래 통합 테스트
- 6단계 알림 통합 테스트
- 7단계 차트 통합 테스트
- 8단계 메모 / 설정 통합 테스트

## 9. 확인 필요 항목

- 항목: 실제 Google 계정 OAuth 승인 과정
- 관련 문서: `docs/INVESTMENT_SYSTEM_PLAN_v1.2.md`
- 애매한 이유: 개인 Google 계정 인증 자동화에는 보안 및 외부 인증 서비스 의존성이 있음
- 가능한 선택지: 수동 확인 / 별도 테스트 계정 정책 확정
- 추천안: 실제 Google 승인은 수동 확인, 내부 callback·guard·logout은 자동화 유지
- 현재 구현 여부: 보류

## 10. 다음 단계

- 사용자 승인 후 2단계 대시보드 테스트만 진행한다.

## 11. 완료 문구

Playwright 테스트 DB 기반 통합 테스트 1단계 작업을 완료했습니다.
