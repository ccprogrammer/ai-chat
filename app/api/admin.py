"""
Admin-only API: list all users, view any user's chats, view any chat's messages,
and update user roles (promote/demote).
Requires role=admin (stored in the users.role column).
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_admin
from app.repositories.auth_repository import UserRepository
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository
from app.models.schemas.auth import UserResponse, UserRoleUpdateRequest
from app.models.schemas import ChatResponse, ChatListResponse, MessageResponse
from app.core.exceptions import UserNotFoundError, ChatNotFoundError

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/bootstrap/users/{user_id}/make-admin", response_model=UserResponse)
def bootstrap_make_admin(
    user_id: str,
    db: Session = Depends(get_db),
):
    """
    DEVELOPMENT ONLY: make a user admin without being logged in.

    Use this to bootstrap the first admin from Swagger:
    1. Register a user via /auth/register and copy their id.
    2. Call this endpoint with that id to set role='admin'.

    WARNING: Do NOT expose this in a real production environment.
    """
    user = UserRepository.update_role(db, user_id, "admin")
    if not user:
        raise UserNotFoundError(user_id)
    return user


@router.get("/users", response_model=List[UserResponse])
def list_all_users(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """List all users (admin only)."""
    users = UserRepository.get_all_users(db, limit=limit, offset=offset)
    return users


@router.patch("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: str,
    request: UserRoleUpdateRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Update a user's role (e.g. promote to admin). Admin only."""
    user = UserRepository.update_role(db, user_id, request.role)
    if not user:
        raise UserNotFoundError(user_id)
    return user


@router.get("/users/{user_id}/chats", response_model=ChatListResponse)
def list_user_chats(
    user_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """List all chats of a specific user (admin only)."""
    if UserRepository.get_by_id(db, user_id) is None:
        raise UserNotFoundError(user_id)
    chats = ChatRepository.get_user_chats(db, user_id, limit=limit, offset=offset)
    chat_responses = []
    for chat in chats:
        message_count = MessageRepository.get_message_count(db, chat.id)
        chat_responses.append(ChatResponse(
            id=chat.id,
            user_id=chat.user_id,
            title=chat.title,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
            message_count=message_count,
        ))
    total = len(ChatRepository.get_user_chats(db, user_id, limit=1000))
    return ChatListResponse(chats=chat_responses, total=total)


@router.get("/chats/{chat_id}/messages", response_model=List[MessageResponse])
def get_chat_messages(
    chat_id: str,
    limit: int = Query(500, ge=1, le=1000),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Get all messages in a chat (any user's chat; admin only)."""
    chat = ChatRepository.get_chat_by_id_any(db, chat_id)
    if not chat:
        raise ChatNotFoundError(chat_id)
    messages = MessageRepository.get_chat_messages(db, chat_id, limit=limit)
    return messages
