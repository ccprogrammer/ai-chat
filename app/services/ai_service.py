"""
AI Service - handles chat interactions with AI
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.services.memory_service import add_message, get_conversation
from app.repositories.message_repository import MessageRepository
from app.repositories.chat_repository import ChatRepository
from app.providers.groq_provider import generate_chat_completion, generate_chat_title
from app.core.config import SYSTEM_PROMPT
from app.core.exceptions import AIProviderError


def chat_with_ai(
    db: Session,
    chat_id: str,
    user_message: str,
    user_id: Optional[str] = None,
) -> str:
    """
    Process a user message and get AI response (always uses fast model).
    If this is the first message in the chat and user_id is provided,
    the chat title is auto-generated from the message (AI-generated short title).

    Args:
        db: Database session
        chat_id: ID of the chat conversation
        user_message: User's message
        user_id: Optional; required to auto-set chat title on first message

    Returns:
        AI's reply

    Raises:
        AIProviderError: If AI service fails
    """
    try:
        is_first_message = MessageRepository.get_message_count(db, chat_id) == 0

        # Add user message to conversation
        add_message(db, chat_id, "user", user_message)

        # Build messages list for AI (system prompt + conversation history)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(get_conversation(db, chat_id))

        # Get AI reply (fast model only)
        ai_reply = generate_chat_completion(messages)

        # Save AI reply to conversation
        add_message(db, chat_id, "assistant", ai_reply)

        # Auto-generate chat title from first message (reference/summary, not copy-paste)
        if is_first_message and user_id:
            try:
                title = generate_chat_title(user_message)
                ChatRepository.update_chat_title(db, chat_id, user_id, title)
            except Exception:
                pass  # keep existing title (e.g. None or "New chat") on failure

        return ai_reply
    except Exception as e:
        # Re-raise as AIProviderError for proper HTTP handling
        raise AIProviderError(f"Failed to get AI response: {str(e)}")
