from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import AlertHistory, PriceAlert, Stock
from app.domains.alerts import repository
from app.domains.alerts.schemas import (
    PRICE_ALERT_TYPES,
    AlertHistoryRead,
    PriceAlertCreate,
    PriceAlertEvaluationItem,
    PriceAlertEvaluationRequest,
    PriceAlertEvaluationResult,
    PriceAlertRead,
    PriceAlertSummary,
    PriceAlertUpdate,
)
from app.external.gmail import GmailMessage, GmailSmtpClient

DEFAULT_LOOKBACK_DAYS = 60
RANGE_ALERT_TYPES = {"DROP_FROM_HIGH", "RISE_FROM_LOW"}


def _normalize_alert_type(alert_type: str) -> str:
    value = alert_type.strip().upper()
    if value not in PRICE_ALERT_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported alert_type: {alert_type}")
    return value


def _validate_stock(db: Session, stock_id: int) -> Stock:
    stock = repository.get_stock(db, stock_id)
    if stock is None:
        raise HTTPException(status_code=404, detail="stock not found")
    return stock


def _lookback_days_from_model(alert: PriceAlert) -> int:
    return DEFAULT_LOOKBACK_DAYS


def _serialize_price_alert(alert: PriceAlert, stock: Stock) -> PriceAlertRead:
    return PriceAlertRead(
        id=alert.id,
        stock_id=alert.stock_id,
        stock_code=stock.code,
        stock_name=stock.name,
        current_price=stock.current_price,
        alert_type=alert.alert_type,
        target_price=alert.target_price,
        threshold_percent=alert.threshold_rate,
        lookback_days=_lookback_days_from_model(alert),
        is_enabled=alert.enabled,
        triggered=alert.triggered,
        triggered_at=alert.triggered_at,
        memo=alert.memo,
        created_at=alert.created_at,
        updated_at=alert.updated_at,
    )


def _apply_payload(alert: PriceAlert, payload: PriceAlertCreate | PriceAlertUpdate) -> None:
    updates = payload.model_dump(exclude_unset=True)
    if "alert_type" in updates:
        updates["alert_type"] = _normalize_alert_type(updates["alert_type"])
    if "stock_id" in updates:
        alert.stock_id = updates["stock_id"]
    if "alert_type" in updates:
        alert.alert_type = updates["alert_type"]
    if "target_price" in updates:
        alert.target_price = updates["target_price"]
    if "threshold_percent" in updates:
        alert.threshold_rate = updates["threshold_percent"]
    if "is_enabled" in updates:
        alert.enabled = updates["is_enabled"]
    if "memo" in updates:
        alert.memo = updates["memo"]
    alert.base_price = None
    alert.direction = "above" if alert.alert_type in {"TARGET_PRICE_ABOVE", "RISE_FROM_LOW"} else "below"
    if alert.alert_type in RANGE_ALERT_TYPES and alert.threshold_rate is None:
        raise HTTPException(status_code=400, detail="threshold_percent is required for range-based alerts")
    if alert.alert_type in {"TARGET_PRICE_ABOVE", "TARGET_PRICE_BELOW"} and alert.target_price is None:
        raise HTTPException(status_code=400, detail="target_price is required for target price alerts")
    if alert.alert_type in RANGE_ALERT_TYPES:
        alert.target_price = None
    else:
        alert.threshold_rate = None


def get_price_alerts(db: Session, stock_id: int | None = None, enabled: bool | None = None):
    rows = repository.list_price_alerts(db, stock_id=stock_id, enabled=enabled)
    return [_serialize_price_alert(alert, stock) for alert, stock in rows]


def get_price_alert_detail(db: Session, alert_id: int):
    row = repository.get_price_alert(db, alert_id)
    if row is None:
        raise HTTPException(status_code=404, detail="price alert not found")
    alert, stock = row
    return _serialize_price_alert(alert, stock)


def create_price_alert(db: Session, payload: PriceAlertCreate):
    _validate_stock(db, payload.stock_id)
    alert = PriceAlert(
        stock_id=payload.stock_id,
        alert_type=_normalize_alert_type(payload.alert_type),
        enabled=payload.is_enabled,
        base_price=None,
    )
    _apply_payload(alert, payload)
    db.add(alert)
    db.commit()
    return get_price_alert_detail(db, alert.id)


