"""
AI Service - handles chat interactions with AI
"""
from sqlalchemy.orm import Session
from app.services.memory_service import add_message, get_conversation
from app.providers.groq_provider import generate_chat_completion
from app.core.config import SYSTEM_PROMPT
from app.core.exceptions import AIProviderError


def chat_with_ai(db: Session, chat_id: str, user_message: str, model: str) -> str:
    """
    Process a user message and get AI response
    
    Args:
        db: Database session
        chat_id: ID of the chat conversation
        user_message: User's message
        model: AI model to use
        
    Returns:
        AI's reply
        
    Raises:
        AIProviderError: If AI service fails
    """
    try:
        # Add user message to conversation
        add_message(db, chat_id, "user", user_message)

        # Build messages list for AI (system prompt + conversation history)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(get_conversation(db, chat_id))

        # Get AI reply
        ai_reply = generate_chat_completion(messages, model)

        # Save AI reply to conversation
        add_message(db, chat_id, "assistant", ai_reply)
        
        return ai_reply
    except Exception as e:
        # Re-raise as AIProviderError for proper HTTP handling
        raise AIProviderError(f"Failed to get AI response: {str(e)}")
