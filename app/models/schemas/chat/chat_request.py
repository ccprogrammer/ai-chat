"""
ChatRequest schema.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Incoming chat message from the client (Flutter, Web, etc.)
    """
    chat_id: str = Field(
        ...,
        description="Unique identifier for the chat/conversation"
    )
    message: str = Field(
        ...,
        min_length=1,
        description="User message to the AI"
    )

