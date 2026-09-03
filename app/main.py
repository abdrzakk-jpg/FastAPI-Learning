
from scalar_fastapi import Theme
from scalar_fastapi import Layout
from app.routers import votes
from fastapi import FastAPI

from scalar_fastapi import get_scalar_api_reference # UI enhancement

from app.routers import posts, users, auth

from app.database import engine
from app import models


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
        layout=Layout.CLASSIC,
        theme=Theme.DEEP_SPACE,
        title="API Docs",
    )
#* ======================================================== *#

@app.get("/") # "/" => path, .get => method 
def root():
    return {"msg":"hello api !!!"} 



#* add routers 
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router) # add `login` end-point
app.include_router(votes.router) # add `vote` end-point
