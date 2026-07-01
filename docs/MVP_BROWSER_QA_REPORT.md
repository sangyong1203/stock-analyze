# MVP BROWSER QA REPORT

## 1. 작업 개요

- 작업 기준: `docs/CODEX_TASK_1.18.md`
- 목적: Codex in-app browser로 주요 MVP 화면을 실제 렌더링 기준으로 점검
- 제한 준수:
  - 실제 Gmail 발송 미실행
  - `news_alert_send` 실제 실행 미실행
  - `price_alert_evaluate` 실제 발송 검증 미실행
  - 새 기능, 새 테이블, 새 마이그레이션 없음

## 2. 화면별 QA 결과

| Route | 결과 | 비고 |
|---|---|---|
| `/dashboard` | 정상 | KPI, 최근 뉴스, 최근 알림, quick navigation 확인 |
| `/stocks` | 정상 | 진입 및 기본 렌더 확인 |
| `/collection` | 정상 | 진입 및 기본 렌더 확인 |
| `/news` | 정상 | 목록 및 상세 drawer 확인 |
| `/portfolio` | 정상 | 요약 카드, 자금 폼, 빈 holdings 상태 확인 |
| `/trades` | 정상 | 거래 폼, 빈 목록 상태 확인 |
| `/alerts` | 정상 | 요약 카드, 생성 폼, dry-run 영역, 이력 테이블 확인 |
| `/charts` | 정상 | 기간 필터와 MA/RSI/MACD 토글 확인 |
| `/memos` | 정상 | 진입 및 기본 렌더 확인 |
| `/settings` | 정상 | 설정 화면 및 수동 작업 탭 확인 |

## 3. 콘솔 에러 확인 결과

- 초기 진입 시 CORS 문제로 API 로딩 실패가 있었음
- 원인:
  - frontend origin: `http://127.0.0.1:5173`
  - backend 허용 origin: `http://localhost:5173`만 설정
- 조치 후 결과:
  - application console error 없음
  - 남은 로그는 Vite dev client debug 로그뿐임

예:

```text
[vite] connecting...
[vite] connected.
```

## 4. 네트워크 오류 확인 결과

- 수정 전:
  - `OPTIONS` preflight 400 발생
  - `/api/dashboard/summary` 등 주요 API fetch 실패
- 수정 후:
  - 주요 화면 route scan 기준 loading-failed request 0
  - 점검 대상 회귀 API 모두 200

## 5. 레이아웃 / 한글 깨짐 확인 결과

- 대시보드, 뉴스, 거래, 알림, 차트, 설정 화면에서 눈에 띄는 한글 깨짐 미재현
- 빈 데이터 상태 렌더링 정상
- 차트 SVG 렌더링 이상 미확인
- 뉴스 상세 drawer 렌더링 정상

## 6. 발견된 문제

1. Local CORS origin mismatch
   - `127.0.0.1` 기반 frontend와 `localhost`만 허용한 backend가 충돌
   - 실제 브라우저 QA를 막는 원인이었음

2. Empty select placeholder regression
   - 선택 전 값이 placeholder 대신 `0`으로 보였음
   - 대상:
     - alerts
     - portfolio
     - trades

## 7. 수정된 문제

1. Backend CORS
   - `allowed_origins` 파싱 추가
   - `localhost`와 `127.0.0.1` 둘 다 허용
   - 기존 `allowed_origin`도 호환 유지

2. Frontend empty select initial value
   - sentinel `0` 대신 `null` 초기값 사용
   - placeholder가 정상 표시되도록 수정

## 8. 보류 항목

- 프런트 빌드 chunk size warning
  - 빌드는 성공
  - 이번 QA 범위에서는 성능 최적화 미진행

## 9. 다음 단계 제안

- 추후 필요 시 bundle splitting을 별도 성능 작업으로 분리
- 로컬 QA 시 `localhost`와 `127.0.0.1` 혼용에 대한 회귀가 없는지 유지 확인
