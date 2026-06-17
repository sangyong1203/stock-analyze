좋습니다. 권장안대로 반영해서 **1차 MVP DB 테이블 확정안 v1.2**로 정리합니다.

핵심 반영 사항은 다음입니다.

```text id="b218mp"
- corporate_actions 추가
- memos.context_json 추가
- 주요 UNIQUE 인덱스 추가
- DART 전용 저장 테이블은 1차 MVP DB에서 제외
- 최종 문서에는 이전 버전 변경/제거 표현 없이 현재 확정 구조만 작성
```

# 투자 분석 시스템 1차 MVP DB 테이블 확정안 v1.2

## 1. DB 설계 기준

1차 MVP DB는 다음 기능을 지원한다.

- Google OAuth 로그인
- 종목 기본정보 조회 및 보정
- KODEX 200 / KODEX 코스닥150 구성종목 관리
- 수집 종목 관리
- KRX 가격 데이터 저장
- 네이버 현재가 스냅샷 저장
- 네이버 금융 시장 뉴스 수집
- 뉴스 필터링
- 뉴스 중복 처리
- GPT mini 요약 저장
- GPT-5 재필터 결과 저장
- Gmail SMTP 알림
- 자금 풀 관리
- 입출금 관리
- 매수/매도 기록
- 거래와 관련 뉴스 연결
- 보유현황 계산
- 가격 알림
- 뉴스 알림
- 메모 관리
- 태그 관리
- 기본 차트 표시
- 차트의 매수/매도/기업 이벤트 표시
- 시스템 설정
- 수집/알림/시스템 로그

---

## 2. 1차 MVP 최종 테이블 목록

### 인증/설정/로그

```text
users
app_settings
scheduled_jobs
system_logs
```

### 종목/지수/가격/기업 이벤트

```text
stocks
index_constituents
stock_prices
price_snapshots
corporate_actions
```

### 수집 종목 관리

```text
stock_collection_settings
collection_rules
```

### 뉴스/뉴스 수집/GPT 처리

```text
news
news_stock_links
news_keyword_settings
news_collect_jobs
news_collect_job_items
```

### 자금/거래/보유현황

```text
fund_pools
fund_transactions
trades
trade_news_links
holdings
```

### 알림

```text
price_alerts
alert_settings
alert_histories
```

### 메모/태그

```text
memos
tags
tag_links
```

---

## 3. 인증/설정/로그 테이블

### 3.1 users

Google OAuth 로그인 사용자 테이블이다.

```text
users
- id
- email
- name
- google_sub
- avatar_url
- is_active
- is_admin
- last_login_at
- created_at
- updated_at
```

설명:

- 개인 단독 사용 기준이다.
- `email`은 허용 계정 검증에 사용한다.
- `google_sub`는 Google 계정 고유 식별자다.

---

### 3.2 app_settings

시스템 전역 설정 테이블이다.

```text
app_settings
- id
- setting_key
- setting_value
- value_type
- description
- created_at
- updated_at
```

저장 예시:

```text
news_collect_start_time = 07:30
news_collect_end_time = 23:30
news_collect_interval_minutes = 60

news_duplicate_window_market_hours = 24
news_duplicate_window_event_hours = 72

news_gpt_summary_min_score = 6
news_min_duplicate_for_summary = 2
news_min_source_for_summary = 2

news_alert_min_score = 7
news_alert_min_duplicate_count = 3

gmail_daily_limit = 200
gmail_hourly_limit = 50
```

---

### 3.3 scheduled_jobs

자동 실행 작업 설정 테이블이다.

```text
scheduled_jobs
- id
- job_key
- job_name
- enabled
- schedule_type
- cron_expression
- config_json
- last_run_at
- next_run_at
- created_at
- updated_at
```

`job_key` 예시:

```text
news_collect
index_constituents_update
krx_price_update
```

기본 스케줄 예시:

```text
news_collect:
- 매일 07:30 ~ 23:30
- 1시간 간격

index_constituents_update:
- 매월 1일

krx_price_update:
- 장마감 후 1회
```

