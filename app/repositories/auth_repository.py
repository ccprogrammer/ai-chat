"""
Repository layer for Auth operations
"""
from app.models.database import User
from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password


class UserRepository:
    """
    Repository for managing User entities.
    """

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(db: Session, user_id: str) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, email: str, password: str, role: str = "user") -> User:
        user = User(email=email, hashed_password=hash_password(password), role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_role(db: Session, user_id: str, role: str) -> Optional[User]:
        """Update a user's role (e.g. promote to admin)."""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            return None
        user.role = role
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_role_by_email(db: Session, email: str, role: str) -> Optional[User]:
        """Update a user's role by email (for bootstrap/dev helpers)."""
        user = UserRepository.get_by_email(db, email)
        if not user:
            return None
        user.role = role
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_all_users(db: Session, limit: int = 100, offset: int = 0):
        """Return all users (for admin)."""
        return db.query(User).order_by(User.created_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def count_users(db: Session) -> int:
        """Total user count (for admin)."""
        return db.query(User).count()

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        user = UserRepository.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def increment_token_version(db: Session, user_id: str) -> None:
        """Increment token_version to invalidate all existing tokens for this user."""
        user = UserRepository.get_by_id(db, user_id)
        if user:
            current = int(user.token_version) if user.token_version else 0
            user.token_version = str(current + 1)
            db.commit()
