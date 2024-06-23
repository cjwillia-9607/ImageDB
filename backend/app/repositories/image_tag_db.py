from sqlalchemy.orm import Session
from app.models.image_tag import ImageTag

def create_image_tag(db: Session, image_id: int, tag_id: int):
    new_image_tag = ImageTag(image_id=image_id, tag_id=tag_id)
    db.add(new_image_tag)
    db.commit()
    return new_image_tag

def get_image_tags(db: Session, image_id: int):
    return db.query(ImageTag).filter(ImageTag.image_id == image_id).all()

def delete_image_tag(db: Session, image_id: int, tag_id: int):
    image_tag = db.query(ImageTag).filter(ImageTag.image_id == image_id, ImageTag.tag_id == tag_id).first()
    if image_tag:
        db.delete(image_tag)
        db.commit()
    return image_tag