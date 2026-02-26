"""
API endpoint for sending messages to AI in a chat
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.schemas import ChatRequest, ChatMessageResponse
from app.services.ai_service import chat_with_ai
from app.repositories.chat_repository import ChatRepository
router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatMessageResponse)
def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Send a message to AI. If chat_id is omitted or invalid, creates a new chat first.
    ChatGPT-style: single API call for both new and existing chats.
    """
    chat_id = request.chat_id
    chat = ChatRepository.get_chat_by_id(db, chat_id, current_user.id) if chat_id else None

    if not chat:
        chat = ChatRepository.create_chat(db, current_user.id, title=None)
        chat_id = chat.id

    reply = chat_with_ai(
        db=db,
        chat_id=chat_id,
        user_message=request.message,
        user_id=current_user.id,
    )

    return ChatMessageResponse(reply=reply, chat_id=chat_id)
