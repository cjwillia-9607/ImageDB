from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.storage.db import get_db
from app.repositories.tag_db import get_tag, create_tag, get_tags, delete_tag, get_tag_by_name, search_tags_by_name
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

@router.get("/tags/{tag_id}", response_model=TagRead)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@router.post("/tags/", response_model=TagRead)
def create_new_tag(tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = get_tag_by_name(db, name=tag.name)
    if db_tag:
        raise HTTPException(status_code=400, detail="Tag already exists")
    db_tag = create_tag(db, name=tag.name)
    return db_tag

@router.get("/tags/", response_model=List[TagRead])
def read_tags(skip: int = 0, limit: int = 10, tag_id: int = 0, name: str = Query(None), db: Session = Depends(get_db)):
    if name:
        tags = search_tags_by_name(db, name=name, skip=skip, limit=limit)
    elif tag_id:
        tags = [get_tag(db, tag_id)]
    else:
        tags = get_tags(db, skip=skip, limit=limit)
    return tags

@router.delete("/tags/{tag_id}", response_model=TagRead)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = delete_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

