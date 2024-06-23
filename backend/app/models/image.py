from sqlalchemy import Column, Integer, String
from app.models.base import Base

# Define the Image model class
class Image(Base):
    __tablename__ = "images"
    
    # Define the columns of the table
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    url = Column(String, index=True)  # Add URL field

# Optional: A function to create the table
def create_image_table(engine):
    Base.metadata.create_all(bind=engine)