def update_price_alert(db: Session, alert_id: int, payload: PriceAlertUpdate):
    alert = repository.get_price_alert_model(db, alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="price alert not found")
    if payload.stock_id is not None:
        _validate_stock(db, payload.stock_id)
    _apply_payload(alert, payload)
    db.commit()
    return get_price_alert_detail(db, alert.id)


def delete_price_alert(db: Session, alert_id: int):
    alert = repository.get_price_alert_model(db, alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="price alert not found")
    db.delete(alert)
    db.commit()


def _current_price(stock: Stock, latest_close: Decimal | None) -> Decimal | None:
    return stock.current_price if stock.current_price is not None else latest_close


def _trigger_price_and_match(
    alert: PriceAlert,
    current_price: Decimal | None,
    recent_high: Decimal | None,
    recent_low: Decimal | None,
) -> tuple[Decimal | None, bool, str | None]:
    if current_price is None:
        return None, False, "missing_current_price"
    if alert.alert_type == "TARGET_PRICE_ABOVE":
        if alert.target_price is None:
            return None, False, "missing_target_price"
        return alert.target_price, current_price >= alert.target_price, None
    if alert.alert_type == "TARGET_PRICE_BELOW":
        if alert.target_price is None:
            return None, False, "missing_target_price"
        return alert.target_price, current_price <= alert.target_price, None
    if alert.alert_type == "DROP_FROM_HIGH":
        if recent_high is None or alert.threshold_rate is None:
            return None, False, "missing_range_data"
        trigger_price = recent_high * (Decimal("1") - (alert.threshold_rate / Decimal("100")))
        return trigger_price, current_price <= trigger_price, None
    if alert.alert_type == "RISE_FROM_LOW":
        if recent_low is None or alert.threshold_rate is None:
            return None, False, "missing_range_data"
        trigger_price = recent_low * (Decimal("1") + (alert.threshold_rate / Decimal("100")))
        return trigger_price, current_price >= trigger_price, None
    return None, False, "unsupported_alert_type"


def _validate_gmail_settings() -> tuple[str, str, str]:
    username = settings.gmail_smtp_username
    password = settings.gmail_smtp_app_password
    recipient = settings.alert_recipient_email
    missing = []
    if not settings.gmail_smtp_host:
        missing.append("GMAIL_SMTP_HOST")
    if not settings.gmail_smtp_port:
        missing.append("GMAIL_SMTP_PORT")
    if not username:
        missing.append("GMAIL_SMTP_USERNAME")
    if not password:
        missing.append("GMAIL_SMTP_APP_PASSWORD")
    if not recipient:
        missing.append("ALERT_RECIPIENT_EMAIL")
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing Gmail SMTP settings: {', '.join(missing)}")
    return username, password, recipient


def _alert_subject(stock: Stock, alert: PriceAlert) -> str:
    return f"[Price Alert] {stock.name} {alert.alert_type}"[:255]


def _alert_body(
    stock: Stock,
    alert: PriceAlert,
    current_price: Decimal | None,
    trigger_price: Decimal | None,
    recent_high: Decimal | None,
    recent_low: Decimal | None,
) -> str:
    return "\n".join(
        [
            f"stock: {stock.name} ({stock.code})",
            f"alert_type: {alert.alert_type}",
            f"current_price: {current_price if current_price is not None else '-'}",
            f"target_price: {alert.target_price if alert.target_price is not None else '-'}",
            f"threshold_percent: {alert.threshold_rate if alert.threshold_rate is not None else '-'}",
            f"lookback_days: {_lookback_days_from_model(alert)}",
            f"recent_high: {recent_high if recent_high is not None else '-'}",
            f"recent_low: {recent_low if recent_low is not None else '-'}",
            f"trigger_price: {trigger_price if trigger_price is not None else '-'}",
            f"memo: {alert.memo or '-'}",
        ]
    )


def _record_history(
    db: Session,
    *,
    alert: PriceAlert,
    stock: Stock,
    status: str,
    title: str,
    message: str,
    recipient: str | None = None,
    error_message: str | None = None,
) -> AlertHistory:
    history = AlertHistory(
        stock_id=stock.id,
        price_alert_id=alert.id,
        alert_type="price",
        recipient_email=recipient,
        title=title[:255],
        message=message,
        link_url=None,
        status=status,
        sent_at=datetime.utcnow() if status == "sent" else None,
        error_message=error_message,
    )
    db.add(history)
    db.flush()
    return history


