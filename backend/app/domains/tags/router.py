from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domains.tags.schemas import TagCreate, TagLinkCreate, TagLinkRead, TagRead, TagUpdate
from app.domains.tags.service import create_tag, create_tag_link, delete_tag, delete_tag_link, list_tag_links, list_tags, update_tag

router = APIRouter()


@router.get("", response_model=list[TagRead])
def list_items(tag_type: str | None = None, db: Session = Depends(get_db)):
    return list_tags(db, tag_type=tag_type)


@router.post("", response_model=TagRead, status_code=201)
def create_item(payload: TagCreate, db: Session = Depends(get_db)):
    return create_tag(db, payload)


@router.post("/link", response_model=TagLinkRead, status_code=201)
def create_link(payload: TagLinkCreate, db: Session = Depends(get_db)):
    return create_tag_link(db, payload)


@router.delete("/link")
def remove_link(
    tag_id: int = Query(),
    target_type: str = Query(),
    target_id: int = Query(),
    db: Session = Depends(get_db),
):
    return delete_tag_link(db, tag_id=tag_id, target_type=target_type, target_id=target_id)


@router.get("/links", response_model=list[TagLinkRead])
def list_links(target_type: str | None = None, target_id: int | None = None, db: Session = Depends(get_db)):
    return list_tag_links(db, target_type=target_type, target_id=target_id)


@router.patch("/{tag_id}", response_model=TagRead)
def update_item(tag_id: int, payload: TagUpdate, db: Session = Depends(get_db)):
    return update_tag(db, tag_id, payload)


@router.delete("/{tag_id}", status_code=204)
def delete_item(tag_id: int, db: Session = Depends(get_db)):
    delete_tag(db, tag_id)
    return Response(status_code=204)
