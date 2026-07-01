# MVP COMPLETION REPORT

## 1. MVP 1차 완료 선언

- 현재 저장소는 1차 MVP 범위 기준 구현, 통합 검증, 브라우저 화면 QA, 문서 정리까지 완료된 상태로 정리되었다.
- 이번 문서는 향후 기능 확장 문서가 아니라 현재 MVP 완료 범위를 고정해서 보는 기준 문서다.

## 2. 구현 완료 기능

1. 기본 프로젝트 구조
   - backend domain structure
   - frontend menu-based structure
   - environment-based local execution flow
2. 27개 MVP DB 테이블
   - confirmed MVP schema 기준 유지
3. 종목 관리
   - 종목 조회
   - 종목 검색
   - 활성 상태 기반 조회
4. KODEX 구성종목 import
   - index constituents 기반 import 구조 반영
5. KRX 가격 수집
   - 일별 가격 수집
   - 범위 수집 검증
   - duplicate cleanup/validation 흐름 확보
6. 차트 / MA / RSI / MACD
   - 기본 차트 렌더
   - 기간 필터
   - 보조지표 토글
7. Naver 뉴스 수집
   - 뉴스 목록
   - 수집 job 구조
   - 링크 및 요약 연결 기반
8. GPT 뉴스 요약 / 필터 구조
   - GPT 처리 대상 조회
   - 상태 확인
   - 요약 및 후보 처리 구조 확보
9. 뉴스 알림 후보 / Gmail 발송 구조
   - 후보 생성
   - 발송 job 구조
   - dry-run 중심 검증
10. 가격 알림 / Gmail 발송 구조
   - 목표가 상향/하향
   - 최근 60일 고점 대비 하락
   - 최근 60일 저점 대비 상승
   - dry-run, evaluate, history 기록
11. 거래 기록 / 자금 / 보유 / 손익
   - fund pool
   - 입출금
   - 매수/매도 거래
   - holdings 재계산
   - portfolio summary
12. 메모 / 태그 / 거래-뉴스 연결
   - 메모 CRUD
   - 태그 및 태그 링크
   - trade-news links
13. 대시보드
   - 주요 KPI
   - 최근 뉴스
   - 최근 거래
   - 최근 알림
   - quick navigation
14. scheduled_jobs 기반 수동 job runner
   - jobs 목록
   - summary
   - 수동 실행 UI/endpoint 구조
15. 통합 regression
   - 핵심 API 회귀 점검 완료
   - compile/build 검증 완료 이력 확보
16. 브라우저 화면 QA
   - Codex in-app browser 기준 주요 화면 점검 완료

## 3. Backend 구성 요약

- FastAPI 기반 domain router 구조
- stocks, collection, prices, news, portfolio, trades, alerts, charts, memos, settings, jobs, dashboard domain 반영
- scheduled job execution path 보유
- local dev CORS는 `localhost`와 `127.0.0.1` 모두 대응

## 4. Frontend 구성 요약

- Vue 3 + TypeScript + Vite + Element Plus
- 주요 메뉴 라우트:
  - `/dashboard`
  - `/stocks`
  - `/collection`
  - `/news`
  - `/portfolio`
  - `/trades`
  - `/alerts`
  - `/charts`
  - `/memos`
  - `/settings`
- 차트 필터, 알림 폼, 거래/포트폴리오 화면, 뉴스 drawer, 설정 jobs 화면까지 기본 QA 완료

## 5. DB 구성 요약

- 기준 문서: `docs/MVP_DB_SCHEMA_v1.2.md`
- MVP 27-table structure 유지
- 새 테이블 없음
- 새 마이그레이션 없음
- wrap-up 단계에서 schema drift 없음

## 6. 외부 연동 요약

- Google OAuth 구조 포함
- Gmail SMTP 발송 구조 포함
- KRX Open API 기반 가격 수집 구조 포함
- Naver 뉴스/현재가 연동 구조 포함
- OpenAI GPT mini / GPT-5 계열 처리 구조 포함
- 단, 실제 운영 성공 여부는 key, quota, billing, SMTP 설정에 의존

## 7. 검증 완료 항목

- backend compile 검증 이력 확보
- frontend build 검증 이력 확보
- 주요 regression API 응답 확인
- 가격 수집 duplicate 검증 이력 확보
- sample trade / holdings / portfolio 정합성 검증 이력 확보
- price alert dry-run / evaluate 흐름 검증 이력 확보
- memos / tags / trade-news link 검증 이력 확보
- browser 화면 QA 완료

## 8. 운영 전 체크리스트

1. `backend/.env` 값을 확인한다.
2. Gmail SMTP 계정과 앱 비밀번호 또는 발송 설정을 확인한다.
3. `KRX_AUTH_KEY` 설정을 확인한다.
4. OpenAI API key, billing, quota 상태를 확인한다.
5. SQLite DB 백업 위치와 백업 주기를 확인한다.
6. KRX 가격 수집 기준일과 수집 범위를 확인한다.
7. 뉴스 수집은 먼저 dry-run 또는 비발송 경로로 확인한다.
8. 알림 발송은 먼저 dry-run 또는 작은 limit로 확인한다.
9. 주요 화면을 실제 브라우저에서 한 번 더 점검한다.
10. 배포 전 `npm run build`와 핵심 API 상태를 다시 확인한다.

## 9. 보류 항목

- OpenAI quota / GPT filter 실제 운영 성공률 재확인
- 종목명 / 뉴스명 인코딩 이슈 재현 여부 추가 확인
- ECharts 성능 최적화 필요 여부 확인
- frontend bundle chunk-size warning 최적화
- 장기 실행용 background job 운영 방식 정리
- job config 직접 편집 UI 고도화
- 종목 상세 메모 / 태그 전용 UI
- 거래 시점 `price_snapshot` 자동 생성 고도화
- trade-news link 입력 UX 개선
- 알림 quick-entry
- 더 풍부한 대시보드 샘플 데이터/요약 표현

## 10. 후속 작업 우선순위

1. 운영 credential readiness 확인
   - Gmail, OpenAI, KRX key 실환경 점검
2. 안정화
   - 장시간 job 실행과 예외 처리 보강
3. 성능/패키징
   - frontend bundle split
   - chart/data loading 비용 점검
4. UX 개선
   - quick-entry
   - 상세 연결 입력 UX
   - 설정 UI 세분화
5. 선택적 기능 확장
   - phase-2 scope에서만 검토

## 11. 최종 판단

- 현재 저장소는 1차 MVP 완료 상태로 볼 수 있다.
- 다만 운영 투입 전에는 credential, quota, SMTP, KRX key 같은 외부 의존성 점검이 반드시 필요하다.
- 후속 과제는 모두 별도 작업으로 다루고, 현재 MVP 완료 상태 자체는 유지하는 것이 적절하다.
