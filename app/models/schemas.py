from pydantic import BaseModel, Field
from app.core.enum import AIModel


class ChatRequest(BaseModel):
    """
    Incoming chat message from the client (Flutter, Web, etc.)
    """
    user_id: str = Field(
        ...,
        description="Unique identifier for the user or session"
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


class ChatResponse(BaseModel):
    """
    AI reply returned to the client
    """
    reply: str = Field(
        ...,
        description="AI-generated response"
    )