---

### 3.4 system_logs

시스템 로그 테이블이다.

```text
system_logs
- id
- level
- category
- message
- context_json
- created_at
```

`level` 예시:

```text
info
warning
error
```

`category` 예시:

```text
auth
news_collect
price_collect
alert
gpt
system
```

---

## 4. 종목/지수/가격/기업 이벤트 테이블

### 4.1 stocks

종목 기본정보 테이블이다.

```text
stocks
- id
- code
- name
- market
- sector
- industry
- market_cap
- current_price
- change_rate
- aliases_json
- is_favorite
- is_active
- created_at
- updated_at
```

설명:

- `code`: 6자리 종목코드
- `market`: KOSPI 또는 KOSDAQ
- `market_cap`: KRX 일별매매정보 MKTCAP 기준
- `current_price`: 네이버 증권 현재가 스냅샷 또는 최신 가격 기준
- `aliases_json`: 뉴스 매칭용 별칭
- `is_favorite`: 관심종목 여부
- 보유 여부는 `holdings` 기준으로 계산한다.

---

### 4.2 index_constituents

KODEX 200 / KODEX 코스닥150 구성종목 테이블이다.

```text
index_constituents
- id
- index_code
- index_name
- tracking_index
- stock_id
- stock_code
- stock_name
- market
- effective_date
- is_active
- source
- created_at
- updated_at
```

`index_code` 예시:

```text
KODEX_200
KODEX_KOSDAQ150
```

설명:

- 구성종목 목록은 기초 후보군으로 사용한다.
- 실제 뉴스 수집 대상은 `stock_collection_settings`와 `collection_rules`로 산출한다.

---

### 4.3 stock_prices

종목 가격 이력 테이블이다.

```text
stock_prices
- id
- stock_id
- market
- date
- timeframe
- open
- high
- low
- close
- volume
- trade_value
- market_cap
- listed_shares
- change_price
- change_rate
- source
- created_at
```

`timeframe`:

```text
daily
weekly
monthly
```

`source`:

```text
KRX
manual
```

---

### 4.4 price_snapshots

특정 이벤트 당시 가격 스냅샷 테이블이다.

```text
price_snapshots
- id
- stock_id
- snapshot_type
- related_id
- price
- change_rate
- volume
- market_cap
- source
- captured_at
- created_at
```

`snapshot_type`:

```text
news
trade_buy
trade_sell
alert
memo
manual
```

`related_id` 사용 규칙:

```text
snapshot_type = news       → related_id = news.id
snapshot_type = trade_buy  → related_id = trades.id
snapshot_type = trade_sell → related_id = trades.id
snapshot_type = alert      → related_id = alert_histories.id 또는 price_alerts.id
snapshot_type = memo       → related_id = memos.id
snapshot_type = manual     → related_id = null 가능
```

`source`:

```text
naver
krx
manual
```

---

### 4.5 corporate_actions

종목별 기업 이벤트 테이블이다.

차트에서 병합, 분할, 무상증자, 유상증자 등을 표시하기 위해 사용한다.

```text
corporate_actions
- id
- stock_id
- action_type
- action_date
- base_date
- ratio
- description
- source
- created_at
- updated_at
```

`action_type`:

```text
split
reverse_split
bonus_issue
rights_issue
merger
```

설명:

- `split`: 액면분할 또는 주식분할
- `reverse_split`: 주식병합
- `bonus_issue`: 무상증자
- `rights_issue`: 유상증자
- `merger`: 합병 또는 병합성 이벤트
- `action_date`: 차트에 이벤트를 표시할 날짜
- `base_date`: 기준일이 별도로 필요한 경우 사용
- `ratio`: 분할/병합/증자 비율
- `source`: KRX, DART, manual 등

---

## 5. 수집 종목 관리 테이블

### 5.1 stock_collection_settings

실제 뉴스 수집 대상 종목 설정 테이블이다.

