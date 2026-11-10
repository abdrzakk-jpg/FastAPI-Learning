
from scalar_fastapi import Theme
from scalar_fastapi import Layout
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scalar_fastapi import get_scalar_api_reference # UI enhancement
from app.routers import posts, users, auth, votes
from app.database import engine
import app.models as models
from app.config import settings


if settings.ENVIRONMENT == "production":
    #* create models in `posts` table in production
    models.Base.metadata.create_all(bind=engine) #* disable while using `Alembic`


app = FastAPI(  
    docs_url=None,   # تعطيل Swagger
    redoc_url=None,  # تعطيل ReDoc
)
origins = [
    "https://www.google.com",
]

app.add_middleware(
    CORSMiddleware, # is a function  (Client ----> CORSMiddleware() ----> Backend(Fastapi))
    allow_origins=origins, # 
    allow_credentials=True,
    allow_methods=["*"], # GET, POST,PUT,PATCH,DELETE,OPTIONS ...
    allow_headers=["*"], # 
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
