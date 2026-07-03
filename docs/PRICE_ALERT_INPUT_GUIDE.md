# PRICE ALERT INPUT GUIDE

## 1. 목적

- 가격 알림을 실제로 등록하기 전에, 사용자가 명확한 조건을 한 번에 전달할 수 있도록 입력 형식을 정리한 가이드다.
- 이 문서의 예시는 입력 형식 안내용이며, 예시 자체로 알림을 생성하지 않는다.

## 2. 현재 보유 종목

현재 기준 보유 종목:

| stock_name | stock_code | quantity | average_price | current_price |
|---|---|---:|---:|---:|
| 삼성SDI | `006400` | 5 | 596970 | 185300 |
| 두산에너빌리티 | `034020` | 10 | 105215 | 61900 |
| 삼성E&A | `028050` | 10 | 55809 | 23200 |
| NAVER | `035420` | 2 | 256500 | 253000 |

## 3. 알림 조건 종류

`TARGET_PRICE_ABOVE`

- 현재가가 특정 가격 이상일 때 알림

`TARGET_PRICE_BELOW`

- 현재가가 특정 가격 이하일 때 알림

`DROP_FROM_HIGH`

- 최근 60일 고점 대비 일정 비율 하락 시 알림

`RISE_FROM_LOW`

- 최근 60일 저점 대비 일정 비율 상승 시 알림

## 4. 입력 형식

권장 CSV 형식:

```csv
stock_name,stock_code,alert_name,alert_type,target_price,threshold_percent,enabled,memo
```

입력 규칙:

- `TARGET_PRICE_ABOVE` / `TARGET_PRICE_BELOW`
  - `target_price` 필수
  - `threshold_percent` 비워 둠
- `DROP_FROM_HIGH` / `RISE_FROM_LOW`
  - `threshold_percent` 필수
  - `target_price` 비워 둠
- `enabled`
  - `true` 또는 `false`
- `memo`
  - 사용 목적을 짧게 적음

## 5. 예시

다음은 입력 예시일 뿐이며, 이 문서만으로 실제 알림을 생성하지 않는다.

```csv
stock_name,stock_code,alert_name,alert_type,target_price,threshold_percent,enabled,memo
NAVER,035420,NAVER 진입 알림,TARGET_PRICE_BELOW,190000,,true,사용자 지정 진입 가격
삼성SDI,006400,삼성SDI 회복 알림,TARGET_PRICE_ABOVE,400000,,true,사용자 지정 반등 가격
두산에너빌리티,034020,두산 급락 확인,DROP_FROM_HIGH,,12,true,최근 60일 고점 대비 하락률
삼성E&A,028050,삼성E&A 반등 확인,RISE_FROM_LOW,,15,true,최근 60일 저점 대비 상승률
```

## 6. dry-run 확인 순서

1. 사용자가 위 형식으로 조건을 명시한다.
2. 알림 등록 전 조건이 명확한지 확인한다.
3. 등록 후 `/api/price-alerts/evaluate/dry-run`으로 먼저 평가한다.
4. dry-run 결과에서 다음을 본다.
   - `evaluated_count`
   - `matched_count`
   - `sendable_count`
   - `skip_reason`
5. dry-run 결과가 의도와 맞는지 확인한 뒤에만 실제 발송 여부를 검토한다.

## 7. 실제 Gmail 발송 전 체크리스트

- 사용자가 명시적으로 알림 조건을 제공했는가
- 종목 코드와 종목명이 현재 시스템 종목과 일치하는가
- `alert_type`에 맞는 값이 들어갔는가
- 먼저 dry-run 결과를 확인했는가
- 실제 발송이 필요한지 사용자가 다시 확인했는가
- Gmail 설정이 준비되어 있는가

## 8. 중복 발송 방지 기준

현재 로직 기준:

- 같은 가격 알림이 같은 날 이미 `sent` 이력이 있으면 다시 보내지 않음
- 같은 날 `failed` 이력이 있으면 기본적으로 재시도하지 않음
- 단, `force=true`면 failed 재평가를 허용할 수 있음
- 일일 발송 한도와 최근 1시간 발송 한도를 초과하면 발송하지 않음

## 9. 주의사항

- 사용자가 명시하지 않은 목표가를 임의로 만들지 않는다.
- 평균단가 기준으로 자동 목표가를 추정하지 않는다.
- 현재가 기준 몇 퍼센트 같은 임의 조건을 자동 생성하지 않는다.
- dry-run은 실제 Gmail을 보내지 않는다.
- 실제 발송 API는 사용자 확인 없이 실행하지 않는다.