```text
stock_collection_settings
- id
- stock_id
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
- created_at
- updated_at
```

`priority`:

```text
high
normal
low
```

`collect_reason` 예시:

```text
index_rule
market_cap_rule
holding
favorite
alert
manual_include
manual_exclude
```

수집 대상 우선순위:

```text
수동 제외 > 수동 포함 > 보유종목 > 관심종목 > 알림 설정 종목 > 조건 규칙
```

---

### 5.2 collection_rules

수집 종목 조건 규칙 테이블이다.

```text
collection_rules
- id
- name
- rule_type
- enabled
- condition_json
- priority
- created_at
- updated_at
```

`rule_type` 예시:

```text
index
market_cap
market
sector
holding
favorite
alert
custom
```

`condition_json` 예시:

```json
{
  "target_indices": ["KODEX_200", "KODEX_KOSDAQ150"],
  "market_cap_min": 1000000000000
}
```

---

## 6. 뉴스/뉴스 수집/GPT 처리 테이블

### 6.1 news

대표 뉴스 저장 테이블이다.

중복 뉴스 원문은 저장하지 않고 대표 뉴스 1건만 저장한다.

```text
news
- id

- title
- url
- source
- published_at
- original_summary
- content_preview

- normalized_title
- url_hash
- title_hash
- news_group_key

- source_type
- market_scope
- event_type

- detected_stock_codes_json
- matched_index_codes_json
- is_index_member_news

- duplicate_count
- source_count
- sources_json
- first_published_at
- last_published_at
- duplicate_check_window_hours

- filter_status
- filter_reason
- matched_keywords_json
- importance_score

- gpt_summary
- gpt_summary_model
- gpt_summary_status
- gpt_summary_at

- gpt_filter_result
- gpt_filter_reason
- gpt_filter_model
- gpt_filter_at

- is_gpt_summary_target
- is_alert_target

- collected_at
- created_at
- updated_at
```

`source_type`:

```text
naver_finance_market
naver_finance_stock
manual
```

`market_scope`:

```text
stock
sector
market
macro
policy
noise
```

`event_type` 예시:

```text
breaking
price_breakout
price_drop
market
macro
sector
policy
earnings
disclosure
contract
supply_contract
rights_issue
bonus_issue
buyback
dividend
shareholder_return
capacity_expansion
mna
legal_risk
technology
noise
```

`filter_status`:

```text
important_candidate
normal_candidate
exclude_candidate
review_needed
```

`gpt_summary_status`:

```text
pending
completed
failed
skipped
```

`gpt_filter_result`:

```text
important
price_impact
unnecessary
```

설명:

- `url`: 대표 뉴스 URL
- `source`: 대표 뉴스 언론사
- `sources_json`: 같은 이슈를 보도한 전체 언론사 목록
- `importance_score`: 0~10 기준 뉴스 중요도 점수
- `gpt_summary`: GPT mini 요약 결과
- `gpt_filter_result`: GPT-5 재필터 결과

---

### 6.2 news_stock_links

뉴스와 종목 연결 테이블이다.

```text
news_stock_links
- id
- news_id
- stock_id
- stock_code
- stock_name
- relation_type
- relation_score
- source_stock_code
- price_snapshot_id
- created_at
```

`relation_type`:

```text
direct
sector
related
market
noise
```

설명:

- 하나의 뉴스가 여러 종목과 연결될 수 있다.
- `source_stock_code`는 종목별 뉴스 페이지에서 수집한 경우 원래 페이지의 종목코드다.
- 네이버 금융 시장 뉴스에서는 `source_stock_code`가 null일 수 있다.

---

### 6.3 news_keyword_settings

뉴스 키워드 설정 테이블이다.

```text
news_keyword_settings
- id
- group_type
- keyword
- weight
- enabled
- is_default
- created_at
- updated_at
```

`group_type`:

```text
market
sector
macro
policy
exclude
event
```

---

### 6.4 news_collect_jobs

