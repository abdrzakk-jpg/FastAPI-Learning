
from datetime import datetime
from pydantic import (
    BaseModel, #* we need `BaseModel` for setting schemas
    EmailStr   #* for true email structure
    ) 
from pydantic_extra_types.phone_numbers import PhoneNumber

#! We Need this Schema to set the `post` Structure
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #*=> set defualt value

class PostCreate(PostBase): pass
class PostUpdate(PostBase): pass



class PostDictSchema(PostBase):
    id: int
    created_at: datetime 
    author_id: int


    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    Post: PostDictSchema
    votes: int

    class Config:
        from_attributes = True


class User(BaseModel):
    id: int
    email: EmailStr
    joined_at: datetime
    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    phone_number: PhoneNumber

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    joined_at: datetime
    phone_number: str

    class Config:
        from_attributes = True

class UserLogin(UserRegister):
    pass


class Token(BaseModel):
    access_token: str
    token_type  : str = "bearer"

class TokenData(BaseModel):
    sub: str


class Vote(BaseModel):
    post_id: int
    vote_dir: int

    class Config:
        from_attributes = True