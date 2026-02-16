"""
Pydantic schemas package.
Exports chat- and message-related schemas for backwards-compatible imports like:
    from app.models.schemas import ChatRequest, ChatResponse, MessageResponse
"""

from .chat import (  # noqa: F401
    ChatCreateRequest,
    ChatUpdateRequest,
    ChatResponse,
    ChatListResponse,
    ChatRequest,
    ChatMessageResponse,
)
from .message import MessageResponse  # noqa: F401