뉴스 수집 작업 단위 로그 테이블이다.

```text
news_collect_jobs
- id
- job_type
- source_type
- trigger_type
- status
- started_at
- finished_at
- target_url
- total_fetched_count
- new_count
- duplicate_count
- excluded_count
- gpt_target_count
- alert_target_count
- error_message
- created_at
```

`job_type`:

```text
market_news
stock_news
manual
scheduled
```

`trigger_type`:

```text
scheduled
manual
retry
```

`status`:

```text
pending
running
success
partial_success
failed
```

---

### 6.5 news_collect_job_items

뉴스 수집 작업의 세부 실행 결과 테이블이다.

```text
news_collect_job_items
- id
- job_id
- item_type
- target
- status
- fetched_count
- new_count
- duplicate_count
- excluded_count
- error_message
- started_at
- finished_at
- created_at
```

`item_type`:

```text
page
stock
keyword
```

---

## 7. 자금/거래/보유현황 테이블

### 7.1 fund_pools

투자금 풀 테이블이다.

```text
fund_pools
- id
- name
- currency
- cash_balance
- description
- is_active
- created_at
- updated_at
```

예시:

```text
국내주식 계좌
```

---

### 7.2 fund_transactions

현금 흐름 테이블이다.

```text
fund_transactions
- id
- fund_pool_id
- transaction_type
- amount
- currency
- related_trade_id
- memo
- transaction_date
- created_at
```

`transaction_type`:

```text
deposit
withdraw
buy
sell
dividend
fee
tax
adjustment
```

연결 규칙:

```text
매수 거래 생성:
- trades 1건 생성
- fund_transactions에 buy 현금 흐름 1건 생성
- fund_pools.cash_balance 감소

매도 거래 생성:
- trades 1건 생성
- fund_transactions에 sell 현금 흐름 1건 생성
- fund_pools.cash_balance 증가

입금/출금:
- trades 없이 fund_transactions만 생성

배당/수수료/세금/조정:
- 필요 시 trades 없이 fund_transactions만 생성 가능
```

---

### 7.3 trades

매수/매도 거래 기록 테이블이다.

```text
trades
- id
- fund_pool_id
- stock_id
- trade_type
- trade_date
- price
- quantity
- amount
- fee
- tax
- total_amount
- price_snapshot_id
- average_price_at_trade
- realized_profit_loss
- realized_profit_loss_rate
- target_price
- target_achieved
- target_achievement_rate
- loss_rate
- reason
- memo
- created_at
- updated_at
```

`trade_type`:

```text
buy
sell
```

설명:

- 매수/매도 사유를 저장한다.
- 거래 당시 가격 스냅샷을 연결한다.
- 매도 시 실현손익, 목표 달성률, 손실률을 저장한다.
- 거래와 관련된 뉴스는 `trade_news_links`로 연결한다.

---

### 7.4 trade_news_links

거래와 뉴스를 연결하는 테이블이다.

```text
trade_news_links
- id
- trade_id
- news_id
- link_type
- memo
- created_at
```

`link_type`:

```text
reason
reference
risk
follow_up
```

설명:

- 거래 1건에 여러 뉴스가 연결될 수 있다.
- 매수/매도 판단의 근거가 된 뉴스를 연결한다.
- 리스크 확인용 뉴스나 사후 추적 뉴스도 연결할 수 있다.

---

### 7.5 holdings

보유현황 테이블이다.

```text
holdings
- id
- fund_pool_id
- stock_id
- quantity
- average_price
- total_buy_amount
- current_price
- market_value
- unrealized_profit_loss
- unrealized_profit_loss_rate
- realized_profit_loss
- first_buy_date
- last_trade_date
- is_closed
- created_at
- updated_at
```

운영 규칙:

```text
holdings는 거래 기록을 기준으로 계산/갱신한다.
사용자가 직접 수량과 평균단가를 임의 수정하는 테이블이 아니다.

조정이 필요한 경우:
- fund_transactions의 adjustment
- 또는 별도 조정 거래 방식으로 처리한다.
```

