
from fastapi import status, HTTPException, Depends, APIRouter
from rich import print
from sqlalchemy.orm import Session 
from .. import models, schemas
from ..utils import hash_pwd, get_db




#* we can use `prefix` parameter to pass a `Unified` path structure
router = APIRouter(
    prefix="/users", #* best-practicies way for better router managing
    tags=['Users'] #* UI enhancement: create Users Category
)




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def user_register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    try:
        
        
        #* Check If The User Email|Phone_number is taken:
        email_query = db.query(models.User).filter(models.User.email == user.email)
        phone_number_query = db.query(models.User).filter(models.User.phone_number == user.phone_number)
        
         
        if (email_query.first() or phone_number_query.first()) is not None:
            raise HTTPException( 
                status_code=status.HTTP_409_CONFLICT,
                detail="Invaild Credentials"
            )
        
        
        
        #* hash user password
        user.password = hash_pwd(user.password)

        #* un-pack the dict in User-model
        new_user = models.User(**user.dict())
        # true insertion to database
        db.add(new_user)
        db.commit() # save changes
        db.refresh(new_user)

        return new_user
    
    except HTTPException:
        raise
    
    except Exception as err:
        print(f"[red bold][✖][/red bold] Error: [yellow]{err}[/yellow]\n[green][➔][/green] {__file__}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )


#* get user by ID
#? will converted to prefix=/users/{user_id}
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try: 
        user_query = db.query(models.User).filter(models.User.id == user_id)

        if user_query.first() is None:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )

        return user_query.first()
        
    # * tell `try:` to avoid HTTPException's
    except HTTPException:
        raise 

    except Exception as err:
        print(f"[red bold][✖][/red bold] Error: [yellow]{err}[/yellow]\n[green][➔][/green] {__file__}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )
