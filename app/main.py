"""
Main FastAPI application
"""
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.chats import router as chats_router
from app.core.database import init_db

# Configure logging so uvicorn terminal shows our debug output
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("app")

# Initialize database on startup
init_db()

# Create FastAPI app
app = FastAPI(
    title="AI Chat Backend",
    description=(
        "A professional AI chat backend with multi-chat support.\n\n"
        "**To call protected endpoints (e.g. POST /chats):**\n"
        "1. Click the **Authorize** button (lock icon) above.\n"
        "2. Either: (a) Enter your **email** in the *username* field and **password**, then click Authorize, "
        "or (b) Call **POST /auth/login** first, copy the **access_token** from the response, then in Authorize choose **Bearer** and paste the token.\n"
        "3. Try the request again — the token will be sent automatically."
    ),
    version="1.0.0",
)

# Configure CORS (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware – see each request and if Authorization header is present
@app.middleware("http")
async def log_requests(request: Request, call_next):
    auth = request.headers.get("Authorization", "(none)")
    has_bearer = auth.startswith("Bearer ") if auth != "(none)" else False
    logger.info("→ %s %s | Auth: %s", request.method, request.url.path, "Bearer present" if has_bearer else "MISSING")
    response = await call_next(request)
    return response

# Include routers
app.include_router(auth_router)  # Auth endpoints
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
