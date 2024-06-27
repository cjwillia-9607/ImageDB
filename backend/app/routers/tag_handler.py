from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.storage.db import get_db
from app.repositories.tag_db import get_tag, create_tag, get_tags, remove_tag, get_tag_by_name, search_tags_by_name
from app.models.tag import Tag as TagModel
from pydantic import BaseModel

# Pydantic model for creating a tag
class TagCreate(BaseModel):
    name: str

# Pydantic model for reading a tag (used for serialization)
class TagRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

router = APIRouter()

@router.post("/tags/", response_model=TagRead)
def create_new_tag(tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = get_tag_by_name(db, name=tag.name)
    if db_tag:
        return db_tag
    db_tag = create_tag(db, name=tag.name)
    return db_tag

@router.get("/tags/all/", response_model=List[TagRead])
def get_all_tags(db:Session, skip: int = 0, limit: int = 1000):
    db_tags = get_tags(db, skip=skip, limit=limit)
    return db_tags

@router.get("/tags/id/{tag_id}", response_model=TagRead)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@router.get("/tags/name/{name}", response_model=TagRead)
def read_tags(name: str, db: Session = Depends(get_db)):
    tags = get_tag_by_name(db, name)
    if tags is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tags

@router.delete("/tags/{tag_id}", response_model=TagRead)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = remove_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag