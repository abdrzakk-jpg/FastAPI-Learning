
from fastapi import Depends, HTTPException, status, APIRouter

from .. import utils, models, schemas
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authintiacation'])

#* create user-login end-point
@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(utils.get_db)) :

    try:
        
        user_query = db.query(models.User).filter(models.User.email == user_credentials.email)

        if user_query.first() is None:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invaild Credentials"
            )


        # pyrefly: ignore [missing-attribute]
        user_password: str = user_query.first().password
        
        if not utils.verify_pwd(user_password, user_credentials.password): # if given_password == saved_password (avter hash comparing ...)
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invaild Credentials"
            )

        return "Logged In Successfully !"

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