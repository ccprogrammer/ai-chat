"""
FastAPI auth dependencies (JWT bearer).
"""

import logging
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.repositories.auth_repository import UserRepository

logger = logging.getLogger("app.auth")

# Both schemes so Swagger can use either: paste token (Bearer) or username/password (OAuth2)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
http_bearer = HTTPBearer(auto_error=False)


def _get_token(credentials: Optional[HTTPAuthorizationCredentials], oauth2_token: Optional[str]) -> str:
    """Get token from either Bearer header or OAuth2 (Swagger form)."""
    if credentials is not None:
        logger.info("Auth: token from Bearer header (len=%d)", len(credentials.credentials))
        return credentials.credentials
    if oauth2_token is not None:
        logger.info("Auth: token from OAuth2 (len=%d)", len(oauth2_token))
        return oauth2_token
    logger.warning("Auth: NO TOKEN – neither Bearer header nor OAuth2 present")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
    oauth2_token: Optional[str] = Depends(oauth2_scheme),
):
    token = _get_token(credentials, oauth2_token)
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            logger.warning("Auth: token has no 'sub' claim")
            raise ValueError("Missing subject")
        logger.info("Auth: token decoded OK, user_id=%s", user_id)
    except Exception as e:
        logger.warning("Auth: token decode failed – %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = UserRepository.get_by_id(db, user_id)
    if not user:
        logger.warning("Auth: user_id=%s not found in DB", user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info("Auth: OK user=%s", user.email)
    return user


def get_current_admin(user=Depends(get_current_user)):
    """Require the current user to be an admin (role=admin)."""
    if user.role == "admin":
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin access required",
    )

