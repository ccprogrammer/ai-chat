from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.core.enum import AIModel


# Chat Management Schemas
class ChatCreateRequest(BaseModel):
    """Request to create a new chat"""
    user_id: str = Field(..., description="Unique identifier for the user")
    title: Optional[str] = Field(None, description="Optional title for the chat")


class ChatUpdateRequest(BaseModel):
    """Request to update a chat title"""
    title: str = Field(..., min_length=1, max_length=200, description="New title for the chat")


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


class ChatListResponse(BaseModel):
    """Response containing a list of chats"""
    chats: List[ChatResponse] = Field(..., description="List of chats")
    total: int = Field(..., description="Total number of chats")


# Message Schemas
class MessageResponse(BaseModel):
    """Message information response"""
    id: int = Field(..., description="Message ID")
    chat_id: str = Field(..., description="Chat this message belongs to")
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    created_at: datetime = Field(..., description="When the message was created")

    class Config:
        from_attributes = True


# Chat Interaction Schemas
class ChatRequest(BaseModel):
    """
    Incoming chat message from the client (Flutter, Web, etc.)
    """
    chat_id: str = Field(
        ...,
        description="Unique identifier for the chat/conversation"
    )
    user_id: str = Field(
        ...,
        description="Unique identifier for the user (for authorization)"
    )
    message: str = Field(
        ...,
        min_length=1,
        description="User message to the AI"
    )
    model: AIModel = Field(
        default=AIModel.FAST,
        description="AI model preference selected by the user"
    )


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
