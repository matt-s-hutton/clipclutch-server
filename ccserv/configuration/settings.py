from functools import lru_cache
from pydantic import BaseSettings
from os import cpu_count

class Settings(BaseSettings):
    host: str
    port: int
    api_path_base: str
    api_path_version: str
    api_path_download: str
    api_path_email: str
    download_location_local: str
    download_location_remote: str
    email_address: str
    smtp_hostname: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    allow_ips: str = '*'
    workers: int = cpu_count()

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    r_settings = Settings()
    return r_settings

settings = get_settings()