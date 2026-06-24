from datetime import datetime
from hashlib import sha1
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import News, NewsCollectJob, NewsCollectJobItem, NewsStockLink, Stock
from app.domains.news import repository
from app.domains.news.schemas import (
    AlertCandidateItem,
    AlertCandidateRecalculateResult,
    AlertCandidateSummary,
    GptRunItem,
    GptRunRequest,
    GptRunResult,
    GptStatusSummary,
    GptTargetsSummary,
    MarketNewsCollectRequest,
    NewsReviewItem,
    NewsReviewUpdate,
    NewsSummary,
)
from app.external.openai import OpenAiNewsClient
from app.external.naver import NaverFinanceNewsClient
from app.external.naver.types import NaverNewsItem

SOURCE_TYPE = "naver_finance_market"
DUPLICATE_WINDOW_HOURS = 24

KEYWORD_RULES: tuple[tuple[int, tuple[str, ...], str], ...] = (
    (5, ("공시",), "disclosure"),
    (5, ("수주",), "contract"),
    (5, ("공급계약",), "supply_contract"),
    (5, ("실적",), "earnings"),
    (5, ("배당",), "dividend"),
    (5, ("자사주",), "buyback"),
    (5, ("유상증자",), "rights_issue"),
    (5, ("무상증자",), "bonus_issue"),
    (4, ("증설", "CAPA", "공장"), "capacity_expansion"),
    (4, ("인수합병", "M&A"), "mna"),
    (4, ("정부", "정책", "규제", "세제", "보조금"), "policy"),
    (3, ("기술", "특허", "인증", "양산", "임상"), "technology"),
    (3, ("시장", "코스피", "코스닥", "환율", "금리", "유가"), "market"),
    (2, ("반도체", "HBM", "전력", "ESS", "태양광", "2차전지", "로봇", "원전", "방산", "바이오"), "industry"),
    (-2, ("특징주", "단순 급등", "단순 급락"), "noise"),
    (-4, ("봉사활동", "기부", "행사", "사진", "광고"), "noise"),
)

GPT_SUMMARY_EVENT_TYPES = {
    "earnings",
    "disclosure",
    "contract",
    "supply_contract",
    "rights_issue",
    "bonus_issue",
    "buyback",
    "dividend",
    "capacity_expansion",
    "mna",
    "legal_risk",
    "technology",
}


def normalize_news_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    query = urlencode(sorted(parse_qsl(parsed.query, keep_blank_values=True)))
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, query, ""))


