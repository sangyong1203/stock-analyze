# PORTFOLIO TRADE REPORT

## 1. 작업 개요

- 자금 풀, 입출금, 거래 기록, 보유현황, 포트폴리오 요약 구조를 기존 MVP 테이블만으로 구현했다.

## 2. 구현한 API

- `GET /api/funds/pools`
- `POST /api/funds/pools`
- `GET /api/funds/transactions`
- `POST /api/funds/transactions`
- `GET /api/funds/summary`
- `GET /api/trades`
- `POST /api/trades`
- `GET /api/trades/{trade_id}`
- `PATCH /api/trades/{trade_id}`
- `DELETE /api/trades/{trade_id}`
- `GET /api/holdings`
- `GET /api/holdings/summary`
- `POST /api/holdings/recalculate`
- `GET /api/portfolio/summary`

## 3. 거래 계산 기준

- 매수:
  - `amount = quantity * price`
  - `total_amount = amount + fee + tax`
- 매도:
  - `amount = quantity * price`
  - `total_amount = amount - fee - tax`
  - `realized_profit_loss = sell_net_amount - average_price * quantity`

## 4. holdings 재계산 방식

- trades를 `trade_date`, `id` 오름차순으로 순회
- 매수 시 수량 증가, 총원가 누적
- 평균단가 = `총원가 / 보유수량`
- 매도 시 평균단가 기준 실현손익 계산
- 남은 보유분 평균단가는 기존 평균단가 유지
- fund_pool 단위로 기존 holdings를 삭제 후 재생성

## 5. 포트폴리오 요약 계산 방식

- `total_cash = fund_pools.cash_balance 합계`
- `total_invested_amount = open holdings.total_buy_amount 합계`
- `total_market_value = open holdings.market_value 합계`
- `total_unrealized_profit_loss = open holdings.unrealized_profit_loss 합계`
- `realized_profit_loss = holdings.realized_profit_loss 합계`
- `total_asset_value = total_cash + total_market_value`

## 6. Frontend 연결 결과

- 거래 화면에서 자금 풀 선택, 종목 검색, 매수/매도 등록, 수정, 삭제 가능
- 포트폴리오 화면에서 자금 풀 생성, 입출금 입력, 보유 목록 조회, 재계산 가능

## 7. 테스트 결과

- 자금 풀 생성 성공
- 입금 기록 성공
- 매수 거래 등록 성공
- 매도 거래 등록 성공
- holdings 재계산 성공
- 포트폴리오 요약 API 성공
- Frontend build 성공

## 8. 확인 필요 항목

- `total_invested_amount` 의미 확정 필요
- `today_change_amount`, `today_change_rate` 계산 기준 장기적으로 보강 가능
- 종목명 인코딩 데이터 정비 필요

## 9. 다음 단계 제안

- 거래 관련 뉴스 연결 UI 추가
- price snapshot 자동 생성 연동
- 보유 종목 차트/메모 연결 강화
