# AI Chat Backend

A professional, production-ready AI chat backend built with FastAPI, supporting multiple concurrent chat conversations.

## Features

- ✅ **Multiple Chat Support**: Create and manage multiple chat conversations per user
- ✅ **Persistent Storage**: SQLite database with SQLAlchemy ORM
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

### Chat Management

- `POST /chats` - Create a new chat
- `GET /chats` - List all chats for a user
- `GET /chats/{chat_id}` - Get a specific chat
- `GET /chats/{chat_id}/messages` - Get all messages in a chat
- `PATCH /chats/{chat_id}` - Update chat title
- `DELETE /chats/{chat_id}` - Delete a chat

### Chat Interaction

- `POST /chat` - Send a message to AI in a chat

### Other

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Usage Examples

### Create a Chat

```bash
curl -X POST "http://localhost:8000/chats" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "title": "My First Chat"
  }'
```

### Send a Message

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "chat-uuid-here",
    "user_id": "user123",
    "message": "Hello, AI!",
    "model": "fast"
  }'
```

### List All Chats

```bash
curl "http://localhost:8000/chats?user_id=user123"
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
