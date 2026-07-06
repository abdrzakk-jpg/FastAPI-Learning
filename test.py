from httpcore import __name
from time import sleep
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError


SECRET_KEY = "L73Kc5bk,3Gj)$|)!/)z{i)aQ:7-ye[(!)LQy9yFfv|"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUETS = 30

def create_token(payload: dict):
    to_encode = payload.copy()

    # count 30-minutes from now
    exp = datetime.now(timezone.utc) + timedelta(seconds=3)  
    
    to_encode.update({"exp": exp})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token





def verify_token(token_):
    token_data: dict = jwt.decode(
        token=token_, 
        key=SECRET_KEY, 
        algorithms=ALGORITHM
    )

    
    token_exp:int = int(token_data.get("exp")) # pyrefly: ignore [bad-argument-type]
    now = datetime.now(timezone.utc) 

    # if now > datetime.fromtimestamp(token_exp, tz=timezone.utc) :
    #     return "token expired"

    return "token is good"


def test():
    user_data = {
    "user": "abdo",
    "role": "user"
    }
    token: str = create_token(user_data)
    print(verify_token(token))
    print("Sleep for 5 secs...")
    sleep(2)
    print(verify_token(token))

if __name__ == '__main__':
    test()