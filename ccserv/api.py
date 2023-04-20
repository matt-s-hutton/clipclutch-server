from fastapi import FastAPI

from .configuration.settings import settings
from .router import download_router, email_router

api = FastAPI()

api_prefix = f'{settings.api_path_base}{settings.api_path_version}'
api.include_router(download_router.router, prefix=api_prefix)
api.include_router(email_router.router, prefix=api_prefix)

