
from passlib.context import CryptContext # import to set hashing method

pwd_context = CryptContext(
    schemes=["argon2"], #* `argon2` better than `bcrypt`
    deprecated = "auto"
)


def hash_pwd(pwd: str) -> str:
    return pwd_context.hash(pwd)
