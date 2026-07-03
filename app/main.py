from fastapi import FastAPI, status, HTTPException 
from fastapi.responses import Response #* to manage response 
from pydantic import BaseModel #* we need `BaseModel` for setting schemas
from rich import print
import psycopg as psy # add 'postgreSQL' DBMS for python
from psycopg.rows import dict_row  # dict_row => converts result to python-dict
from scalar_fastapi import get_scalar_api_reference # UI enhancement
    

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
    cursor.execute("SELECT * FROM posts")
    
    posts = cursor.fetchall() #* .fetchall() => get all posts
    return {"data":posts}
    


#* to Force the client to send a strict body of data, we must use `BaseModel` to set Schema of Request's
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #*=> set defualt value

    
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    #! UN-RECOMENDED: SQL-Ijnection threat 
    '''
        cursor.execute(f"""
        INSERT INTO posts(title, content, published) VALUES ('{post.title}', '{post.content}', {post.published}) ; 
        """)    
    '''
    
    try:
        #* RECOMENDED: filterd way (psycopg interact with SQL queries)
        cursor.execute(f"""
        INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *; 
        """, (post.title, post.content, post.published))
        created_post = cursor.fetchone() #* return values (will not work without `RETURNING ..`)
        conn.commit() #* => save changes
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