def normalize_news_title(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip().lower()


def _hash(value: str) -> str:
    return sha1(value.encode("utf-8")).hexdigest()


def generate_url_hash(url: str) -> str:
    return _hash(normalize_news_url(url))


def generate_title_hash(title: str) -> str:
    return _hash(normalize_news_title(title))


def calculate_basic_importance_score(text: str) -> tuple[int, list[str], str]:
    score = 0
    matched: list[str] = []
    event_type = "market"
    upper_text = text.upper()

    for weight, keywords, category in KEYWORD_RULES:
        for keyword in keywords:
            target = keyword.upper() if keyword.isascii() else keyword
            if target in upper_text:
                score += weight
                matched.append(keyword)
                if weight > 0 and event_type == "market":
                    event_type = category

    return max(0, min(10, score)), sorted(set(matched)), event_type


def detect_related_stocks(db: Session, item: NaverNewsItem) -> list[Stock]:
    text = f"{item.title} {item.summary or ''}"
    text_lower = text.lower()
    matches: list[Stock] = []

    for stock in repository.list_collect_target_stocks(db):
        aliases = stock.aliases_json if isinstance(stock.aliases_json, list) else []
        candidates = [stock.name, stock.code, *[str(alias) for alias in aliases if alias]]
        if any(candidate and candidate.lower() in text_lower for candidate in candidates):
            matches.append(stock)

    return matches


def _news_group_key(published_at: datetime, matched_stocks: list[Stock], event_type: str) -> str:
    main_entity = matched_stocks[0].code if matched_stocks else "market"
    return f"{published_at.date().isoformat()}:{main_entity}:{event_type}"


def _filter_status(score: int) -> str:
    if score >= 7:
        return "important_candidate"
    if score >= 4:
        return "normal_candidate"
    return "review_needed"


def is_gpt_summary_target(news: News | None = None, **values) -> bool:
    importance_score = values.get("importance_score", getattr(news, "importance_score", 0) if news else 0) or 0
    duplicate_count = values.get("duplicate_count", getattr(news, "duplicate_count", 0) if news else 0) or 0
    source_count = values.get("source_count", getattr(news, "source_count", 0) if news else 0) or 0
    event_type = values.get("event_type", getattr(news, "event_type", None) if news else None)
    is_alert_target_value = values.get("is_alert_target", getattr(news, "is_alert_target", False) if news else False)
    return (
        importance_score >= 6
        or duplicate_count >= 3
        or source_count >= 3
        or event_type in GPT_SUMMARY_EVENT_TYPES
        or bool(is_alert_target_value)
    )


def apply_gpt_target_status(news: News) -> None:
    target = is_gpt_summary_target(news)
    news.is_gpt_summary_target = target
    if target:
        if news.gpt_summary_status in {None, "skipped"}:
            news.gpt_summary_status = "pending"
    elif news.gpt_summary_status in {None, "pending", "failed", "skipped"}:
        news.gpt_summary_status = "skipped"


def save_news_with_duplicates(db: Session, item: NaverNewsItem, matched_stocks: list[Stock]) -> tuple[News, bool]:
    collected_at = datetime.utcnow()
    published_at = item.published_at or collected_at
    normalized_url = normalize_news_url(item.url)
    normalized_title = normalize_news_title(item.title)
    url_hash = generate_url_hash(item.url)
    title_hash = generate_title_hash(item.title)
    source = item.source or "naver_finance"
    score, keywords, event_type = calculate_basic_importance_score(f"{item.title} {item.summary or ''}")

    existing = repository.get_news_by_url_hash(db, url_hash)
    if existing is None:
        existing = repository.get_recent_news_by_title_hash(db, title_hash, DUPLICATE_WINDOW_HOURS)

    if existing is not None:
        sources = existing.sources_json if isinstance(existing.sources_json, list) else []
        if source not in sources:
            sources.append(source)
        existing.duplicate_count += 1
        existing.source_count = len(sources)
        existing.sources_json = sources
        existing.last_published_at = published_at
        existing.importance_score = max(existing.importance_score, score)
        existing.matched_keywords_json = sorted(set((existing.matched_keywords_json or []) + keywords))
        existing.is_alert_target = existing.is_alert_target or score >= 7
        apply_gpt_target_status(existing)
        existing.updated_at = collected_at
        return existing, False

    stock_codes = [stock.code for stock in matched_stocks]
    alert_target = score >= 7
    summary_target = is_gpt_summary_target(
        importance_score=score,
        duplicate_count=1,
        source_count=1,
        event_type=event_type,
        is_alert_target=alert_target,
    )
    news = News(
        title=item.title.strip(),
        url=normalized_url,
        source=source,
        published_at=published_at,
        original_summary=item.summary,
        content_preview=item.summary,
        normalized_title=normalized_title,
        url_hash=url_hash,
        title_hash=title_hash,
        news_group_key=_news_group_key(published_at, matched_stocks, event_type),
        source_type=SOURCE_TYPE,
        market_scope="stock" if matched_stocks else "market",
        event_type=event_type,
        detected_stock_codes_json=stock_codes or None,
        matched_index_codes_json=None,
        is_index_member_news=bool(matched_stocks),
        duplicate_count=1,
        source_count=1,
        sources_json=[source],
        first_published_at=published_at,
        last_published_at=published_at,
        duplicate_check_window_hours=DUPLICATE_WINDOW_HOURS,
        filter_status=_filter_status(score),
        filter_reason="keyword_basic_score",
        matched_keywords_json=keywords,
        importance_score=score,
        gpt_summary_status="pending" if summary_target else "skipped",
        is_gpt_summary_target=summary_target,
        is_alert_target=alert_target,
        collected_at=collected_at,
    )
    db.add(news)
    db.flush()
    return news, True


def create_news_stock_links(db: Session, news: News, matched_stocks: list[Stock]) -> int:
    created = 0
    existing_stock_ids = {
        link.stock_id
        for link in db.query(NewsStockLink).filter(NewsStockLink.news_id == news.id).all()
        if link.stock_id is not None
    }
    for stock in matched_stocks:
        if stock.id in existing_stock_ids:
            continue
        db.add(
            NewsStockLink(
                news_id=news.id,
                stock_id=stock.id,
                stock_code=stock.code,
                stock_name=stock.name,
                relation_type="mentioned",
                relation_score=1,
                source_stock_code=None,
            )
        )
        created += 1
    return created


def collect_market_news(db: Session, payload: MarketNewsCollectRequest) -> NewsCollectJob:
    started_at = datetime.utcnow()
    client = NaverFinanceNewsClient()
    job = NewsCollectJob(
        job_type="market_news",
        source_type=SOURCE_TYPE,
        trigger_type="manual",
        status="running",
        started_at=started_at,
        target_url=client.base_url,
    )
    db.add(job)
    db.flush()

    errors: list[str] = []
    total_processed = 0

    for page in range(1, payload.pages + 1):
        item_started_at = datetime.utcnow()
        job_item = NewsCollectJobItem(
            job_id=job.id,
            item_type="page",
            target=f"{client.base_url}?page={page}",
            status="running",
            started_at=item_started_at,
        )
        db.add(job_item)
        db.flush()

        try:
            fetched_items = client.fetch_market_news(page=page)
            if payload.max_items:
                remaining = payload.max_items - total_processed
                fetched_items = fetched_items[: max(0, remaining)]

            for item in fetched_items:
                if not item.title or not item.url:
                    job_item.excluded_count += 1
                    continue
                matched_stocks = detect_related_stocks(db, item)
                news, is_new = save_news_with_duplicates(db, item, matched_stocks)
                create_news_stock_links(db, news, matched_stocks)
                job_item.fetched_count += 1
                if is_new:
                    job_item.new_count += 1
                    if news.is_gpt_summary_target:
                        job.gpt_target_count += 1
                    if news.is_alert_target:
                        job.alert_target_count += 1
                else:
                    job_item.duplicate_count += 1
                total_processed += 1

            job_item.status = "success"
        except Exception as exc:  # noqa: BLE001 - collection failures must be persisted.
            job_item.status = "failed"
            job_item.error_message = str(exc)
            errors.append(f"page {page}: {exc}")
        finally:
            job_item.finished_at = datetime.utcnow()
            job.total_fetched_count += job_item.fetched_count
            job.new_count += job_item.new_count
            job.duplicate_count += job_item.duplicate_count
            job.excluded_count += job_item.excluded_count

        if total_processed >= payload.max_items:
            break

    job.finished_at = datetime.utcnow()
    if errors and job.new_count == 0 and job.duplicate_count == 0:
        job.status = "failed"
    elif errors:
        job.status = "partial_success"
    else:
        job.status = "success"
    job.error_message = "\n".join(errors) if errors else None
    db.commit()
    db.refresh(job)
    return repository.get_collect_job(db, job.id) or job


def get_news_list(
    db: Session,
    keyword: str | None = None,
    stock_code: str | None = None,
    market_scope: str | None = None,
    event_type: str | None = None,
    filter_status: str | None = None,
    min_importance_score: int | None = None,
    is_alert_target: bool | None = None,
    is_gpt_summary_target: bool | None = None,
    gpt_summary_status: str | None = None,
    gpt_filter_result: str | None = None,
    published_from: datetime | None = None,
    published_to: datetime | None = None,
):
    return repository.list_news(
        db=db,
        keyword=keyword,
        stock_code=stock_code,
        market_scope=market_scope,
        event_type=event_type,
        filter_status=filter_status,
        min_importance_score=min_importance_score,
        is_alert_target=is_alert_target,
        is_gpt_summary_target=is_gpt_summary_target,
        gpt_summary_status=gpt_summary_status,
        gpt_filter_result=gpt_filter_result,
        published_from=published_from,
        published_to=published_to,
    )


def get_news_detail(db: Session, news_id: int) -> News:
    news = repository.get_news(db, news_id)
    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return news


def get_news_summary(db: Session) -> NewsSummary:
    total, today, linked, gpt_target, alert_target, avg_score = repository.summary_counts(db)
    return NewsSummary(
        total_news_count=total,
        today_news_count=today,
        linked_stock_news_count=linked,
        gpt_summary_target_count=gpt_target,
        alert_target_count=alert_target,
        avg_importance_score=round(avg_score, 2),
    )


def get_collect_jobs(db: Session):
    return repository.list_collect_jobs(db)


def get_collect_job_detail(db: Session, job_id: int) -> NewsCollectJob:
    job = repository.get_collect_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="News collect job not found")
    return job


def _related_stock_names(news: News) -> list[str]:
    return [link.stock_name for link in news.stock_links if link.stock_name]


def _review_item(news: News) -> NewsReviewItem:
    return NewsReviewItem(
        news_id=news.id,
        title=news.title,
        source=news.source,
        published_at=news.published_at,
        related_stocks=_related_stock_names(news),
        importance_score=news.importance_score,
        duplicate_count=news.duplicate_count,
        source_count=news.source_count,
        gpt_summary=news.gpt_summary,
        gpt_filter_result=news.gpt_filter_result,
        gpt_filter_reason=news.gpt_filter_reason,
        is_alert_target=news.is_alert_target,
        filter_status=news.filter_status,
    )


def _alert_item(news: News) -> AlertCandidateItem:
    return AlertCandidateItem(
        news_id=news.id,
        title=news.title,
        source=news.source,
        published_at=news.published_at,
        related_stocks=_related_stock_names(news),
        importance_score=news.importance_score,
        duplicate_count=news.duplicate_count,
        source_count=news.source_count,
        gpt_filter_result=news.gpt_filter_result,
        gpt_filter_reason=news.gpt_filter_reason,
        is_alert_target=news.is_alert_target,
    )


def _news_prompt(news: News, task: str) -> str:
    related_stocks = ", ".join(_related_stock_names(news)) or "-"
    return f"""작업: {task}

뉴스 정보:
- 제목: {news.title}
- 출처: {news.source or "-"}
- 발행시각: {news.published_at or "-"}
- 원문 요약: {news.original_summary or "-"}
- preview: {news.content_preview or "-"}
- 매칭 키워드: {", ".join(news.matched_keywords_json or []) or "-"}
- 관련 종목: {related_stocks}
- 중요도: {news.importance_score}
- 중복 횟수: {news.duplicate_count}
- 출처 수: {news.source_count}
- 이벤트 유형: {news.event_type or "-"}
- 시장 범위: {news.market_scope or "-"}
"""


