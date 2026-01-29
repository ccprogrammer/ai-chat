"""
Auth-related Pydantic schemas.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserRegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="User password (8-72 characters; longer passwords are not supported by bcrypt)",
    )


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(
        ...,
        min_length=1,
        max_length=72,
        description="User password (max 72 characters)",
    )


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

