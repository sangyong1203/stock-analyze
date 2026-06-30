from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Tag, TagLink
from app.domains.tags import repository
from app.domains.tags.schemas import TAG_TARGET_TYPES, TagCreate, TagLinkCreate, TagLinkRead, TagRead, TagUpdate


def _normalize_target_type(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in TAG_TARGET_TYPES:
        raise HTTPException(status_code=400, detail=f"target_type must be one of: {', '.join(TAG_TARGET_TYPES)}")
    return normalized


def _validate_target(db: Session, target_type: str, target_id: int) -> None:
    getters = {
        "stock": repository.get_stock,
        "trade": repository.get_trade,
        "news": repository.get_news,
        "memo": repository.get_memo,
    }
    if getters[target_type](db, target_id) is None:
        raise HTTPException(status_code=404, detail=f"{target_type} not found")


def _serialize_link(row: tuple[TagLink, str, str | None, str]) -> TagLinkRead:
    link, tag_name, tag_color, tag_type = row
    return TagLinkRead(
        id=link.id,
        tag_id=link.tag_id,
        target_type=link.target_type,
        target_id=link.target_id,
        created_at=link.created_at,
        tag_name=tag_name,
        tag_color=tag_color,
        tag_type=tag_type,
    )


def list_tags(db: Session, tag_type: str | None = None):
    return [TagRead.model_validate(row) for row in repository.list_tags(db, tag_type=tag_type)]


def create_tag(db: Session, payload: TagCreate):
    if repository.get_tag_by_name_type(db, payload.name.strip(), payload.tag_type.strip()):
        raise HTTPException(status_code=409, detail="tag already exists")
    tag = Tag(name=payload.name.strip(), color=payload.color, tag_type=payload.tag_type.strip())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return TagRead.model_validate(tag)


def update_tag(db: Session, tag_id: int, payload: TagUpdate):
    tag = repository.get_tag(db, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="tag not found")
    updates = payload.model_dump(exclude_unset=True)
    target_name = updates.get("name", tag.name)
    target_type = updates.get("tag_type", tag.tag_type)
    existing = repository.get_tag_by_name_type(db, target_name.strip(), target_type.strip())
    if existing is not None and existing.id != tag_id:
        raise HTTPException(status_code=409, detail="tag already exists")
    for key, value in updates.items():
        if isinstance(value, str):
            value = value.strip()
        setattr(tag, key, value)
    db.commit()
    db.refresh(tag)
    return TagRead.model_validate(tag)


def delete_tag(db: Session, tag_id: int) -> dict[str, int]:
    tag = repository.get_tag(db, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="tag not found")
    for link in repository.list_links_by_tag(db, tag_id):
        db.delete(link)
    db.delete(tag)
    db.commit()
    return {"deleted_tag_id": tag_id}


def list_tag_links(db: Session, target_type: str | None = None, target_id: int | None = None):
    normalized_target_type = _normalize_target_type(target_type) if target_type else None
    return [_serialize_link(row) for row in repository.list_tag_links(db, target_type=normalized_target_type, target_id=target_id)]


def create_tag_link(db: Session, payload: TagLinkCreate):
    tag = repository.get_tag(db, payload.tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="tag not found")
    target_type = _normalize_target_type(payload.target_type)
    _validate_target(db, target_type, payload.target_id)
    existing = repository.get_tag_link(db, payload.tag_id, target_type, payload.target_id)
    if existing is not None:
        raise HTTPException(status_code=409, detail="tag link already exists")
    link = TagLink(tag_id=payload.tag_id, target_type=target_type, target_id=payload.target_id)
    db.add(link)
    db.commit()
    return _serialize_link((link, tag.name, tag.color, tag.tag_type))


def delete_tag_link(db: Session, tag_id: int, target_type: str, target_id: int) -> dict[str, int | str]:
    normalized_target_type = _normalize_target_type(target_type)
    link = repository.get_tag_link(db, tag_id, normalized_target_type, target_id)
    if link is None:
        raise HTTPException(status_code=404, detail="tag link not found")
    db.delete(link)
    db.commit()
    return {"deleted_tag_id": tag_id, "target_type": normalized_target_type, "target_id": target_id}
