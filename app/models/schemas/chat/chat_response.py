"""
ChatResponse schema.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    """Chat information response"""
    id: str = Field(..., description="Unique chat identifier")
    user_id: str = Field(..., description="User who owns this chat")
    title: Optional[str] = Field(None, description="Chat title")
    created_at: datetime = Field(..., description="When the chat was created")
    updated_at: datetime = Field(..., description="When the chat was last updated")
    message_count: int = Field(0, description="Number of messages in this chat")

    class Config:
        from_attributes = True

