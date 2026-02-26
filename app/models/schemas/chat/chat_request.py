"""
ChatRequest schema.
"""

from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Incoming chat message from the client.
    If chat_id is omitted or invalid, a new chat is created.
    """
    chat_id: Optional[str] = Field(
        default=None,
        description="Chat ID. If omitted or not found, a new chat is created"
    )
    message: str = Field(
        ...,
        min_length=1,
        description="User message to the AI"
    )

