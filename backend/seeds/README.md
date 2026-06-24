# Seed Data

## 기본 seed

```bash
python seeds/seed_defaults.py
```

생성 항목:

- app_settings 기본값
- scheduled_jobs 기본값
- news_keyword_settings 기본값
- alert_settings 기본값
- collection_rules 기본값

## KODEX 구성종목

KODEX 200 / KODEX 코스닥150 구성종목은 CSV 또는 XLSX 파일에서 import한다.

```bash
python seeds/import_index_constituents.py --file ./data/kodex200.csv --index-code KODEX_200 --index-name "KODEX 200" --effective-date 2026-06-24
python seeds/import_index_constituents.py --file ./data/kodex_kosdaq150.xlsx --index-code KODEX_KOSDAQ150 --index-name "KODEX 코스닥150" --effective-date 2026-06-24
```

지원 컬럼명:

- 종목코드: `stock_code`, `code`, `종목코드`, `단축코드`
- 종목명: `stock_name`, `name`, `종목명`, `한글종목명`
- 시장: `market`, `시장`, `시장구분`
