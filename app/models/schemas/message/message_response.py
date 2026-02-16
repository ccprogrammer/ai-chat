"""
MessageResponse schema.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    """Message information response"""
    id: int = Field(..., description="Message ID")
    chat_id: str = Field(..., description="Chat this message belongs to")
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    created_at: datetime = Field(..., description="When the message was created")

    class Config:
        from_attributes = True

