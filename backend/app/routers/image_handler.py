from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.storage.db import get_db
from app.repositories.image_db import get_image, create_image, get_images, delete_image, get_images_by_title
from app.models.image import Image as ImageModel
from pydantic import BaseModel
import shutil
import os

# Pydantic model for creating an image
class ImageCreate(BaseModel):
    title: str
    description: str

# Pydantic model for creating an image with URL
class ImageCreateWithUrl(BaseModel):
    title: str
    description: str
    url: str

# Pydantic model for reading an image (used for serialization)
class ImageRead(BaseModel):
    id: int
    title: str
    description: str
    url: str  # Include URL field

    class Config:
        from_attributes = True

router = APIRouter()

@router.get("/images/{image_id}", response_model=ImageRead)
def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image = get_image(db, image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@router.post("/images/", response_model=ImageRead)
def create_new_image(image: ImageCreateWithUrl, db: Session = Depends(get_db)):
    db_image = create_image(db, title=image.title, description=image.description, url=image.url)
    return db_image

@router.get("/images/", response_model=List[ImageRead])
def read_images(skip: int = 0, limit: int = 10, title: Optional[str] = Query(None), db: Session = Depends(get_db)):
    if title:
        images = get_images_by_title(db, title=title)
    else:
        images = get_images(db, skip=skip, limit=limit)
    return images

@router.delete("/images/{image_id}", response_model=ImageRead)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = delete_image(db, image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

# New endpoint to handle file uploads and store the URL in the database
@router.post("/uploadfile/", response_model=ImageRead)
async def upload_image(
    title: str, 
    description: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # Ensure the directory exists
    file_path = "app/static"
    os.makedirs(file_path, exist_ok=True)

    file_location = os.path.join(file_path, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = f"/static/{file.filename}"
    db_image = create_image(db, title=title, description=description, url=url)
    return db_image