from app.oauth2 import get_user
from app import oauth2
from fastapi import  status, HTTPException , Depends, APIRouter
from typing import List
from rich import print
from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts'] #* UI enhancement: create Posts Category
)

# get all posts for logged-in user 
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), author: schemas.User = Depends(get_user), limit: int = 5):

    posts = db.query(models.Post).filter(models.Post.author_id == author.id).limit(limit).all()
    
    return posts


#? response_model=schemas.PostResponse => set response structure
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), author: schemas.User  = Depends(oauth2.get_user)):
    try:

        created_post = models.Post(**post.dict(), author_id = author.id)

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
def get_post(post_id: int, db: Session = Depends(get_db), ):
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
def delete_post(post_id: int, db: Session = Depends(get_db), author: schemas.User  = Depends(oauth2.get_user)):
    try: 

        # get the post
        post: models.Post = db.query(models.Post).filter(models.Post.id == post_id)

        # catch the first one
        if post.first() is None:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )            
        # this is `More logical`
        if post.first().author_id != author.id:
            raise HTTPException( 
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not Allowed"
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


#* add update post route using "PUT"
@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), author: schemas.User  = Depends(oauth2.get_user)):   
    try: 

        # get the post
        post_query = db.query(models.Post).filter(models.Post.id == post_id)

        updated_post = post_query.first()

        # catch the first one
        if updated_post is None:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )

        if updated_post.author_id != author.id:
            raise HTTPException( 
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not Allowed"
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

