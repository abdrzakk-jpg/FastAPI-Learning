
from passlib.context import CryptContext # import to set hashing method
from .database import SessionLocal
pwd_context = CryptContext(
    schemes=["argon2"], #* `argon2` better than `bcrypt`
    deprecated = "auto"
)


def hash_pwd(pwd: str) -> str:
    return pwd_context.hash(pwd)

def verify_pwd (hahedpwd: str, pwd: str) -> bool:
    return pwd_context.verify(pwd, hahedpwd)


#* define get_db dependency
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

