"""
ChatListResponse schema.
"""

from pydantic import BaseModel, Field
from typing import List

from .chat_response import ChatResponse


class ChatListResponse(BaseModel):
    """Response containing a list of chats"""
    chats: List[ChatResponse] = Field(..., description="List of chats")
    total: int = Field(..., description="Total number of chats")

