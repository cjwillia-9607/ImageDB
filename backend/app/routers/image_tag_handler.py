from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.storage.db import get_db
from app.repositories.image_tag_db import create_image_tag, get_tags_by_image_id, get_images_by_tag_id, get_image_tags_by_img, get_image_tags_by_tag, remove_image_tag
from app.repositories.tag_db import get_tag_by_name, create_tag
from app.models.image_tag import ImageTag as ImageTagModel
from app.routers.tag_handler import TagRead
from app.routers.image_handler import ImageRead
from pydantic import BaseModel
# Pydantic model for creating an image tag association
class ImageTagCreate(BaseModel):
    image_id: int
    tag_name: str

# Pydantic model for reading an image tag association
class ImageTagRead(BaseModel):
    image_id: int
    tag_id: int

    class Config:
        from_attributes = True

router = APIRouter()

@router.post("/image_tags/", response_model=ImageTagRead)
def create_new_image_tag(image_tag: ImageTagCreate, db: Session = Depends(get_db)):
    # Ensure the tag exists, create if it does not
    db_tag = get_tag_by_name(db, name=image_tag.tag_name)
    if not db_tag:
        db_tag = create_tag(db, name=image_tag.tag_name)
    
    db_image_tag = create_image_tag(db, image_id=image_tag.image_id, tag_id=db_tag.id)
    return db_image_tag

@router.get("/images/{image_id}/tags", response_model=List[TagRead])
def read_tags_by_image(image_id: int, db: Session = Depends(get_db)):
    tags = get_tags_by_image_id(db, image_id)
    return tags

@router.get("/tags/{tag_id}/images", response_model=List[ImageRead])
def read_images_by_tag(tag_id: int, db: Session = Depends(get_db)):
    images = get_images_by_tag_id(db, tag_id)
    return images

@router.get("/image_tags/image/{image_id}", response_model=List[ImageTagRead])
def read_image_tags(image_id: int, db: Session = Depends(get_db)):
    image_tags = get_image_tags_by_img(db, image_id=image_id)
    return image_tags

@router.get("/image_tags/tag/{tag_id}", response_model=List[ImageTagRead])
def read_image_tags(tag_id: int, db: Session = Depends(get_db)):
    image_tags = get_image_tags_by_tag(db, tag_id=tag_id)
    return image_tags

@router.delete("/image_tags/{image_id}/{tag_id}", response_model=ImageTagRead)
def delete_image_tag(image_id: int, tag_id: int, db: Session = Depends(get_db)):
    db_image_tag = remove_image_tag(db, image_id=image_id, tag_id=tag_id)
    if db_image_tag is None:
        raise HTTPException(status_code=404, detail="Image-Tag association not found")
    return db_image_tag