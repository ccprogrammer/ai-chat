"""
ChatMessageResponse schema.
"""

from pydantic import BaseModel, Field


class ChatMessageResponse(BaseModel):
    """
    AI reply returned to the client
    """
    reply: str = Field(
        ...,
        description="AI-generated response"
    )
    chat_id: str = Field(
        ...,
        description="Chat ID this message belongs to"
    )

