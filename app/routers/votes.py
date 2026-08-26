
from fastapi import  status, HTTPException , Depends, APIRouter
from app.oauth2 import get_user
from sqlalchemy.orm import Session
from .. import models, schemas  
from ..utils import get_db



router = APIRouter(
    prefix="/vote",
    tags=['Votes'] #* UI enhancement: create Votes Category
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, voter: schemas.User = Depends(get_user), db: Session = Depends(get_db)):
    # in voting:
    # 1 = like
    # 0 = unlike
    try:
        post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)

        # check the post
        if post_query.first() is None:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )
    
        # check the vote_dir 
        if vote.vote_dir not in [0, 1]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad Request"
            )
            
        vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == voter.id)
        new_vote = models.Vote(post_id=vote.post_id, user_id=voter.id)

        if vote.vote_dir == 1:
            if vote_query.first() is not None: # the user is liked the post already
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Already Voted"
                )
            else:
                db.add(new_vote)
        else:
            if vote_query.first() is None:
                raise HTTPException( 
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vote is Not Found"
                )   

            vote_query.delete(synchronize_session="evaluate")
        
        
        db.commit()
        return {"detail": "done"}

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )