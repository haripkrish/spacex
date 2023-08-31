from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Spacex data pipeline"
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", "spacex")
    SPACEX_API_BASE_URL: str = os.environ.get("SPACEX_API_BASE_URL", "https://api.spacexdata.com")
    SPACEX_API_VERSION: str = os.environ.get("SPACEX_API_VERSION", "v4")
    SPACEX_API_URL_V4: str = os.environ.get("SPACEX_API_URL_V4", "https://api.spacexdata.com/v4")
    SPACEX_API_URL_V5: str = os.environ.get("SPACEX_API_URL_V5", "https://api.spacexdata.com/v5")
    POSTGRES_DB_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"


settings = Settings()
