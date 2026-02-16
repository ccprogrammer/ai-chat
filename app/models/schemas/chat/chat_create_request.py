"""
ChatCreateRequest schema.
"""

from typing import Optional

from pydantic import BaseModel, Field


class ChatCreateRequest(BaseModel):
    """Request to create a new chat"""
    title: Optional[str] = Field(None, description="Optional title for the chat")