---

## 8. 알림 테이블

### 8.1 price_alerts

가격 알림 테이블이다.

```text
price_alerts
- id
- stock_id
- alert_type
- target_price
- base_price
- threshold_rate
- direction
- enabled
- triggered
- triggered_at
- memo
- created_at
- updated_at
```

`alert_type`:

```text
direct_price
one_month_high_drop_rate
one_month_low_rise_rate
```

`direction`:

```text
above
below
```

---

### 8.2 alert_settings

뉴스/가격 알림 기준 설정 테이블이다.

```text
alert_settings
- id
- enabled
- news_alert_enabled
- price_alert_enabled
- target_scope
- min_importance_score
- min_duplicate_count
- min_source_count
- event_types_json
- keyword_groups_json
- max_daily_alerts
- max_hourly_alerts
- send_email
- created_at
- updated_at
```

기본값:

```text
enabled = true
news_alert_enabled = true
price_alert_enabled = true
target_scope = holding_favorite_alert
min_importance_score = 7
min_duplicate_count = 3
min_source_count = 2
max_daily_alerts = 200
max_hourly_alerts = 50
send_email = true
```

`target_scope`:

```text
holding_only
holding_favorite
holding_favorite_alert
all_collection_targets
```

---

### 8.3 alert_histories

알림 발송 이력 테이블이다.

```text
alert_histories
- id
- news_id
- stock_id
- price_alert_id
- alert_type
- recipient_email
- title
- message
- link_url
- status
- sent_at
- error_message
- created_at
```

`alert_type`:

```text
news
price_target
system
daily_limit_exceeded
```

`status`:

```text
pending
sent
failed
skipped
```

---

## 9. 메모/태그 테이블

### 9.1 memos

메모 테이블이다.

```text
memos
- id
- stock_id
- trade_id
- news_id
- price_snapshot_id
- memo_type
- title
- content
- context_json
- memo_date
- created_at
- updated_at
```

`memo_type`:

```text
stock
trade
news
chart
general
```

`context_json` 사용 예시:

```json
{
  "chart_timeframe": "weekly",
  "start_date": "2025-11-01",
  "end_date": "2026-02-01",
  "indicators": ["MA20", "MA60", "MACD"]
}
```

---

### 9.2 tags

태그 테이블이다.

```text
tags
- id
- name
- color
- tag_type
- created_at
- updated_at
```

`tag_type`:

```text
stock
trade
news
memo
common
```

---

### 9.3 tag_links

태그 연결 테이블이다.

```text
tag_links
- id
- tag_id
- target_type
- target_id
- created_at
```

`target_type`:

```text
stock
trade
news
memo
```

---

## 10. 주요 관계

### 10.1 종목 관계

```text
stocks 1 : N index_constituents
stocks 1 : N stock_prices
stocks 1 : N price_snapshots
stocks 1 : N corporate_actions
stocks 1 : 1 stock_collection_settings
stocks 1 : N news_stock_links
stocks 1 : N trades
stocks 1 : N holdings
stocks 1 : N price_alerts
```

### 10.2 뉴스 관계

```text
news 1 : N news_stock_links
news 1 : N trade_news_links
news 1 : N alert_histories
news 1 : N memos

stocks 1 : N news_stock_links
trades 1 : N trade_news_links
```

### 10.3 거래 관계

```text
fund_pools 1 : N fund_transactions
fund_pools 1 : N trades
fund_pools 1 : N holdings

trades 1 : N trade_news_links
trades 1 : N memos
trades 1 : 1 price_snapshots
```

### 10.4 알림 관계

```text
stocks 1 : N price_alerts
price_alerts 1 : N alert_histories
news 1 : N alert_histories
```

### 10.5 태그 관계

```text
tags 1 : N tag_links
tag_links.target_type + tag_links.target_id 로 대상 연결
```

---

## 11. 필수 인덱스

