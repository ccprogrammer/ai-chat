"""
Database models for Chat and Message entities
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class User(Base):
    """
    User model for authentication (email + hashed password).
    role: "user" (default) or "admin". Admins can list all users and view any user's chat history.
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")  # "user" | "admin"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


class Chat(Base):
    """
    Chat/Conversation model
    Each chat belongs to a user and contains multiple messages
    """
    __tablename__ = "chats"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=True)  # Optional title for the chat
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="chats")

    # Relationship to messages
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan", order_by="Message.created_at")

    def __repr__(self):
        return f"<Chat(id={self.id}, user_id={self.user_id}, title={self.title})>"


class Message(Base):
    """
    Message model
    Each message belongs to a chat and has a role (user/assistant) and content
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to chat
    chat = relationship("Chat", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, chat_id={self.chat_id}, role={self.role})>"
