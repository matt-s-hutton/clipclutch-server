from fastapi import APIRouter
from ..model.download_parameters import DownloadParameters
from ..model.download_response import DownloadResponse
from ..configuration.settings import settings
from ..service.download_service import download_service


router = APIRouter()

@router.post(
    settings.api_path_download,
    response_model=DownloadResponse,
    description="This endpoint accepts JSON in the request body, and is used to download media. "
        "Despite being a POST endpoint, it is used for data retrieval. "
        "This is because transmitting the JSON via GET is less maintainable. "
        "The JSON object must have a structure that can be mapped to DownloadParameters"
)
async def download(params: DownloadParameters):
    response = download_service(params)
    return response.dict()