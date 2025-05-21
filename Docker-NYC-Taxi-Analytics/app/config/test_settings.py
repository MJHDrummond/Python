from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@db:5433/test_analytics"
    secret_token: str = "secret-token"

test_settings = TestSettings()
