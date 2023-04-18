import aiosmtplib
from email.message import EmailMessage

from fastapi import HTTPException
from ..model.email_parameters import EmailParameters
from ..configuration.settings import settings

async def email_service(params: EmailParameters):
    from_email = params.email
    enquiry = params.message

    message = EmailMessage()
    message.set_content(f'Email: {from_email}\nMessage: {enquiry}')
    message['Subject'] = f"ClipClutch Email from {from_email}"
    message['From'] = 'user@clipclutch.app'
    message['To'] = settings.email_address

    try:
        async with aiosmtplib.SMTP(
            hostname=settings.smtp_hostname,
            port=settings.smtp_port,
            use_tls=True
        ) as client:
            await client.login(settings.smtp_username, settings.smtp_password)
            await client.send_message(message)
    except aiosmtplib.errors.SMTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return