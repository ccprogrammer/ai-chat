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
