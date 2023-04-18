from fastapi import FastAPI
import uvicorn

from .configuration.settings import settings
from .router import download_router, email_router

api = FastAPI()

api_prefix = f'{settings.api_path_base}{settings.api_path_version}'
api.include_router(download_router.router, prefix=api_prefix)
api.include_router(email_router.router, prefix=api_prefix)

if __name__ == "__main__":
    uvicorn.run("ccserv.__main__:api", forwarded_allow_ips=settings.allow_ips, proxy_headers=True, host=settings.host, port=settings.port, workers=settings.workers, headers=[("server", "ccserv")])