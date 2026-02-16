"""
UserLoginRequest schema.
"""

from pydantic import BaseModel, EmailStr, Field


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(
        ...,
        min_length=1,
        max_length=72,
        description="User password (max 72 characters)",
    )

