
from datetime import datetime
from pydantic import (
    BaseModel, #* we need `BaseModel` for setting schemas
    EmailStr   #* for true email structure
    ) 


#! We Need this Schema to set the `post` Structure
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #*=> set defualt value

class PostCreate(PostBase): pass
class PostUpdate(PostBase): pass

#* define the structure returned Post-Data in response 
class PostResponse(PostBase): #* inherite [title, content, published] from `PostBase` 
    id: int
    created_at: datetime 

    #* the following line: make Pydantic to handle with SQLAlchemy-Models 
    #* & Tells Pydantic to read data even if it is not a dict (give ability to return SQLAlchemy-Models in Responses)
    class Config:
        orm_mode = True



class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    joined_at: datetime

    class Config:
        orm_mode = True

class UserLogin(UserRegister):
    pass


class Token(BaseModel):
    access_token: str
    token_type  : str = "bearer"

class TokenData(BaseModel):
    sub: str
