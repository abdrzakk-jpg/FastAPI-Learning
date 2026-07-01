from typing import Optional
from fastapi import FastAPI, status #* import status to manage response codes 
from fastapi.responses import Response #* to manage response 
from pydantic import BaseModel #* we need `BaseModel` for setting schemas
from random import randint


app = FastAPI()

@app.get("/") # "/" => path, .get => method 
def root():
    return {"msg":"hello api !!!"} 

database = [
    {
        "title":"title 1",
        "content":"content content content content",
        "ID":1
    }
]
#* func to get post by ID
def find_post(id: int):
    for p in database:
        if p["ID"] == id:
            return p
    
    return None #* if "ID" not found
    

@app.get("/posts")
def get_posts():
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
    post_dict = post_body.dict()
    post_dict["ID"] = randint(1, 1000000) #* make ID for new post
    database.append(post_dict) #* add post in db
    return {        
        "data":database, #* include the sended data in response    
        "msg": "Post Created Successfully "
        }

#* getting post by ID
@app.get("/posts/{id}")
def get_post(id: int, res: Response):
    #* add return with `find_post(id)` value verification
    if find_post(id) != None:
        return { "data": find_post(id)}
    
    res.status_code = status.HTTP_404_NOT_FOUND #* change status_code to 404
    
    return { "data": "Not Found" }