from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://username:password@localhost/physiobuddy_app"


settings = Settings()
