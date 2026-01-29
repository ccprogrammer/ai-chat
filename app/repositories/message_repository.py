"""
Repository layer for Messages operations
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import Chat, Message
from datetime import datetime


class MessageRepository:
    """
    Repository for managing Message entities
    """

    @staticmethod
    def add_message(db: Session, chat_id: str, role: str, content: str) -> Message:
        """
        Add a message to a chat
        """
        message = Message(chat_id=chat_id, role=role, content=content)
        db.add(message)
        
        # Update chat's updated_at timestamp
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if chat:
            chat.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def get_chat_messages(db: Session, chat_id: str, limit: Optional[int] = None) -> List[Message]:
        """
        Get all messages for a chat, ordered by creation time
        """
        query = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at)
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_chat_messages_for_ai(db: Session, chat_id: str, limit: int = 50) -> List[dict]:
        """
        Get messages formatted for AI API (list of dicts with role and content)
        """
        messages = MessageRepository.get_chat_messages(db, chat_id, limit)
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

