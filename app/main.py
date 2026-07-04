from fastapi import FastAPI, status, HTTPException , Depends
from pydantic import BaseModel #* we need `BaseModel` for setting schemas

import psycopg as psy # add 'postgreSQL' DBMS for python
from psycopg.rows import dict_row  # dict_row => converts result to python-dict

from rich import print
from scalar_fastapi import get_scalar_api_reference
from sqlalchemy.orm import Session # UI enhancement


from . import models
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


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall() #* .fetchall() => get all posts

    posts = db.query(models.Post).all()
    return {"data":posts}

#! We Need this Schema to set the `post` Structure
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #*=> set defualt value

    
@app.post("/posts", status_code=status.HTTP_201_CREATED)
#! I used `models.Post` instead `Post` and thats is WRONG!!!

def create_post(post: Post, db: Session = Depends(get_db)):
    try:
        
        #! USE-LESS WAY: Passing each value to its var like below.... is a use-less in large model cases (like 10,20,30 column !)
        USE_LESS_created_post = models.Post(title = post.title, content = post.content, published = post.published)

        #* USE-FUL  WAY: to avoid last problem, we can use `**` before `post.dict()` to create a dict and distribute the values
        created_post = models.Post(**post.dict())
        
        # true insertion to database
        db.add(created_post)
        db.commit() # save changes
        db.refresh(created_post)

        return {        
                "data": created_post, #* include the created post
                "msg": "Post Created Successfully "
        }
    except Exception as err:
        print(f"[blue bold]:: [white]DB Query-Execution: [red bold][✖][/red bold]")
        print(f"[red bold]|____Error:[/red bold]{err}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={ "Post Not Fount" }
        )
#* get post by ID
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    try: 
        cursor.execute(
            "SELECT * FROM posts WHERE id=%s",
            (str(post_id),)
        )

        post_detail = cursor.fetchone()
        if post_detail:
            return {
                "data": post_detail
            }
        else:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )
    # * to fully `raise HTTPException` with status-code & detail
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
def delete_post(post_id: int):
    try: 

        cursor.execute(
            "DELETE FROM posts WHERE id=%s",
            (str(post_id),)
        )

        conn.commit()

    except Exception as err:
        print(f"[blue bold]:: [white]DB Query-Execution: [red bold][✖][/red bold]")
        print(f"[red bold]|____Error:[/red bold]{err}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={ err }
        )


#* add update  post route using "PUT"
@app.put("/posts/{id}")
def update_post(id: int, post :Post):   

    cursor.execute(f"UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *;", (post.title,post.content, post.published, str(id)))

    updated_post = cursor.fetchone()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    conn.commit()

    return {"data": updated_post}
