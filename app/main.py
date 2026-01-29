"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.api.chats import router as chats_router
from app.core.database import init_db

# Initialize database on startup
init_db()

# Create FastAPI app
app = FastAPI(
    title="AI Chat Backend",
    description="A professional AI chat backend with multi-chat support",
    version="1.0.0"
)

# Configure CORS (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chats_router)  # Chat management endpoints
app.include_router(chat_router)  # Chat message endpoint


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "AI Chat Backend API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
