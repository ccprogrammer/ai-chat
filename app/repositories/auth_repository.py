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
    def create_user(db: Session, email: str, password: str) -> User:
        user = User(email=email, hashed_password=hash_password(password))
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        user = UserRepository.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
