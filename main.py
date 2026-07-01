from typing import Optional
from fastapi import FastAPI, status, HTTPException 
from fastapi.responses import Response #* to manage response 
from pydantic import BaseModel #* we need `BaseModel` for setting schemas
from random import randint


app = FastAPI()

@app.get("/") # "/" => path, .get => method 
def root():
    return {"msg":"hello api !!!"} 

database = [
    {
        "ID": 1,
        "title": "Getting Started with Python",
        "content": "Python is an easy-to-learn programming language suitable for beginners."
    },
    {
        "ID": 2,
        "title": "Introduction to FastAPI",
        "content": "FastAPI allows you to build high-performance APIs with minimal code."
    },
    {
        "ID": 3,
        "title": "Working with Git",
        "content": "Git helps you track changes in your code and collaborate with others."
    },
    {
        "ID": 4,
        "title": "Learning SQL",
        "content": "SQL is used to manage and query relational databases efficiently."
    },
    {
        "ID": 5,
        "title": "REST API Basics",
        "content": "REST APIs use HTTP methods such as GET, POST, PUT, and DELETE."
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
@app.post("/posts", status_code=status.HTTP_201_CREATED)
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
        return { "data": find_post(id) }

    raise HTTPException( 
        status_code=status.HTTP_404_NOT_FOUND,
        detail={ "data": "Not Found" }
    )