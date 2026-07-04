from .database import Base
from sqlalchemy import (
    TIMESTAMP,
    Integer,
    String,
    Boolean,
    Column,
    text, 
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
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)


class User(Base):
    # define table name:
    __tablename__ = "users"
    
    # define columns
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    joined_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)