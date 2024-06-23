from sqlalchemy.orm import Session
from app.models.tag import Tag

def get_tag(db: Session, tag_id: int):
    return db.query(Tag).filter(Tag.id == tag_id).first()

def create_tag(db: Session, name: str):
    new_tag = Tag(name=name)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

def get_tags(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Tag).offset(skip).limit(limit).all()

def delete_tag(db: Session, tag_id: int):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag

def get_tag_by_name(db: Session, name: str):
    return db.query(Tag).filter(Tag.name == name).first()

def search_tags_by_name(db: Session, name: str, skip: int = 0, limit: int = 10):
    return db.query(Tag).filter(Tag.name.like(f"%{name}%")).offset(skip).limit(limit).all()