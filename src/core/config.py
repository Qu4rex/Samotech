from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "My Application"
    debug: bool = False
    database_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()