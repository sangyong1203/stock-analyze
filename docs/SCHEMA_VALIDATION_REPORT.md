# SCHEMA VALIDATION REPORT

## 1. 검증 개요

- 기준 문서:
  - docs/INVESTMENT_SYSTEM_PLAN_v1.2.md
  - docs/MVP_DB_SCHEMA_v1.2.md
  - AGENTS.md
  - docs/DEVELOPMENT_REPORT.md
- 검증 대상: SQLAlchemy 모델, Alembic 마이그레이션, SQLite DB, seed 스크립트, Backend/Frontend 실행
- 검증 결과: named UNIQUE 인덱스 누락을 발견해 수정 완료. 최종 기준 문서와 일치.

## 2. DB 테이블 검증

| 테이블 | 존재 여부 | 필드 일치 | 비고 |
|---|---:|---:|---|
| users | O | O | 문서 필드 반영 |
| app_settings | O | O | 문서 필드 반영 |
| scheduled_jobs | O | O | 문서 필드 반영 |
| system_logs | O | O | 문서 필드 반영 |
| stocks | O | O | 문서 필드 반영 |
| index_constituents | O | O | 문서 필드 반영 |
| stock_prices | O | O | 문서 필드 반영 |
| price_snapshots | O | O | 문서 필드 반영 |
| corporate_actions | O | O | 문서 필드 반영 |
| stock_collection_settings | O | O | 문서 필드 반영 |
| collection_rules | O | O | 문서 필드 반영 |
| news | O | O | 문서 필드 반영 |
| news_stock_links | O | O | 문서 필드 반영 |
| news_keyword_settings | O | O | 문서 필드 반영 |
| news_collect_jobs | O | O | 문서 필드 반영 |
| news_collect_job_items | O | O | 문서 필드 반영 |
| fund_pools | O | O | 문서 필드 반영 |
| fund_transactions | O | O | 문서 필드 반영 |
| trades | O | O | 문서 필드 반영 |
| trade_news_links | O | O | 문서 필드 반영 |
| holdings | O | O | 문서 필드 반영 |
| price_alerts | O | O | 문서 필드 반영 |
| alert_settings | O | O | 문서 필드 반영 |
| alert_histories | O | O | 문서 필드 반영 |
| memos | O | O | 문서 필드 반영 |
| tags | O | O | 문서 필드 반영 |
| tag_links | O | O | 문서 필드 반영 |

## 3. 인덱스/제약조건 검증

| 항목 | 반영 여부 | 비고 |
|---|---:|---|
| uq_stocks_code | O | 명시적 UNIQUE 인덱스로 수정 완료 |
| idx_stocks_name | O | 반영 |
| uq_app_settings_key | O | 명시적 UNIQUE 인덱스로 수정 완료 |
| uq_scheduled_jobs_key | O | 명시적 UNIQUE 인덱스로 수정 완료 |
| idx_index_constituents_index_code | O | 반영 |
| idx_index_constituents_stock_code | O | 반영 |
| uq_index_constituents_unique | O | 명시적 UNIQUE 인덱스로 수정 완료 |
| idx_stock_prices_stock_date_timeframe | O | 반영 |
| uq_stock_prices_stock_date_timeframe | O | 명시적 UNIQUE 인덱스로 수정 완료 |
| idx_price_snapshots_stock_type | O | 반영 |
| idx_corporate_actions_stock_date | O | 반영 |
| idx_stock_collection_enabled | O | 반영 |
| uq_stock_collection_stock | O | 명시적 UNIQUE 인덱스로 수정 완료 |
| uq_news_url_hash | O | 명시적 UNIQUE 인덱스로 수정 완료 |
| idx_news_title_hash_published | O | 반영 |
| idx_news_group_key | O | 반영 |
| idx_news_published_at | O | 반영 |
| idx_news_market_scope | O | 반영 |
| idx_news_event_type | O | 반영 |
| idx_news_filter_status | O | 반영 |
| idx_news_importance_score | O | 반영 |
| idx_news_stock_links_news_id | O | 반영 |
| idx_news_stock_links_stock_id | O | 반영 |
| idx_trade_news_links_trade_id | O | 반영 |
| idx_trade_news_links_news_id | O | 반영 |
| idx_news_keyword_group_enabled | O | 반영 |
| uq_news_keyword_group_keyword | O | 명시적 UNIQUE 인덱스로 수정 완료 |
| idx_trades_stock_date | O | 반영 |
| idx_holdings_stock | O | 반영 |
| idx_price_alerts_stock_enabled | O | 반영 |
| idx_alert_histories_status | O | 반영 |
| idx_memos_stock | O | 반영 |
| idx_tag_links_target | O | 반영 |
| uq_tags_name_type | O | 명시적 UNIQUE 인덱스로 수정 완료 |
| 외래키 관계 | O | SQLAlchemy ForeignKey 기준 반영 |
| JSON 필드 | O | SQLite JSON 타입 매핑 확인 |
| Alembic 모델 일치 | O | `python -m alembic check` 통과 |

## 4. 제외 테이블 검증

| 제외 테이블 | 생성 여부 | 결과 |
|---|---:|---|
| auth_sessions | X | 정상 |
| stock_indicators | X | 정상 |
| trade_reviews | X | 정상 |
| stock_scores | X | 정상 |
| news_duplicates | X | 정상 |
| disclosures | X | 정상 |
| company_profiles | X | 정상 |
| backtest_results | X | 정상 |
| reports | X | 정상 |

## 5. Seed 검증

| Seed 항목 | 실행 결과 | 반복 실행 안정성 | 비고 |
|---|---:|---:|---|
| app_settings | O | O | 중복 생성 없음 |
| scheduled_jobs | O | O | 중복 생성 없음 |
| news_keyword_settings | O | O | 중복 생성 없음 |
| alert_settings | O | O | 중복 생성 없음 |

## 6. 실행 검증

| 항목 | 결과 | 비고 |
|---|---:|---|
| `python -m alembic upgrade head` | O | 20260624_0002까지 적용, 임시 신규 DB 기준 재검증 통과 |
| `python seeds/seed_defaults.py` | O | 반복 실행 통과 |
| `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` | O | `/health` 200 응답 확인 |
| `npm install` | O | 취약점 0건 |
| `npm run build` | O | 빌드 성공, chunk size 경고만 존재 |
| `npm run dev -- --host 127.0.0.1 --port 5173` | O | 200 응답 확인 |

## 7. 발견한 문제

- 문제: 문서에 지정된 `uq_*` UNIQUE 인덱스가 SQLite에서 명시적 이름으로 생성되지 않았다.
- 영향: UNIQUE 제약 자체는 동작했지만, 문서 기준의 named index 검증에는 불일치가 있었다.
- 수정 여부: 수정 완료. SQLAlchemy 모델을 명시적 unique Index로 조정하고 `20260624_0002_named_unique_indexes.py` 마이그레이션을 추가했다. 신규 DB에서 0001과 0002를 연속 적용해도 중복 인덱스 오류가 나지 않도록 보정했다.

## 8. 최종 판단

- [x] 기준 문서와 일치
- [ ] 일부 수정 필요
- [ ] 추가 확인 필요
