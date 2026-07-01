# CODEX_TASK_1.18

이전 작업 컨텍스트를 유지하고 이어서 진행하세요.

CDP 액세스 전체 활성화를 켰습니다.

이번 작업은 **Codex in-app browser 기반 MVP 화면 QA**입니다.

## 작업 목표

1. 실제 브라우저에서 주요 MVP 화면을 열어 육안 QA를 진행한다.
2. 콘솔 에러, 네트워크 실패, 레이아웃 깨짐, 한글 깨짐을 확인한다.
3. 실제 Gmail 발송은 하지 않는다.
4. 새 기능 추가는 하지 않는다.
5. 새 테이블과 마이그레이션은 만들지 않는다.

## 작업 전 준비

Backend와 Frontend를 실행한다.

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

Codex in-app browser로 아래 URL을 연다.

```text
http://127.0.0.1:5173/dashboard
```

## 확인 대상 화면

아래 화면을 순서대로 확인한다.

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
2. 콘솔 에러 여부
3. 네트워크 API 실패 여부
4. 레이아웃 깨짐 여부
5. 버튼/폼/테이블 표시 상태
6. 한글 깨짐 여부
7. 빈 데이터 상태 표시 정상 여부
8. 로딩/오류 상태 처리 이상 여부
```

## 핵심 화면 집중 확인

특히 아래 화면은 더 자세히 확인한다.

```text
/dashboard
/charts
/alerts
/trades
/portfolio
/news
/settings
```

### Dashboard

확인 항목:

```text
- KPI 카드 표시
- 최근 뉴스 표시
- 최근 알림 표시
- 빈 거래/보유 데이터 상태 정상 표시
- quick navigation 버튼 표시
```

### Charts

확인 항목:

```text
- 삼성전자 차트 표시
- 1개월/3개월/6개월/1년 필터 동작
- MA20/60/120 토글 동작
- RSI/MACD 토글 동작
- SVG 차트 깨짐 여부
- 한글/숫자/축 표시 이상 여부
```

### Alerts

확인 항목:

```text
- 가격 알림 목록 표시
- 알림 생성 폼 표시
- 조건 선택 표시
- dry-run 버튼 동작
- 실제 발송 버튼은 누르지 않음
- 이력 테이블 표시
```

### Trades / Portfolio

확인 항목:

```text
- 거래 입력 폼 표시
- 자금 풀/입출금 영역 표시
- 보유 목록 빈 상태 표시
- 손익 요약 카드 표시
```

### News

확인 항목:

```text
- 뉴스 목록 표시
- 뉴스 상세 drawer 표시
- 메모/태그/관련 거래 영역 표시
- 한글 뉴스 제목 깨짐 여부
```

### Settings

확인 항목:

```text
- scheduled job 목록 표시
- job 상태 표시
- 수동 실행 버튼 표시
- 실제 발송성 job은 실행하지 않음
```

## 금지 사항

```text
- 실제 Gmail 발송 금지
- news_alert_send 실제 실행 금지
- price_alert_evaluate 실제 발송 금지
- 새 기능 추가 금지
- 새 테이블/마이그레이션 생성 금지
- 테스트 데이터 대량 생성 금지
```

필요한 경우 dry-run만 사용한다.

## Backend / Build 확인

마지막에 아래도 확인한다.

```bash
cd backend
python -m compileall app
```

```bash
cd frontend
npm run build
```

Regression API:

```text
/health
/api/auth/status
/api/dashboard/summary
/api/prices/summary
/api/portfolio/summary
/api/price-alerts/summary
/api/jobs/summary
```

## 문서 갱신

작업 완료 후 아래 문서를 갱신한다.

```text
docs/CODEX_PROGRESS.md
docs/DEVELOPMENT_REPORT.md
```

필요 시 새 문서를 작성한다.

```text
docs/MVP_BROWSER_QA_REPORT.md
```

포함 내용:

```markdown
# MVP BROWSER QA REPORT

## 1. 작업 개요

## 2. 화면별 QA 결과

## 3. 콘솔 에러 확인 결과

## 4. 네트워크 오류 확인 결과

## 5. 레이아웃 / 한글 깨짐 확인 결과

## 6. 발견한 문제

## 7. 수정한 문제

## 8. 보류 항목

## 9. 다음 단계 제안
```

## 완료 조건

```text
- 주요 화면 브라우저 진입 확인
- 콘솔 에러 확인
- 네트워크 실패 확인
- 레이아웃 깨짐 확인
- 한글 깨짐 확인
- 실제 Gmail 발송 없이 dry-run 중심 검증
- Backend compile 성공
- Frontend build 성공
- DEVELOPMENT_REPORT.md 갱신
```

작업 완료 후 다음과 같이 보고하세요.

```text
MVP 브라우저 화면 QA 작업 완료했습니다.
DEVELOPMENT_REPORT.md를 확인해 주세요.
```
