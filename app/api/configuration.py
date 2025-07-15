import os
from pydantic_settings import BaseSettings

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    hash_algorithm: str
    access_token_expire_minutes: int
    project_root: str = PROJECT_ROOT

    class Config:
        env_file = os.path.join(PROJECT_ROOT, '.env')
        frozen = True  # Prevents modification of settings after initialization


settings = Settings()
