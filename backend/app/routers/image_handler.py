from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.storage.db import get_db
from app.repositories.image_db import get_image, create_image, get_images, delete_image, get_images_by_title, get_images_by_tags
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

@router.post("/images/", response_model=ImageRead)
def create_new_image(image: ImageCreateWithUrl, db: Session = Depends(get_db)):
    db_image = create_image(db, title=image.title, description=image.description, url=image.url)
    return db_image

# FUNCTIONALITY IS DEPRECATED FOR NOW
@router.post("/uploadfile/", response_model=ImageRead)
async def upload_image(
    title: str, 
    description: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # Ensure the directory exists
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Get the base directory
    static_dir_path = os.path.join(base_dir, 'static')  # Construct the static directory path
    print(static_dir_path)
    os.makedirs(static_dir_path, exist_ok=True)

    file_location = os.path.join(static_dir_path, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = f"/static/{file.filename}"
    db_image = create_image(db, title=title, description=description, url=url)
    return db_image

@router.get("/images/id/{image_id}", response_model=ImageRead)
def read_image_by_id(image_id: int, db: Session = Depends(get_db)):
    db_image = get_image(db, image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@router.get("/images/title/{title}", response_model=List[ImageRead])
def read_image_by_title(title: str, db: Session = Depends(get_db)):
    if title:
        images = get_images_by_title(db, title=title)
    return images

@router.get("/images/", response_model=List[ImageRead])
def read_images(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    images = get_images(db, skip=skip, limit=limit)
    return images

# @router.get("/images/display/", response_model=List[ImageRead])
# def display_images(limit: int = 10, db: Session = Depends(get_db)):
#     if type(limit) != int:
#         raise HTTPException(status_code=400, detail="Limit must be an integer")
#     images = get_images(db, skip=0, limit=limit)
#     return images

@router.delete("/images/{image_id}", response_model=ImageRead)
def delete_image_endpoint(image_id: int, db: Session = Depends(get_db)):
    db_image = delete_image(db, image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@router.get("/images/by_tags", response_model=List[ImageRead])
def read_images_by_tags(tag_ids: Optional[List[int]] = Query(None), db: Session = Depends(get_db)):
    if not tag_ids:
        images = get_images(db, skip=0, limit=1000)
    else:
        images = get_images_by_tags(db, tag_ids)
    return images
