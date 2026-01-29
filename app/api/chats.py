"""
API endpoints for chat management (create, list, get, update, delete)
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.repositories.chat_repository import ChatRepository, MessageRepository
from app.models.schemas import (
    ChatCreateRequest,
    ChatUpdateRequest,
    ChatResponse,
    ChatListResponse,
    MessageResponse
)
from app.core.exceptions import ChatNotFoundError, UnauthorizedChatAccessError

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("", response_model=ChatResponse, status_code=201)
def create_chat(
    request: ChatCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new chat for a user
    """
    chat = ChatRepository.create_chat(db, request.user_id, request.title)
    
    # Return chat with message count
    return ChatResponse(
        id=chat.id,
        user_id=chat.user_id,
        title=chat.title,
        created_at=chat.created_at,
        updated_at=chat.updated_at,
        message_count=0
    )


@router.get("", response_model=ChatListResponse)
def list_chats(
    user_id: str = Query(..., description="User ID to get chats for"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of chats to return"),
    offset: int = Query(0, ge=0, description="Number of chats to skip"),
    db: Session = Depends(get_db)
):
    """
    Get all chats for a user
    """
    chats = ChatRepository.get_user_chats(db, user_id, limit, offset)
    
    # Get message count for each chat
    chat_responses = []
    for chat in chats:
        message_count = len(MessageRepository.get_chat_messages(db, chat.id))
        chat_responses.append(ChatResponse(
            id=chat.id,
            user_id=chat.user_id,
            title=chat.title,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
            message_count=message_count
        ))
    
    # Get total count (simplified - in production, use count query)
    total = len(ChatRepository.get_user_chats(db, user_id, limit=1000))
    
    return ChatListResponse(chats=chat_responses, total=total)


@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(
    chat_id: str,
    user_id: str = Query(..., description="User ID for authorization"),
    db: Session = Depends(get_db)
):
    """
    Get a specific chat by ID
    """
    chat = ChatRepository.get_chat_by_id(db, chat_id, user_id)
    if not chat:
        raise ChatNotFoundError(chat_id)
    
    message_count = len(MessageRepository.get_chat_messages(db, chat_id))
    
    return ChatResponse(
        id=chat.id,
        user_id=chat.user_id,
        title=chat.title,
        created_at=chat.created_at,
        updated_at=chat.updated_at,
        message_count=message_count
    )


@router.get("/{chat_id}/messages", response_model=list[MessageResponse])
def get_chat_messages(
    chat_id: str,
    user_id: str = Query(..., description="User ID for authorization"),
    limit: Optional[int] = Query(None, ge=1, le=500, description="Maximum number of messages to return"),
    db: Session = Depends(get_db)
):
    """
    Get all messages for a specific chat
    """
    # Verify chat exists and belongs to user
    chat = ChatRepository.get_chat_by_id(db, chat_id, user_id)
    if not chat:
        raise ChatNotFoundError(chat_id)
    
    messages = MessageRepository.get_chat_messages(db, chat_id, limit)
    return messages


@router.patch("/{chat_id}", response_model=ChatResponse)
def update_chat(
    chat_id: str,
    request: ChatUpdateRequest,
    user_id: str = Query(..., description="User ID for authorization"),
    db: Session = Depends(get_db)
):
    """
    Update a chat's title
    """
    chat = ChatRepository.update_chat_title(db, chat_id, user_id, request.title)
    if not chat:
        raise ChatNotFoundError(chat_id)
    
    message_count = len(MessageRepository.get_chat_messages(db, chat_id))
    
    return ChatResponse(
        id=chat.id,
        user_id=chat.user_id,
        title=chat.title,
        created_at=chat.created_at,
        updated_at=chat.updated_at,
        message_count=message_count
    )


@router.delete("/{chat_id}", status_code=204)
def delete_chat(
    chat_id: str,
    user_id: str = Query(..., description="User ID for authorization"),
    db: Session = Depends(get_db)
):
    """
    Delete a chat and all its messages
    """
    deleted = ChatRepository.delete_chat(db, chat_id, user_id)
    if not deleted:
        raise ChatNotFoundError(chat_id)
    
    return None
