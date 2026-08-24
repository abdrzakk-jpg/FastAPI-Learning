

from pydantic_settings import BaseSettings, InitSettingsSource


class Settings(BaseSettings):
    DB_PWD: str


settings = Settings()
print(settings.DB_PWD)
