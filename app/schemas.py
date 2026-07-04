
from pydantic import BaseModel #* we need `BaseModel` for setting schemas


#! We Need this Schema to set the `post` Structure
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #*=> set defualt value

class PostCreate(PostBase): pass

class PostUpdate(PostBase): pass