def _summary_model() -> str:
    if not settings.openai_news_summary_model:
        raise HTTPException(status_code=400, detail="OPENAI_NEWS_SUMMARY_MODEL is not configured")
    return settings.openai_news_summary_model


def _filter_model() -> str:
    if not settings.openai_news_filter_model:
        raise HTTPException(status_code=400, detail="OPENAI_NEWS_FILTER_MODEL is not configured")
    return settings.openai_news_filter_model


def _openai_client() -> OpenAiNewsClient:
    if not settings.openai_api_key:
        raise HTTPException(status_code=400, detail="OPENAI_API_KEY is not configured")
    return OpenAiNewsClient(api_key=settings.openai_api_key)


def _validate_filter_result(value: str | None) -> None:
    if value is not None and value not in {"important", "price_impact", "unnecessary", "failed"}:
        raise HTTPException(status_code=400, detail="gpt_filter_result must be important, price_impact, unnecessary, or failed")


def run_gpt_summary(db: Session, payload: GptRunRequest) -> GptRunResult:
    targets = repository.list_summary_targets(db, payload.limit)
    model = settings.openai_news_summary_model or None
    if payload.dry_run:
        return GptRunResult(
            dry_run=True,
            processed_count=0,
            target_count=len(targets),
            model=model,
            items=[GptRunItem(id=news.id, title=news.title, status=news.gpt_summary_status or "pending") for news in targets],
        )

    client = _openai_client()
    model = _summary_model()
    items: list[GptRunItem] = []
    processed_count = 0
    for news in targets:
        try:
            prompt = _news_prompt(
                news,
                "투자 분석용으로 핵심 사실, 관련 종목 영향, 확인 필요 사항을 한국어 3~5문장으로 요약하세요.",
            )
            result = client.create_text_response(model=model, prompt=prompt)
            news.gpt_summary = result.text
            news.gpt_summary_model = result.model
            news.gpt_summary_status = "done"
            news.gpt_summary_at = datetime.utcnow()
            items.append(GptRunItem(id=news.id, title=news.title, status="done", result=result.text))
            processed_count += 1
        except Exception as exc:  # noqa: BLE001 - persist per-news GPT failure.
            news.gpt_summary_status = "failed"
            items.append(GptRunItem(id=news.id, title=news.title, status="failed", reason=str(exc)))
    db.commit()
    return GptRunResult(dry_run=False, processed_count=processed_count, target_count=len(targets), model=model, items=items)


