"""
UserResponse schema.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    role: str = "user"
    created_at: datetime

    class Config:
        from_attributes = True

