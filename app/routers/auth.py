
from app.oauth2 import create_token
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm  # to set sended-data Form (OAuth2 standard)
from .. import utils, models, schemas
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authintiacation'])

#* create user-login end-point
@router.post("/login", response_model=schemas.LoginResponse)
# FastAPI will notice that `Depends()` is empty ===> it will use `OAuth2PasswordRequestForm` like :<user_credentials = Depends( OAuth2PasswordRequestForm )>
# the data will recived from `body` of Form-Data
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(utils.get_db)) :

    try:
        # in `OAuth2PasswordRequestForm` there are TWO vars: `username` & `password`
        # we can easly use `username` instead of `email` by code below in `user_credentials`
        user_query = db.query(models.User).filter(models.User.email == user_credentials.username)

        if user_query.first() is None:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invaild Credentials"
            )
        
        user_password: str = user_query.first().password # pyrefly: ignore [missing-attribute]
        
        if not utils.verify_pwd(user_password, user_credentials.password): # if given_password == saved_password (avter hash comparing ...)
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invaild Credentials"
            )
        
        
        payload: dict = {"sub": int(user_query.first().id)} # pyrefly: ignore [missing-attribute]
        token: str = create_token(payload)

        return {
            "access_token": token,
            "token_type": "bearer"
        }


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