def _parse_filter_result(text: str) -> tuple[str, str]:
    lowered = text.lower()
    for result in ("important", "price_impact", "unnecessary"):
        if result in lowered:
            return result, text.strip()
    return "unnecessary", text.strip()


def run_gpt_filter(db: Session, payload: GptRunRequest) -> GptRunResult:
    targets = repository.list_filter_targets(db, payload.limit)
    model = settings.openai_news_filter_model or None
    if payload.dry_run:
        return GptRunResult(
            dry_run=True,
            processed_count=0,
            target_count=len(targets),
            model=model,
            items=[GptRunItem(id=news.id, title=news.title, status=news.gpt_filter_result or "pending") for news in targets],
        )

    client = _openai_client()
    model = _filter_model()
    items: list[GptRunItem] = []
    processed_count = 0
    for news in targets:
        try:
            prompt = _news_prompt(
                news,
                "뉴스를 important, price_impact, unnecessary 중 하나로 분류하고 이유를 한국어 한 문단으로 작성하세요. 첫 줄에는 반드시 분류값만 쓰세요.",
            )
            if news.gpt_summary:
                prompt += f"\nGPT 요약:\n{news.gpt_summary}\n"
            result = client.create_text_response(model=model, prompt=prompt)
            filter_result, reason = _parse_filter_result(result.text)
            news.gpt_filter_result = filter_result
            news.gpt_filter_reason = reason
            news.gpt_filter_model = result.model
            news.gpt_filter_at = datetime.utcnow()
            items.append(GptRunItem(id=news.id, title=news.title, status="done", result=filter_result, reason=reason))
            processed_count += 1
        except Exception as exc:  # noqa: BLE001 - persist per-news GPT failure.
            news.gpt_filter_result = "failed"
            news.gpt_filter_reason = str(exc)
            items.append(GptRunItem(id=news.id, title=news.title, status="failed", reason=str(exc)))
    db.commit()
    return GptRunResult(dry_run=False, processed_count=processed_count, target_count=len(targets), model=model, items=items)


def get_gpt_targets(db: Session) -> GptTargetsSummary:
    summary_pending, summary_done, summary_failed, filter_pending, filter_done, filter_failed = repository.gpt_targets_counts(db)
    return GptTargetsSummary(
        summary_pending_count=summary_pending,
        summary_done_count=summary_done,
        summary_failed_count=summary_failed,
        filter_pending_count=filter_pending,
        filter_done_count=filter_done,
        filter_failed_count=filter_failed,
    )


