"""
Custom exception classes for the application
"""
from fastapi import HTTPException, status


class ChatNotFoundError(HTTPException):
    """Raised when a chat is not found"""
    def __init__(self, chat_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id '{chat_id}' not found"
        )


class UnauthorizedChatAccessError(HTTPException):
    """Raised when user tries to access a chat that doesn't belong to them"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this chat"
        )


class AIProviderError(HTTPException):
    """Raised when AI provider fails"""
    def __init__(self, message: str = "AI service temporarily unavailable"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=message
        )
