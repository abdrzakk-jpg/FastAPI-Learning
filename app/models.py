from .database import Base
from sqlalchemy import (
    Integer,
    String,
    Boolean,
    Column, 
)

# post structure in data-base
class Post(Base):
    # define table name:
    __tablename__ = "posts"
    
    # define columns
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True, nullable=False)