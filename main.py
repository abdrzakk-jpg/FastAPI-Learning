from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel #* we need `BaseModel` for setting schemas
app = FastAPI()
@app.get("/") # "/" => path, .get => method 
def root():
    return {"msg":"hello api !!!"} 

database = [
    {
        "title":"title 1",
        "content":"content content content content",
        "ID":0
    }
]

@app.get("/posts")
def get_posts(req: Request):
    return {
        "data": database
    }
    


#* to Force the client to send a strict body of data, we must use `BaseModel` to set Schema of Request's
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #*=> set defualt value
    rating: Optional[int] = None #*=> make rating Optional
    
#* /createpost => /posts: for good practiceies
@app.post("/posts")
def create_post(post_body: Post):
    return {
        "data":database, #* include the sended data in response    
        "msg": "Post Created Successfully "
        }