def get_gpt_status(db: Session) -> GptStatusSummary:
    total, summary_target, summary_done, filter_done, important, price_impact, unnecessary = repository.gpt_status_counts(db)
    return GptStatusSummary(
        total_news_count=total,
        gpt_summary_target_count=summary_target,
        gpt_summary_done_count=summary_done,
        gpt_filter_done_count=filter_done,
        important_count=important,
        price_impact_count=price_impact,
        unnecessary_count=unnecessary,
    )


def get_gpt_review_list(
    db: Session,
    gpt_summary_status: str | None = None,
    gpt_filter_result: str | None = None,
    min_importance_score: int | None = None,
    stock_code: str | None = None,
    keyword: str | None = None,
    published_from: datetime | None = None,
    published_to: datetime | None = None,
) -> list[NewsReviewItem]:
    rows = repository.list_review_news(
        db=db,
        gpt_summary_status=gpt_summary_status,
        gpt_filter_result=gpt_filter_result,
        min_importance_score=min_importance_score,
        stock_code=stock_code,
        keyword=keyword,
        published_from=published_from,
        published_to=published_to,
    )
    return [_review_item(news) for news in rows]


def update_gpt_review(db: Session, news_id: int, payload: NewsReviewUpdate) -> NewsReviewItem:
    _validate_filter_result(payload.gpt_filter_result)
    news = get_news_detail(db, news_id)
    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(news, key, value)
    news.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(news)
    return _review_item(news)


def _is_attention_news(news: News, attention_stock_ids: set[int]) -> bool:
    return any(link.stock_id in attention_stock_ids for link in news.stock_links if link.stock_id is not None)


def _is_alert_candidate(news: News, alert_setting, attention_stock_ids: set[int]) -> bool:
    event_types = set(alert_setting.event_types_json or [])
    base_match = (
        news.importance_score >= alert_setting.min_importance_score
        or news.duplicate_count >= alert_setting.min_duplicate_count
        or news.source_count >= alert_setting.min_source_count
        or news.gpt_filter_result in {"important", "price_impact"}
        or (news.event_type in event_types if event_types else False)
    )
    return bool(base_match or _is_attention_news(news, attention_stock_ids))


def recalculate_alert_candidates(db: Session) -> AlertCandidateRecalculateResult:
    alert_setting = repository.get_alert_setting(db)
    if alert_setting is None:
        raise HTTPException(status_code=400, detail="alert_settings is not configured")
    if not alert_setting.enabled or not alert_setting.news_alert_enabled:
        return AlertCandidateRecalculateResult(processed_count=0, alert_target_count=0, changed_count=0)

    attention_stock_ids = repository.get_attention_stock_ids(db)
    rows = repository.list_alert_candidate_news(db, only_alert_targets=False, limit=None)
    processed_count = 0
    alert_target_count = 0
    changed_count = 0
    for news in rows:
        target = _is_alert_candidate(news, alert_setting, attention_stock_ids)
        processed_count += 1
        if target:
            alert_target_count += 1
        if news.is_alert_target != target:
            news.is_alert_target = target
            news.updated_at = datetime.utcnow()
            changed_count += 1
    db.commit()
    return AlertCandidateRecalculateResult(
        processed_count=processed_count,
        alert_target_count=alert_target_count,
        changed_count=changed_count,
    )


def get_alert_candidates(
    db: Session,
    stock_code: str | None = None,
    gpt_filter_result: str | None = None,
    min_importance_score: int | None = None,
    published_from: datetime | None = None,
    published_to: datetime | None = None,
) -> list[AlertCandidateItem]:
    rows = repository.list_alert_candidate_news(
        db=db,
        stock_code=stock_code,
        gpt_filter_result=gpt_filter_result,
        min_importance_score=min_importance_score,
        published_from=published_from,
        published_to=published_to,
        only_alert_targets=True,
    )
    return [_alert_item(news) for news in rows]


def get_alert_summary(db: Session) -> AlertCandidateSummary:
    alert_target, important, price_impact, high_importance = repository.alert_summary_counts(db)
    return AlertCandidateSummary(
        alert_target_count=alert_target,
        important_count=important,
        price_impact_count=price_impact,
        high_importance_count=high_importance,
    )
