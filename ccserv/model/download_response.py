from pydantic import BaseModel, Field

class DownloadResponse(BaseModel):
    path: str = Field(..., description="Path to the downloaded file")
    format: str = Field(..., description="Format of the downloaded file, must be one of the supported formats")
    media: str = Field(..., description="Video or audio")
    thumbnail: str = Field(None, description="URL of the video's thumbnail")
    warning: str = Field(None, description="Warn the user of something e.g. video is provided in a format different to the request")
