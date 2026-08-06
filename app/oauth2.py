
from app.schemas import TokenData
from fastapi import HTTPException, status, Depends
from datetime import timedelta, datetime, timezone
# pyrefly: ignore [untyped-import]
from jose import jwt, JWTError
from rich import print
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "L73Kc5bk,3Gj)$|)!/)z{i)aQ:7-ye[(!)LQy9yFfv|"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUETS = 30

def create_token(payload: dict):
    # token createion
    to_encode = payload.copy()

    # count 30-minutes from now
    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUETS)  
    
    to_encode.update({"exp": exp})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


#* we used `credentials_exception` to avoid `HTTPException` Err Repetation in the Code 
def verify_token(token, credentials_exception) -> TokenData:
    # verify token validation
    try:
        # the `decode()` method automaticly checks the token expiration
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = payload.get("sub")

        if user_id is None: raise credentials_exception

        token_data = TokenData(id=user_id)
    
    except JWTError :
        raise credentials_exception

    return token_data


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # `OAuth2PasswordBearer` take `token` from headers !

# just to set `credentials_exception`
def get_user(token: str = Depends(oauth2_scheme)): #the token is taken automaticly from `OAuth2PasswordBearer`
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could Not Validate Credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return verify_token(token, credentials_exception)