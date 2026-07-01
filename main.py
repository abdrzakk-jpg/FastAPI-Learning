
from fastapi import FastAPI, Request, Body

app = FastAPI()
@app.get("/") # "/" => path, .get => method 
def root():
    return {"msg":"hello api !!!"} 