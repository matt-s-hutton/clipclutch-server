from pydantic import BaseModel, Field, validator
from .supported_format import SupportedFormat

class DownloadOptions(BaseModel):
    convertFormat: str = Field(..., description="Target format for the media file")
    embedSubs: bool = Field(..., description="Whether to embed subtitles in the output file")
    getThumbnail: bool = Field(..., description="Whether to download the thumbnail")

    @validator('convertFormat')
    def supported_format(cls, format):
        supported_formats = SupportedFormat.get_supported_formats()
        if format not in supported_formats:
            raise ValueError(f"convertFormat must be one of {supported_formats}")
        return format