import os
import sys
import uvicorn
from ccserv.configuration.settings import settings

def main():
    uvicorn.run("ccserv.api:api", forwarded_allow_ips=settings.allow_ips, proxy_headers=True, host=settings.host, port=settings.port, workers=settings.workers, headers=[("server", "ccserv")])

if __name__ == '__main__':
    main()
