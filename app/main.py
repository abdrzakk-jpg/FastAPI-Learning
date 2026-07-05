from typing import List
from fastapi import FastAPI, status, HTTPException , Depends

import psycopg as psy # add 'postgreSQL' DBMS for python
from psycopg.rows import dict_row  # dict_row => converts result to python-dict

from rich import print
from scalar_fastapi import get_scalar_api_reference
from sqlalchemy.orm import Session # UI enhancement


from . import models, schemas
from .database import engine, SessionLocal
from .utils import hash_pwd



#* create models in `posts` table
models.Base.metadata.create_all(bind=engine)


app = FastAPI(  
    docs_url=None,   # تعطيل Swagger
    redoc_url=None,  # تعطيل ReDoc
)


#* ===================|Updating-Docs-UI|=================== *#
@app.get("/docs", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="API Docs",
    )
#* ======================================================== *#

@app.get("/") # "/" => path, .get => method 
def root():
    return {"msg":"hello api !!!"} 

