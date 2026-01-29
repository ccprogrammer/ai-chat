from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.ai_service import chat_with_ai

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = chat_with_ai(
        user_id=request.user_id,
        user_message=request.message,
        model=request.model.value
    )
    return ChatResponse(reply=reply)
