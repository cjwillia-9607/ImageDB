from sqlalchemy.orm import Session
from app.models.image import Image
from app.models.image_tag import ImageTag
from sqlalchemy import func
from typing import List

def get_image(db: Session, image_id: int):
    return db.query(Image).filter(Image.id == image_id).first()

def create_image(db: Session, title: str, description: str, url: str):
    new_image = Image(title=title, description=description, url=url)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

def get_images(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Image).offset(skip).limit(limit).all()

def delete_image(db: Session, image_id: int):
    image = db.query(Image).filter(Image.id == image_id).first()
    if image:
        db.delete(image)
        db.commit()
    return image

def get_images_by_title(db: Session, title: str):
    return db.query(Image).filter(Image.title == title).all()

def get_images_by_tags(db: Session, tag_ids: List[int]) -> List[Image]:
    # Ensure there are tag_ids to search for
    if not tag_ids:
        return []

    # Count the number of tag_ids
    tag_count = len(tag_ids)

    # Join Image and ImageTag, filter by tag_ids, group by Image.id, and having count of tags equal to tag_count
    images = db.query(Image).join(ImageTag).filter(ImageTag.tag_id.in_(tag_ids)).group_by(Image.id).having(func.count(Image.id) == tag_count).all()
    return images