"""
Repository layer for Chat operations
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import Chat, Message
from datetime import datetime


class ChatRepository:
    """
    Repository for managing Chat entities
    """

    @staticmethod
    def create_chat(db: Session, user_id: str, title: Optional[str] = None) -> Chat:
        """
        Create a new chat for a user
        """
        chat = Chat(user_id=user_id, title=title)
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat

    @staticmethod
    def get_chat_by_id(db: Session, chat_id: str, user_id: str) -> Optional[Chat]:
        """
        Get a specific chat by ID, ensuring it belongs to the user
        """
        return db.query(Chat).filter(
            Chat.id == chat_id,
            Chat.user_id == user_id
        ).first()

    @staticmethod
    def get_user_chats(db: Session, user_id: str, limit: int = 50, offset: int = 0) -> List[Chat]:
        """
        Get all chats for a user, ordered by most recent first
        """
        return db.query(Chat).filter(
            Chat.user_id == user_id
        ).order_by(Chat.updated_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def delete_chat(db: Session, chat_id: str, user_id: str) -> bool:
        """
        Delete a chat (and all its messages via cascade)
        Returns True if deleted, False if not found
        """
        chat = ChatRepository.get_chat_by_id(db, chat_id, user_id)
        if chat:
            db.delete(chat)
            db.commit()
            return True
        return False

    @staticmethod
    def update_chat_title(db: Session, chat_id: str, user_id: str, title: str) -> Optional[Chat]:
        """
        Update the title of a chat
        """
        chat = ChatRepository.get_chat_by_id(db, chat_id, user_id)
        if chat:
            chat.title = title
            chat.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(chat)
        return chat

