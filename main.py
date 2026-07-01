
from fastapi import FastAPI, Request, Body

app = FastAPI()
@app.get("/") # "/" => path, .get => method 
def root():
    return {"msg":"hello api !!!"} 


@app.get("/posts")
def get_posts(req: Request):
    return {
        "data": "post 1"
    }
    