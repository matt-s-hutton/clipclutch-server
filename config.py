from pydantic import BaseSettings
from os import cpu_count

class Settings(BaseSettings):
    host: str
    port: int
    api_path: str
    download_path: str
    workers: int = cpu_count()

    class Config:
        env_file = ".env"

settings = Settings()