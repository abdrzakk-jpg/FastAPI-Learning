


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ==>JWT<==
    ACCESS_TOKEN_EXPIRATION_MINUETS: int
    SECRET_KEY: str
    ALGORITHM : str
    # ==>DB<==
    DB_PASSWORD: str
    DB_USERNAME: str
    DB_HOSTNAME: str
    DB_PORT: str
    DB_NAME: str
    ENVIRONMENT: str

    class Config: #*=> to set env vars source
        env_file = ".env"

# create an instance
settings = Settings()