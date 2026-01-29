"""
API endpoint for sending messages to AI in a chat
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schemas import ChatRequest, ChatMessageResponse
from app.services.ai_service import chat_with_ai
from app.repositories.chat_repository import ChatRepository
from app.core.exceptions import ChatNotFoundError

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatMessageResponse)
def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Send a message to AI in a specific chat
    
    Verifies that the chat exists and belongs to the user before processing.
    """
    # Verify chat exists and belongs to user
    chat = ChatRepository.get_chat_by_id(db, request.chat_id, request.user_id)
    if not chat:
        raise ChatNotFoundError(request.chat_id)
    
    # Get AI reply
    reply = chat_with_ai(
        db=db,
        chat_id=request.chat_id,
        user_message=request.message,
        model=request.model.value
    )
    
    return ChatMessageResponse(reply=reply, chat_id=request.chat_id)
