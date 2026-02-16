"""
Message ORM model.
"""

from datetime import datetime

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class Message(Base):
    """
    Message model.
    Each message belongs to a chat and has a role (user/assistant) and content.
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to chat
    chat = relationship("Chat", back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, chat_id={self.chat_id}, role={self.role})>"

