from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:password@db:5432/nyc_taxi"
    secret_token: str = "secret-token"

settings = Settings()
