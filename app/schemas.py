
from datetime import datetime
from pydantic import BaseModel #* we need `BaseModel` for setting schemas


#! We Need this Schema to set the `post` Structure
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #*=> set defualt value

class PostCreate(PostBase): pass
class PostUpdate(PostBase): pass

#* define the structure returned Post-Data in response 
class PostResponse(BaseModel):
    title: str
    content: str
    published: bool 
    #! 
    created_at: datetime 

    #* the following line: make Pydantic to handle with SQLAlchemy-Models 
    #* & Tells Pydantic to read data even if it is not a dict (give ability to return SQLAlchemy-Models in Responses)
    class Config:
        orm_mode = True