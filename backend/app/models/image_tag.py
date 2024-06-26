from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import Base
from sqlalchemy.orm import relationship

class ImageTag(Base):
    __tablename__ = "image_tags"
    
    image_id = Column(Integer, ForeignKey("images.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
    image = relationship("Image", back_populates="tags")
    tag = relationship("Tag", back_populates="images")

# Optional: A function to create the table
def create_image_tag_table(engine):
    Base.metadata.create_all(bind=engine)