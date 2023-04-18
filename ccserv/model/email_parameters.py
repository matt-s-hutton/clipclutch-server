from pydantic import BaseModel, EmailStr


class EmailParameters(BaseModel):
    email: EmailStr
    message: str