# OPERATION READY CHECKLIST

## 1. 목적

- 실제 운영 전 환경 준비 상태를 빠르게 확인하고, 실제 발송 없이 dry-run 중심으로 점검하기 위한 문서다.
- 민감정보 값 자체는 적지 않고 `configured/missing` 상태만 기록한다.

## 2. 환경변수 준비 결과

### Backend `.env`

| Item | Status | Note |
|---|---|---|
| `DATABASE_URL` | configured | SQLite DB 경로 사용 중 |
| `ALLOWED_ORIGIN` | configured | legacy 단일 origin 호환 |
| `ALLOWED_ORIGINS` | missing in current `.env` | 코드 기본값으로 `localhost`, `127.0.0.1` 지원 |
| `GMAIL_SMTP_HOST` | configured | 값 자체는 문서 미기록 |
| `GMAIL_SMTP_PORT` | configured | 값 자체는 문서 미기록 |
| `GMAIL_SMTP_USERNAME` | configured | 값 자체는 문서 미기록 |
| `GMAIL_SMTP_APP_PASSWORD` | configured | 값 자체는 문서 미기록 |
| `ALERT_RECIPIENT_EMAIL` | configured | 값 자체는 문서 미기록 |
| `OPENAI_API_KEY` | configured | 값 자체는 문서 미기록 |
| `OPENAI_NEWS_SUMMARY_MODEL` | configured | 모델명 자체는 코드/로그 기준 존재 확인 |
| `OPENAI_NEWS_FILTER_MODEL` | configured | 모델명 자체는 코드/로그 기준 존재 확인 |
| `KRX_AUTH_KEY` | configured | 값 자체는 문서 미기록 |
| `KRX_API_BASE_URL` | configured | KRX base URL 존재 확인 |

### Google OAuth

| Item | Status | Note |
|---|---|---|
| `GOOGLE_CLIENT_ID` | missing | 현재 `.env` 기준 |
| `GOOGLE_CLIENT_SECRET` | missing | 현재 `.env` 기준 |
| `GOOGLE_ALLOWED_EMAIL` | missing | 현재 `.env` 기준 |
| `/api/auth/status` `oauth_configured` | false | 런타임 기준 |
| `/api/auth/status` `allowed_email_configured` | false | 런타임 기준 |

### Frontend

| Item | Status | Note |
|---|---|---|
| `VITE_API_BASE_URL` override support | available | 없으면 기본값 사용 |
| API fallback base URL | configured in code | `http://127.0.0.1:8000` |
| local CORS compatibility | supported | `localhost` 및 `127.0.0.1` 대응 |

## 3. Gmail SMTP 준비 상태

- 환경변수 존재 상태: configured
- 실제 발송 테스트: 이번 작업에서는 미실행
- 운영 전 확인:
  1. 발신 계정 로그인 가능 여부 확인
  2. 앱 비밀번호 또는 SMTP 발송 권한 상태 확인
  3. `ALERT_RECIPIENT_EMAIL` 수신 주소 확인
  4. 실제 발송은 dry-run 이후 `limit 1`로만 점검

## 4. OpenAI API 준비 상태

- API key 상태: configured
- 뉴스 요약 모델: configured
- 뉴스 필터 모델: configured
- 이번 작업에서는 실제 GPT 호출 성공률을 추가 검증하지 않음
- 운영 전 확인:
  1. billing 활성 상태
  2. quota 초과 여부
  3. 사용 모델 접근 권한

## 5. KRX API 준비 상태

- `KRX_AUTH_KEY`: configured
- `KRX_API_BASE_URL`: configured
- 최근 가격 요약 엔드포인트 응답 정상 확인
- 운영 전 확인:
  1. 기준일이 최신인지
  2. 장 마감 이후 수집 시점인지
  3. 실패 시 재수집 범위를 어디까지 허용할지

## 6. SQLite DB 백업 플랜

### 현재 DB 위치

- 운영 DB: `backend/stock_analyze.db`
- 권장 백업 위치: `storage/backups/`

### 권장 파일명 규칙

```text
storage/backups/stock_analyze_YYYYMMDD_HHMMSS.db
```

### 수동 백업 절차

1. 가능하면 backend 서버를 먼저 중지한다.
2. 현재 시각 기준 백업 파일명을 만든다.
3. DB 파일을 `storage/backups/`로 복사한다.

예시 PowerShell:

```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item "backend/stock_analyze.db" "storage/backups/stock_analyze_$timestamp.db"
```

### 복구 절차

1. backend 서버를 중지한다.
2. 현재 DB를 별도 파일로 한 번 더 보관한다.
3. 복구할 백업 파일을 `backend/stock_analyze.db`로 복사한다.
4. 서버를 재시작하고 `/health`, `/api/jobs/summary`, `/api/prices/summary`를 확인한다.

예시 PowerShell:

```powershell
Copy-Item "storage/backups/stock_analyze_YYYYMMDD_HHMMSS.db" "backend/stock_analyze.db" -Force
```

## 7. 운영 전 dry-run 점검 결과

### Regression API

| Endpoint | Result |
|---|---|
| `/health` | 200 |
| `/api/auth/status` | 200 |
| `/api/jobs/summary` | 200 |
| `/api/prices/summary` | 200 |
| `/api/news/summary` | 200 |
| `/api/price-alerts/summary` | 200 |

### Dry-run API

| Endpoint | Result | Summary |
|---|---|---|
| `/api/news/alerts/send/dry-run` | 200 | candidate 2, sendable 0, skipped 2 |
| `/api/price-alerts/evaluate/dry-run` | 200 | evaluated 0, sendable 0 |

### 현재 참고 상태

- jobs summary:
  - `total_count = 8`
  - `failed_count = 0`
- prices summary:
  - `total_price_rows = 352427`
  - `latest_price_date = 2025-06-24`
  - `latest_updated_stocks_count = 2757`
- news summary:
  - `total_news_count = 18`
  - `alert_target_count = 2`
- price alerts summary:
  - `total_count = 0`

## 8. 첫 운영 데이터 입력 순서

1. DB 백업을 먼저 만든다.
2. fund pool을 생성한다.
3. 실제 보유 현금 기준 입금 내역을 입력한다.
4. 과거 거래를 어디까지 입력할지 기준일을 정한다.
5. 과거 매수/매도 거래를 순서대로 입력한다.
6. holdings와 portfolio summary가 기대값과 맞는지 확인한다.
7. 가격 알림은 먼저 dry-run으로만 확인한다.
8. 뉴스 알림도 먼저 후보와 dry-run만 확인한다.
9. 실제 발송은 `limit 1` 수준으로만 첫 테스트를 한다.

## 9. 알림 발송 이전 수칙

1. 실제 Gmail 발송 전에는 반드시 dry-run 결과를 본다.
2. 수신 주소가 본인 테스트용 주소인지 확인한다.
3. 최초 발송은 `limit 1`로만 진행한다.
4. price alert와 news alert를 동시에 대량 발송하지 않는다.
5. 발송 후 `alert_histories` 요약과 status를 바로 확인한다.

## 10. 보류 / 확인 필요 항목

- Google OAuth는 현재 미설정 상태다.
- `ALLOWED_ORIGINS`는 현재 `.env`에 없고 코드 기본값/legacy 설정으로 동작 중이다.
- OpenAI billing/quota는 문서 점검만으로 확정할 수 없다.
- 실제 SMTP 발송 가능 여부는 이번 작업에서 검증하지 않았다.
- backup 자동화는 아직 없고 현재는 수동 절차 기준이다.
