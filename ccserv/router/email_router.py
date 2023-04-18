from fastapi import APIRouter, BackgroundTasks
from ccserv.configuration.settings import settings
from ..model.email_parameters import EmailParameters
from ..service.email_service import email_service

router = APIRouter()

@router.post(
    settings.api_path_email,
    description="This endpoint is used to send an email. Yhe JSON object "
    "in the body must have a structure that can be mapped to EmailParameters"
)
async def email(params: EmailParameters, background_tasks: BackgroundTasks):
    background_tasks.add_task(email_service, params)
    return {"status": "success", "detail": "Email sending has been scheduled"}