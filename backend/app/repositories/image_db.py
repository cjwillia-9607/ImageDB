from sqlalchemy.orm import Session
from app.models.image import Image

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