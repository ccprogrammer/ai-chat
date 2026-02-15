# AI Chat Backend

A professional, production-ready AI chat backend built with FastAPI, supporting multiple concurrent chat conversations.

## Features

- ✅ **Multiple Chat Support**: Create and manage multiple chat conversations per user
- ✅ **Persistent Storage**: SQLite database with SQLAlchemy ORM
- ✅ **Auth (Email/Password)**: Register/login and protect chat endpoints with JWT Bearer tokens
- ✅ **RESTful API**: Clean, well-documented REST endpoints
- ✅ **Professional Structure**: Organized codebase following best practices
- ✅ **Error Handling**: Comprehensive error handling with custom exceptions
- ✅ **Type Safety**: Full type hints and Pydantic models
- ✅ **API Documentation**: Auto-generated OpenAPI/Swagger docs

## Project Structure

```
app/
├── api/              # API endpoints/routes
│   ├── chat.py      # Chat message endpoint
│   └── chats.py     # Chat management endpoints
├── core/            # Core utilities
│   ├── config.py    # Configuration
│   ├── database.py  # Database setup
│   ├── enum.py      # Enumerations
│   └── exceptions.py # Custom exceptions
├── models/          # Data models
│   ├── database.py  # SQLAlchemy models
│   └── schemas.py   # Pydantic schemas
├── providers/       # AI provider integrations
│   ├── groq_provider.py
│   └── model_registry.py
├── repositories/    # Data access layer
│   └── chat_repository.py
├── services/        # Business logic
│   ├── ai_service.py
│   └── memory_service.py
└── main.py          # FastAPI application
```

## Setup

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Set up environment variables**:
   Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=sqlite:///./ai_chat.db  # Optional, defaults to this
```

3. **Run the application**:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- `POST /auth/register` - Create account (email/password)
- `POST /auth/login` - Login with JSON body (email + password), returns JWT
- `POST /auth/token` - OAuth2 token endpoint (form: username=email, password); used by Swagger "Authorize"

### Chat Management

- `POST /chats` - Create a new chat
- `GET /chats` - List all chats for the current user
- `GET /chats/{chat_id}` - Get a specific chat (current user)
- `GET /chats/{chat_id}/messages` - Get all messages in a chat (current user)
- `PATCH /chats/{chat_id}` - Update chat title (current user)
- `DELETE /chats/{chat_id}` - Delete a chat (current user)

### Chat Interaction

- `POST /chat` - Send a message to AI in a chat

### Other

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Authentication (how to stay logged in)

- **Swagger UI (`/docs`)**: Click **Authorize**, enter your **email** in the *username* field and your password, then click Authorize. All subsequent requests will send the Bearer token automatically.
- **curl / app**: After `POST /auth/login`, copy `access_token` from the response and send it in the header: `Authorization: Bearer <access_token>` on every request.

## Usage Examples

### Register

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Login (get token)

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Create a Chat

```bash
curl -X POST "http://localhost:8000/chats" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Chat"
  }'
```

### Send a Message

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "chat-uuid-here",
    "message": "Hello, AI!",
    "model": "fast"
  }'
```

### List All Chats

```bash
curl "http://localhost:8000/chats" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Database

The application uses SQLite by default (can be configured via `DATABASE_URL`). The database file (`ai_chat.db`) will be created automatically on first run.

### Database Schema

- **chats**: Stores chat conversations
  - `id` (UUID): Primary key
  - `user_id`: User who owns the chat
  - `title`: Optional chat title
  - `created_at`, `updated_at`: Timestamps

- **messages**: Stores messages within chats
  - `id`: Primary key
  - `chat_id`: Foreign key to chats
  - `role`: "user" or "assistant"
  - `content`: Message content
  - `created_at`: Timestamp

## Development

### Code Structure Principles

- **Separation of Concerns**: API routes, business logic, and data access are separated
- **Repository Pattern**: Data access is abstracted through repositories
- **Dependency Injection**: Database sessions are injected via FastAPI dependencies
- **Type Safety**: Full type hints throughout the codebase
- **Error Handling**: Custom exceptions for better error messages

### Adding New Features

1. **New API Endpoint**: Add to `app/api/`
2. **New Business Logic**: Add to `app/services/`
3. **New Data Model**: Add to `app/models/database.py` and schema to `app/models/schemas.py`
4. **New Repository Method**: Add to `app/repositories/`

## License

MIT
