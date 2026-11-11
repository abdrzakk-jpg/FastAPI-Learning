import sqlalchemy
from sqlalchemy import func, Row
from app.oauth2 import get_user
from app import oauth2
from fastapi import  status, HTTPException , Depends, APIRouter
from typing import List, Optional, Any
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
def get_posts(db: Session = Depends(get_db), author: schemas.User = Depends(get_user), limit: int = 5, skip=0, search: Optional[str] = ""):
    
    # posts = db.query(models.Post).filter(models.Post.author_id == author.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id,models.Vote.post_id)
    
    filtered_query = posts_query.filter(models.Post.author_id == author.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)

    return filtered_query.all()


#? response_model=schemas.PostResponse => set response structure
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), author: schemas.User  = Depends(oauth2.get_user)):
    try:

        created_post = models.Post(**post.dict(), author_id = author.id)

        # true insertion to database
        db.add(created_post)
        db.commit() # save changes
        db.refresh(created_post)
        print(f"[blue]{post}[/blue]")
        print(f"[blue]{created_post}[/blue]")
        return schemas.PostResponse(Post=created_post, votes=0) #* votes=0 on create-time
    
    except Exception as err:
        print(f"[red bold][✖][/red bold] Error: [yellow]{err}[/yellow]\n[green][➔][/green] {__file__}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )
        
        
#* get post by ID
# #? response_model=schemas.PostResponse => set response structure
@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db), ):
    try: 
        posts_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id,models.Vote.post_id)
        filtred_post_query = posts_query.filter(models.Post.id == post_id).first()

        if filtred_post_query is None:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )

        return filtred_post_query
        
    # * tell `try:` to avoid HTTPException's
    except HTTPException:
        raise 

    except Exception as err:
        print(f"[red bold][✖][/red bold] Error: [yellow]{err}[/yellow]\n[green][➔][/green] {__file__}")
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
        print(f"[red bold][✖][/red bold] Error: [yellow]{err}[/yellow]\n[green][➔][/green] {__file__}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )


#* add update post route using "PUT"
@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), author: schemas.User  = Depends(oauth2.get_user)):
       
    try: 
        post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        grouping_filter = post_query.filter(models.Post.author_id == author.id).group_by(models.Post.id)
        target_post = grouping_filter.filter(models.Post.id == post_id) # the result is a tuple(or row) of (Post, votes)
        
        # target_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.author_id == author.id)
        
        # catch the first one
        to_update_post, votes = target_post.first()
        
        # check if it None
        if to_update_post is None:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )

        # make-Sure if it belongs to correct user
        if to_update_post.author_id != author.id:
            raise HTTPException( 
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not Allowed"
            )
        
        
        db.query(models.Post).filter(models.Post.author_id == author.id, models.Post.id == post_id).update({**post.model_dump(exclude_unset=True)}, synchronize_session="evaluate") 
        db.commit() # save changes
        db.refresh(to_update_post)
        
        return schemas.PostResponse(
            Post={
            **post.model_dump(),
            "id" : post_id,
            "created_at": to_update_post.created_at,
            "author_id": to_update_post.author_id
            }, votes=votes)

    # * tell `try:` to avoid HTTPException's
    except HTTPException:
        raise 
    
    except Exception as err:
        print(f"[red bold][✖][/red bold] Error: [yellow]{err}[/yellow]\n[green][➔][/green] {__file__}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )

