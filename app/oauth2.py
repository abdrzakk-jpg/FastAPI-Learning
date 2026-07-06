from datetime import timedelta, datetime
from jose import jwt, JWTError


SECRET_KEY = "L73Kc5bk,3Gj)$|)!/)z{i)aQ:7-ye[(!)LQy9yFfv|"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUETS = 30

def create_token(payload: dict):
    to_encode = payload.copy()

    # count 30-minutes from now
    exp = datetime.now() + timedelta(ACCESS_TOKEN_EXPIRATION_MINUETS)  
    
    to_encode.update({"exp": exp})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token