```sql
CREATE UNIQUE INDEX uq_stocks_code
ON stocks(code);

CREATE INDEX idx_stocks_name
ON stocks(name);

CREATE UNIQUE INDEX uq_app_settings_key
ON app_settings(setting_key);

CREATE UNIQUE INDEX uq_scheduled_jobs_key
ON scheduled_jobs(job_key);

CREATE INDEX idx_index_constituents_index_code
ON index_constituents(index_code);

CREATE INDEX idx_index_constituents_stock_code
ON index_constituents(stock_code);

CREATE UNIQUE INDEX uq_index_constituents_unique
ON index_constituents(index_code, stock_code, effective_date);

CREATE INDEX idx_stock_prices_stock_date_timeframe
ON stock_prices(stock_id, date, timeframe);

CREATE UNIQUE INDEX uq_stock_prices_stock_date_timeframe
ON stock_prices(stock_id, date, timeframe);

CREATE INDEX idx_price_snapshots_stock_type
ON price_snapshots(stock_id, snapshot_type);

CREATE INDEX idx_corporate_actions_stock_date
ON corporate_actions(stock_id, action_date);

CREATE INDEX idx_stock_collection_enabled
ON stock_collection_settings(collect_enabled);

CREATE UNIQUE INDEX uq_stock_collection_stock
ON stock_collection_settings(stock_id);

CREATE UNIQUE INDEX uq_news_url_hash
ON news(url_hash);

CREATE INDEX idx_news_title_hash_published
ON news(title_hash, published_at);

CREATE INDEX idx_news_group_key
ON news(news_group_key);

CREATE INDEX idx_news_published_at
ON news(published_at);

CREATE INDEX idx_news_market_scope
ON news(market_scope);

CREATE INDEX idx_news_event_type
ON news(event_type);

CREATE INDEX idx_news_filter_status
ON news(filter_status);

CREATE INDEX idx_news_importance_score
ON news(importance_score);

CREATE INDEX idx_news_stock_links_news_id
ON news_stock_links(news_id);

CREATE INDEX idx_news_stock_links_stock_id
ON news_stock_links(stock_id);

CREATE INDEX idx_trade_news_links_trade_id
ON trade_news_links(trade_id);

CREATE INDEX idx_trade_news_links_news_id
ON trade_news_links(news_id);

CREATE INDEX idx_news_keyword_group_enabled
ON news_keyword_settings(group_type, enabled);

CREATE UNIQUE INDEX uq_news_keyword_group_keyword
ON news_keyword_settings(group_type, keyword);

CREATE INDEX idx_trades_stock_date
ON trades(stock_id, trade_date);

CREATE INDEX idx_holdings_stock
ON holdings(stock_id);

CREATE INDEX idx_price_alerts_stock_enabled
ON price_alerts(stock_id, enabled);

CREATE INDEX idx_alert_histories_status
ON alert_histories(status);

CREATE INDEX idx_memos_stock
ON memos(stock_id);

CREATE INDEX idx_tag_links_target
ON tag_links(target_type, target_id);

CREATE UNIQUE INDEX uq_tags_name_type
ON tags(name, tag_type);
```

---

## 12. 1차 MVP DB 확정 요약

1차 MVP DB는 아래 27개 테이블로 구성한다.

```text
users
app_settings
scheduled_jobs
system_logs

stocks
index_constituents
stock_prices
price_snapshots
corporate_actions

stock_collection_settings
collection_rules

news
news_stock_links
news_keyword_settings
news_collect_jobs
news_collect_job_items

fund_pools
fund_transactions
trades
trade_news_links
holdings

price_alerts
alert_settings
alert_histories

memos
tags
tag_links
```

본 DB 구조는 1차 MVP 기능을 구현하기 위한 기준 구조로 사용한다.

DART 공시/기업정보 전용 저장 테이블은 1차 MVP DB에 포함하지 않는다.
1차에서는 네이버 금융 뉴스의 공시/실적/수주/증자 등 이벤트성 뉴스 필터링을 우선 사용한다.
