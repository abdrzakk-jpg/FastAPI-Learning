
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import (
    ForeignKey,
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
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    #                                      tablename.column
    author_info = relationship("User") ## SQLAlchemy gets the User-Data (id, email, joined_at) automaticaly !
    ## we must put the Model Name instead __tablename__ in place of <"User">

# user structure in data-base
class User(Base):
    # define table name:
    __tablename__ = "users"
    
    # define columns
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    joined_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
    phone_number = Column(String, nullable=False, unique=True)

# Vote structure in data-base
class Vote(Base):
    # define table name:
    __tablename__ = "votes"

    # define columns (post_id PK, user_id PK)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)