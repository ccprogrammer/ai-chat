"""
ChatUpdateRequest schema.
"""

from pydantic import BaseModel, Field


class ChatUpdateRequest(BaseModel):
    """Request to update a chat title"""
    title: str = Field(..., min_length=1, max_length=200, description="New title for the chat")