def _history_item(
    alert: PriceAlert,
    stock: Stock,
    *,
    current_price: Decimal | None,
    recent_high: Decimal | None,
    recent_low: Decimal | None,
    trigger_price: Decimal | None,
    latest_price_date: datetime | None,
    matched: bool,
    status: str,
    skip_reason: str | None = None,
    recipient_email: str | None = None,
    subject: str | None = None,
    reason: str | None = None,
) -> PriceAlertEvaluationItem:
    return PriceAlertEvaluationItem(
        price_alert_id=alert.id,
        stock_id=stock.id,
        stock_code=stock.code,
        stock_name=stock.name,
        alert_type=alert.alert_type,
        current_price=current_price,
        target_price=alert.target_price,
        threshold_percent=alert.threshold_rate,
        lookback_days=_lookback_days_from_model(alert),
        recent_high=recent_high,
        recent_low=recent_low,
        trigger_price=trigger_price,
        latest_price_date=latest_price_date,
        matched=matched,
        status=status,
        skip_reason=skip_reason,
        recipient_email=recipient_email,
        subject=subject,
        reason=reason,
    )


def _evaluate_alert(
    db: Session,
    alert: PriceAlert,
    stock: Stock,
    *,
    force: bool,
    recipient_email: str | None,
    sent_so_far: int,
    daily_sent_count: int,
    hourly_sent_count: int,
    max_daily_alerts: int,
    max_hourly_alerts: int,
    evaluate_now: bool,
    alerts_enabled: bool,
    price_alert_enabled: bool,
    send_email_enabled: bool,
) -> PriceAlertEvaluationItem:
    latest_row = repository.get_latest_price_row(db, stock.id)
    latest_date = latest_row.date if latest_row is not None else None
    latest_close = latest_row.close if latest_row is not None else None
    current_price = _current_price(stock, latest_close)
    recent_high = None
    recent_low = None
    latest_price_date = None
    if latest_date is not None:
        recent_high, recent_low, latest_seen_date = repository.get_price_range_stats(
            db,
            stock.id,
            latest_date,
            _lookback_days_from_model(alert),
        )
        if latest_seen_date is not None:
            latest_price_date = datetime.combine(latest_seen_date, datetime.min.time())
    trigger_price, matched, calc_reason = _trigger_price_and_match(alert, current_price, recent_high, recent_low)
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    if not alert.enabled:
        return _history_item(
            alert,
            stock,
            current_price=current_price,
            recent_high=recent_high,
            recent_low=recent_low,
            trigger_price=trigger_price,
            latest_price_date=latest_price_date,
            matched=False,
            status="skipped",
            skip_reason="disabled",
        )
    if not alerts_enabled:
        return _history_item(
            alert,
            stock,
            current_price=current_price,
            recent_high=recent_high,
            recent_low=recent_low,
            trigger_price=trigger_price,
            latest_price_date=latest_price_date,
            matched=False,
            status="skipped",
            skip_reason="alerts_disabled",
        )
    if not price_alert_enabled:
        return _history_item(
            alert,
            stock,
            current_price=current_price,
            recent_high=recent_high,
            recent_low=recent_low,
            trigger_price=trigger_price,
            latest_price_date=latest_price_date,
            matched=False,
            status="skipped",
            skip_reason="price_alert_disabled",
        )
    if evaluate_now and not send_email_enabled:
        return _history_item(
            alert,
            stock,
            current_price=current_price,
            recent_high=recent_high,
            recent_low=recent_low,
            trigger_price=trigger_price,
            latest_price_date=latest_price_date,
            matched=False,
            status="skipped",
            skip_reason="email_disabled",
        )
    if calc_reason is not None:
        return _history_item(
            alert,
            stock,
            current_price=current_price,
            recent_high=recent_high,
            recent_low=recent_low,
            trigger_price=trigger_price,
            latest_price_date=latest_price_date,
            matched=False,
            status="skipped",
            skip_reason=calc_reason,
        )
    if not matched:
        return _history_item(
            alert,
            stock,
            current_price=current_price,
            recent_high=recent_high,
            recent_low=recent_low,
            trigger_price=trigger_price,
            latest_price_date=latest_price_date,
            matched=False,
            status="skipped",
            skip_reason="condition_not_met",
        )
    if repository.get_sent_history_today(db, alert.id, stock.id, today_start):
        return _history_item(
            alert,
            stock,
            current_price=current_price,
            recent_high=recent_high,
            recent_low=recent_low,
            trigger_price=trigger_price,
            latest_price_date=latest_price_date,
            matched=True,
            status="skipped",
            skip_reason="already_sent_today",
        )
    if not force and repository.get_failed_history_today(db, alert.id, stock.id, today_start):
        return _history_item(
            alert,
            stock,
            current_price=current_price,
            recent_high=recent_high,
            recent_low=recent_low,
            trigger_price=trigger_price,
            latest_price_date=latest_price_date,
            matched=True,
            status="skipped",
            skip_reason="failed_exists_today",
        )
    if daily_sent_count + sent_so_far >= max_daily_alerts:
        return _history_item(
            alert,
            stock,
            current_price=current_price,
            recent_high=recent_high,
            recent_low=recent_low,
            trigger_price=trigger_price,
            latest_price_date=latest_price_date,
            matched=True,
            status="skipped",
            skip_reason="daily_limit",
        )
    if hourly_sent_count + sent_so_far >= max_hourly_alerts:
        return _history_item(
            alert,
            stock,
            current_price=current_price,
            recent_high=recent_high,
            recent_low=recent_low,
            trigger_price=trigger_price,
            latest_price_date=latest_price_date,
            matched=True,
            status="skipped",
            skip_reason="hourly_limit",
        )
    return _history_item(
        alert,
        stock,
        current_price=current_price,
        recent_high=recent_high,
        recent_low=recent_low,
        trigger_price=trigger_price,
        latest_price_date=latest_price_date,
        matched=True,
        status="pending" if evaluate_now else "would_send",
        recipient_email=recipient_email,
        subject=_alert_subject(stock, alert),
    )


