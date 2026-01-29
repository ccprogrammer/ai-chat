"""
Memory/Message service - now uses database via repository
"""
from typing import List
from sqlalchemy.orm import Session
from app.repositories.message_repository import MessageRepository


def add_message(db: Session, chat_id: str, role: str, content: str):
    """
    Add a message to a chat conversation
    """
    return MessageRepository.add_message(db, chat_id, role, content)


def get_conversation(db: Session, chat_id: str, limit: int = 50) -> List[dict]:
    """
    Get conversation messages formatted for AI API
    """
    return MessageRepository.get_chat_messages_for_ai(db, chat_id, limit)
