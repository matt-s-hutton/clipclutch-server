from urllib.parse import urlsplit
from pydantic import BaseModel, Field, validator
from downloadoptions import DownloadOptions

class DownloadParameters(BaseModel):
    url: str = Field(..., description="URL of the video to download")
    options: DownloadOptions

    @validator('url')
    def valid_url(cls, url_to_validate):
        parsed_url = urlsplit(url_to_validate)
        if not (parsed_url.scheme and parsed_url.netloc):
            raise ValueError("'url' must be a valid URL")
        return url_to_validate