def _build_result(
    items: list[PriceAlertEvaluationItem],
    *,
    sent_count: int,
    failed_count: int,
    daily_sent_count: int,
    hourly_sent_count: int,
) -> PriceAlertEvaluationResult:
    skipped_reasons: dict[str, int] = {}
    matched_count = 0
    sendable_count = 0
    for item in items:
        if item.matched:
            matched_count += 1
        if item.status in {"would_send", "pending", "sent"}:
            sendable_count += 1
        if item.status == "skipped":
            reason = item.skip_reason or "skipped"
            skipped_reasons[reason] = skipped_reasons.get(reason, 0) + 1
    return PriceAlertEvaluationResult(
        evaluated_count=len(items),
        matched_count=matched_count,
        sendable_count=sendable_count,
        sent_count=sent_count,
        failed_count=failed_count,
        skipped_count=sum(skipped_reasons.values()),
        skipped_reasons=skipped_reasons,
        daily_sent_count=daily_sent_count,
        hourly_sent_count=hourly_sent_count,
        items=items,
    )


def evaluate_price_alerts_dry_run(db: Session, payload: PriceAlertEvaluationRequest):
    alert_setting = repository.get_alert_setting(db)
    if alert_setting is None:
        raise HTTPException(status_code=400, detail="alert_settings is not configured")
    rows = repository.list_evaluation_targets(db, payload.alert_ids)
    daily_sent_count = repository.count_sent_alerts_since(
        db,
        datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0),
    )
    hourly_sent_count = repository.count_sent_alerts_since(db, datetime.utcnow() - timedelta(hours=1))
    items: list[PriceAlertEvaluationItem] = []
    for alert, stock in rows[: payload.limit]:
        items.append(
            _evaluate_alert(
                db,
                alert,
                stock,
                force=payload.force,
                recipient_email=settings.alert_recipient_email or None,
                sent_so_far=sum(1 for current in items if current.status in {"would_send", "pending", "sent"}),
                daily_sent_count=daily_sent_count,
                hourly_sent_count=hourly_sent_count,
                max_daily_alerts=alert_setting.max_daily_alerts,
                max_hourly_alerts=alert_setting.max_hourly_alerts,
                evaluate_now=False,
                alerts_enabled=alert_setting.enabled,
                price_alert_enabled=alert_setting.price_alert_enabled,
                send_email_enabled=alert_setting.send_email,
            )
        )
    return _build_result(
        items,
        sent_count=0,
        failed_count=0,
        daily_sent_count=daily_sent_count,
        hourly_sent_count=hourly_sent_count,
    )


