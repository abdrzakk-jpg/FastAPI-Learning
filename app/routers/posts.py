from app import oauth2
from fastapi import  status, HTTPException , Depends, APIRouter


from typing import List

from rich import print
from sqlalchemy.orm import Session


from .. import models, schemas
from ..utils import get_db

#* we can use `prefix` parameter to pass a `Unified` path structure
router = APIRouter(
    prefix="/posts",
    tags=['Posts'] #* UI enhancement: create Posts Category
)


#* to retrun a Group Of Posts in Response => we cover `schemas.PostResponse` within List[...] in `response_model`
#* Why?: The Pydantic Trying To Put Many Objects in PostRespnse and fails !
#* so we make a `List` of `PostResponse-Scheme` To give `Pydantic` ability to create many `PostResponse` Objects

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall() #* .fetchall() => get all posts

    posts = db.query(models.Post).all()

    return posts


#? response_model=schemas.PostResponse => set response structure
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
#! I used `models.Post` instead `Post` and thats is WRONG!!!
#* `user_id` is taken from `get_user()` that take token from `OAuth2PasswordBearer` that take it from `/login` that have `access_token`
#* then decode the token and return id
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
            detail=err
        )
#* get post by ID
# #? response_model=schemas.PostResponse => set response structure
@router.get("/{post_id}", response_model=schemas.PostResponse)
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
            detail=err
        )



#* delete post route 
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
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
            detail=err
        )


#* add update  post route using "PUT"
#? response_model=schemas.PostResponse => set response structure
@router.put("/{post_id}", response_model=schemas.PostResponse)
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

        # pyrefly: ignore [bad-argument-type]
        post_query.update(post.model_dump(), synchronize_session=False) # ignore 

        db.commit() # save changes
        db.refresh(updated_post)
        return updated_post

    # * tell `try:` to avoid HTTPException's
    except HTTPException:
        raise 
    #* just to commit to git
    except Exception as err:
        print(f"[blue bold]:: [white]DB Query-Execution: [red bold][✖][/red bold]")
        print(f"[red bold]|____Error:[/red bold]{err}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )

