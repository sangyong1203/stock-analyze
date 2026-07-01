from sqlalchemy.orm import Session

from app.db.models import AlertSetting, AppSetting, CollectionRule, NewsKeywordSetting, ScheduledJob


DEFAULT_APP_SETTINGS = [
    ("news_collect_start_time", "07:30", "string", "News collect start time"),
    ("news_collect_end_time", "23:30", "string", "News collect end time"),
    ("news_collect_interval_minutes", "60", "integer", "News collect interval minutes"),
    ("news_duplicate_window_market_hours", "24", "integer", "Market news duplicate window"),
    ("news_duplicate_window_event_hours", "72", "integer", "Event news duplicate window"),
    ("news_gpt_summary_min_score", "6", "integer", "GPT summary min score"),
    ("news_min_duplicate_for_summary", "2", "integer", "GPT summary min duplicate count"),
    ("news_min_source_for_summary", "2", "integer", "GPT summary min source count"),
    ("news_alert_min_score", "7", "integer", "News alert min score"),
    ("news_alert_min_duplicate_count", "3", "integer", "News alert min duplicate count"),
    ("gmail_daily_limit", "200", "integer", "Gmail daily send limit"),
    ("gmail_hourly_limit", "50", "integer", "Gmail hourly send limit"),
]

DEFAULT_JOBS = [
    ("krx_price_daily", "KRX Daily Price Collect", "manual", {"markets": ["KOSPI", "KOSDAQ"], "dry_run": True}),
    ("krx_price_range", "KRX Range Price Collect", "manual", {"markets": ["KOSPI", "KOSDAQ"], "dry_run": True, "skip_empty": True}),
    ("naver_news_collect", "Naver News Collect", "manual", {"pages": 1, "max_items": 10}),
    ("gpt_news_summary", "GPT News Summary", "manual", {"limit": 5, "dry_run": True}),
    ("gpt_news_filter", "GPT News Filter", "manual", {"limit": 5, "dry_run": True}),
    ("news_alert_candidate", "News Alert Candidate Recalculate", "manual", {}),
    ("news_alert_send", "News Alert Send", "manual", {"limit": 10, "force": False, "dry_run": True}),
    ("price_alert_evaluate", "Price Alert Evaluate", "manual", {"limit": 10, "force": False, "dry_run": True}),
]

DEFAULT_KEYWORDS = [
    ("market", "KOSPI", 1),
    ("market", "KOSDAQ", 1),
    ("macro", "금리", 2),
    ("policy", "정책", 2),
    ("event", "실적", 5),
    ("event", "수주", 5),
    ("event", "배당", 5),
    ("exclude", "행사", -4),
    ("exclude", "광고", -5),
]

DEFAULT_COLLECTION_RULES = [
    ("KODEX 200 포함 종목", "index_member", {"index_code": "KODEX_200"}, 10),
    ("KODEX 코스닥 150 포함 종목", "index_member", {"index_code": "KODEX_KOSDAQ_150"}, 20),
    ("관심종목 포함", "favorite", {"is_favorite": True}, 30),
    ("보유종목 포함", "holding", {"is_holding": True}, 40),
    ("알림 설정 종목 포함", "alert", {"has_price_alert": True}, 50),
    ("시가총액 상위 종목 조건", "market_cap", {"market_cap_rank_lte": 200}, 60),
]


def seed_defaults(db: Session) -> None:
    for key, value, value_type, description in DEFAULT_APP_SETTINGS:
        if not db.query(AppSetting).filter(AppSetting.setting_key == key).first():
            db.add(AppSetting(setting_key=key, setting_value=value, value_type=value_type, description=description))

    for key, name, schedule_type, config in DEFAULT_JOBS:
        if not db.query(ScheduledJob).filter(ScheduledJob.job_key == key).first():
            db.add(ScheduledJob(job_key=key, job_name=name, schedule_type=schedule_type, config_json=config))

    for group_type, keyword, weight in DEFAULT_KEYWORDS:
        exists = (
            db.query(NewsKeywordSetting)
            .filter(
                NewsKeywordSetting.group_type == group_type,
                NewsKeywordSetting.keyword == keyword,
            )
            .first()
        )
        if not exists:
            db.add(NewsKeywordSetting(group_type=group_type, keyword=keyword, weight=weight, is_default=True))

    for name, rule_type, condition_json, priority in DEFAULT_COLLECTION_RULES:
        rule = db.query(CollectionRule).filter(CollectionRule.name == name).first()
        if rule:
            rule.rule_type = rule_type
            rule.condition_json = condition_json
            rule.priority = priority
            rule.enabled = True
        else:
            db.add(
                CollectionRule(
                    name=name,
                    rule_type=rule_type,
                    enabled=True,
                    condition_json=condition_json,
                    priority=priority,
                )
            )

    if not db.query(AlertSetting).first():
        db.add(AlertSetting())

    db.commit()