def evaluate_price_alerts(db: Session, payload: PriceAlertEvaluationRequest):
    alert_setting = repository.get_alert_setting(db)
    if alert_setting is None:
        raise HTTPException(status_code=400, detail="alert_settings is not configured")
    recipient = settings.alert_recipient_email or None
    client = None
    if alert_setting.enabled and alert_setting.price_alert_enabled and alert_setting.send_email:
        username, password, recipient = _validate_gmail_settings()
        client = GmailSmtpClient(
            host=settings.gmail_smtp_host,
            port=settings.gmail_smtp_port,
            username=username,
            app_password=password,
        )
    rows = repository.list_evaluation_targets(db, payload.alert_ids)
    daily_sent_count = repository.count_sent_alerts_since(
        db,
        datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0),
    )
    hourly_sent_count = repository.count_sent_alerts_since(db, datetime.utcnow() - timedelta(hours=1))
    items: list[PriceAlertEvaluationItem] = []
    sent_count = 0
    failed_count = 0
    for alert, stock in rows[: payload.limit]:
        item = _evaluate_alert(
            db,
            alert,
            stock,
            force=payload.force,
            recipient_email=recipient,
            sent_so_far=sent_count,
            daily_sent_count=daily_sent_count,
            hourly_sent_count=hourly_sent_count,
            max_daily_alerts=alert_setting.max_daily_alerts,
            max_hourly_alerts=alert_setting.max_hourly_alerts,
            evaluate_now=True,
            alerts_enabled=alert_setting.enabled,
            price_alert_enabled=alert_setting.price_alert_enabled,
            send_email_enabled=alert_setting.send_email,
        )
        if item.status == "pending":
            subject = item.subject or _alert_subject(stock, alert)
            body = _alert_body(stock, alert, item.current_price, item.trigger_price, item.recent_high, item.recent_low)
            try:
                if client is None:
                    raise RuntimeError("email client is unavailable")
                client.send(GmailMessage(recipient=recipient, subject=subject, body=body))
                alert.triggered = True
                alert.triggered_at = datetime.utcnow()
                _record_history(
                    db,
                    alert=alert,
                    stock=stock,
                    status="sent",
                    title=subject,
                    message=body,
                    recipient=recipient,
                )
                item.status = "sent"
                sent_count += 1
            except Exception as exc:  # noqa: BLE001
                alert.triggered = True
                alert.triggered_at = datetime.utcnow()
                _record_history(
                    db,
                    alert=alert,
                    stock=stock,
                    status="failed",
                    title=subject,
                    message=body,
                    recipient=recipient,
                    error_message=str(exc),
                )
                item.status = "failed"
                item.reason = str(exc)
                failed_count += 1
        else:
            alert.triggered = item.matched
            if item.matched:
                alert.triggered_at = datetime.utcnow()
            _record_history(
                db,
                alert=alert,
                stock=stock,
                status="skipped",
                title=_alert_subject(stock, alert),
                message=item.skip_reason or item.status,
                recipient=recipient,
                error_message=item.skip_reason,
            )
        items.append(item)
    db.commit()
    return _build_result(
        items,
        sent_count=sent_count,
        failed_count=failed_count,
        daily_sent_count=daily_sent_count,
        hourly_sent_count=hourly_sent_count,
    )


def get_price_alert_histories(db: Session, status: str | None = None):
    return [AlertHistoryRead.model_validate(row) for row in repository.list_alert_histories(db, status=status)]


def get_price_alert_summary(db: Session):
    total, enabled, disabled, triggered, sent, failed, skipped, today_sent, hourly_sent = repository.summary_counts(db)
    return PriceAlertSummary(
        total_count=total,
        enabled_count=enabled,
        disabled_count=disabled,
        triggered_count=triggered,
        sent_count=sent,
        failed_count=failed,
        skipped_count=skipped,
        today_sent_count=today_sent,
        hourly_sent_count=hourly_sent,
    )
