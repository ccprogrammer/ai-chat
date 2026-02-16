"""
UserRegisterRequest schema.
"""

from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="User password (8-72 characters; longer passwords are not supported by bcrypt)",
    )

