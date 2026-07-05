
from fastapi import status, HTTPException , Depends

import psycopg as psy # add 'postgreSQL' DBMS for python
from psycopg.rows import dict_row  # dict_row => converts result to python-dict

from rich import print
from sqlalchemy.orm import Session # UI enhancement

from .. import models, schemas
from ..utils import hash_pwd, get_db
from ..main import app








@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def user_register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    try:
        #* hash user password
        user.password = hash_pwd(user.password)

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
            detail=err
        )


#* get user by ID
# #? response_model=schemas.UserResponse => set response structure
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
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
        print(f"[blue bold]:: [white]DB Query-Execution: [red bold][✖][/red bold]")
        print(f"[red bold]|____Error:[/red bold]{err}")
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err
        )
