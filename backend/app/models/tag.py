from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

# Optional: A function to create the table
def create_tag_table(engine):
    Base.metadata.create_all(bind=engine)