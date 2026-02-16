"""
UserRoleUpdateRequest schema.
"""

from typing import Literal

from pydantic import BaseModel


class UserRoleUpdateRequest(BaseModel):
    """Body for updating a user's role (admin API)."""
    role: Literal["user", "admin"]

