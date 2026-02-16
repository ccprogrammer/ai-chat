"""
User ORM model.
"""

from datetime import datetime
import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

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

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

