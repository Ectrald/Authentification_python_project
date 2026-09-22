from datetime import datetime

from pydantic import BaseModel, EmailStr


class TokenCreate(BaseModel):
    user_id: int
    token: str
    expires_at: datetime


class TokenVerify(BaseModel):
    token: str


class ResendRequest(BaseModel):
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class VerifyResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"
