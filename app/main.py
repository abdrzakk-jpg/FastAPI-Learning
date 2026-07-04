from typing import List
from fastapi import FastAPI, status, HTTPException , Depends

import psycopg as psy # add 'postgreSQL' DBMS for python
from psycopg.rows import dict_row  # dict_row => converts result to python-dict

from rich import print
from scalar_fastapi import get_scalar_api_reference
from sqlalchemy.orm import Session # UI enhancement


from . import models, schemas
from .database import engine, SessionLocal

#* create models in `posts` table
models.Base.metadata.create_all(bind=engine)

#* define get_db dependency

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()



app = FastAPI(
    docs_url=None,   # تعطيل Swagger
    redoc_url=None,  # تعطيل ReDoc
)

try:
    conn = psy.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="123",
        port=5432,
        #* in tutorial the prof used RealDictCursor wich is `replaced` in psycopg3
    )

    #* RealDictCursor alternative 
    cursor = conn.cursor(
        row_factory=dict_row
    )

    print(f"[blue bold]:: [white]DB Connection: [green bold][✓][/green bold]")


except Exception as e:
    print(f"[blue bold]:: [white]DB Connection: [red bold][✖][/red bold]")
    print(f"[red bold]|____Error:[/red bold]{e}")




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

#* to retrun a Group Of Posts in Response => we cover `schemas.PostResponse` within List[...] in `response_model`
#* Why?: The Pydantic Trying To Put Many Objects in PostRespnse and fails !
#* so we make a `List` of `PostResponse-Scheme` To give `Pydantic` ability to create many `PostResponse` Objects

@app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall() #* .fetchall() => get all posts

    posts = db.query(models.Post).all()
    
    return posts


#? response_model=schemas.PostResponse => set response structure
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
#! I used `models.Post` instead `Post` and thats is WRONG!!!
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    try:
        
        #! USE-LESS WAY: Passing each value to its var like below.... is a useless in large model cases (like 10,20,30 column !)
        USE_LESS_created_post = models.Post(title = post.title, content = post.content, published = post.published)

        #* USE-FUL WAY : to avoid last problem, we can use `**` before `post.dict()` to create a dict and distribute the values
        created_post = models.Post(**post.dict())
        

        # true insertion to database
        db.add(created_post)
        db.commit() # save changes
        db.refresh(created_post)

        return created_post
    
    except Exception as err:
        print(f"[blue bold]:: [white]DB Query-Execution: [red bold][✖][/red bold]")
        print(f"[red bold]|____Error:[/red bold]{err}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={ "Post Not Fount" }
        )
#* get post by ID
# #? response_model=schemas.PostResponse => set response structure
@app.get("/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    try: 
        post_detail = db.query(models.Post).filter(models.Post.id == post_id).first()

        if post_detail is None:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )

        return post_detail
        
    # * tell `try:` to avoid HTTPException's
    except HTTPException:
        raise 

    except Exception as err:
        print(f"[blue bold]:: [white]DB Query-Execution: [red bold][✖][/red bold]")
        print(f"[red bold]|____Error:[/red bold]{err}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={ err }
        )



#* delete post route 
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    try: 

        # get the post
        post = db.query(models.Post).filter(models.Post.id == post_id)

        # catch the first one
        if post.first() is None:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )

        post.delete(synchronize_session=False)
        db.commit() # save changes

    # * tell `try:` to avoid HTTPException's
    except HTTPException:
        raise 

    except Exception as err:
        print(f"[blue bold]:: [white]DB Query-Execution: [red bold][✖][/red bold]")
        print(f"[red bold]|____Error:[/red bold]{err}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={ err }
        )


#* add update  post route using "PUT"
#? response_model=schemas.PostResponse => set response structure
@app.put("/posts/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):   
    try: 

        # get the post
        post_query = db.query(models.Post).filter(models.Post.id == post_id)

        updated_post = post_query.first()

        print(f"[blue bold]{updated_post}[/blue bold]")
        # catch the first one
        if updated_post is None:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )

        post_query.update(post.model_dump(), synchronize_session=False) # ignore 

        db.commit() # save changes
        db.refresh(updated_post)
        return updated_post

    # * tell `try:` to avoid HTTPException's
    except HTTPException:
        raise 

    except Exception as err:
        print(f"[blue bold]:: [white]DB Query-Execution: [red bold][✖][/red bold]")
        print(f"[red bold]|____Error:[/red bold]{err}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={ err }
        )





@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
#! I used `models.Post` instead `Post` and thats is WRONG!!!
def user_register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    try:
        #* un-pack the dict in 
        new_user = models.User(**user.dict())
        # true insertion to database
        db.add(new_user)
        db.commit() # save changes
        db.refresh(new_user)

        return new_user
    
    except Exception as err:
        print(f"[blue bold]:: [white]DB Query-Execution: [red bold][✖][/red bold]")
        print(f"[red bold]|____Error:[/red bold]{err}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={ "User Not Fount" }
        )