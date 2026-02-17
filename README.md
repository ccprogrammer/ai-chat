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
│   └── exceptions.py # Custom exceptions
├── models/          # Data models
│   ├── database.py  # SQLAlchemy models
│   └── schemas.py   # Pydantic schemas
├── providers/       # AI provider integrations
│   └── groq_provider.py
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

or

```bash
pip3 install -r requirements.txt
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

or

```bash
python3 -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- `POST /auth/register` - Create account (email/password)
- `POST /auth/login` - Login with JSON body (email + password), returns JWT
- `GET /auth/me` - Get current user (id, email, role); requires valid JWT
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

### Admin (admin only)

- `POST /admin/bootstrap/users/{user_id}/make-admin` - **DEV ONLY**: bootstrap a user to `role=admin` without login (use from Swagger to create the first admin)
- `GET /admin/users` - List all users
- `PATCH /admin/users/{user_id}/role` - Change a user's role (`user` or `admin`)
- `GET /admin/users/{user_id}/chats` - List all chats of a user
- `GET /admin/chats/{chat_id}/messages` - Get all messages in any chat

Admins are users whose `role` is set to `admin` in the database. New users always start with `role=\"user\"`; you can:

- In development: call `POST /admin/bootstrap/users/{user_id}/make-admin` once (from Swagger) to create the first admin.
- After that: existing admins can promote/demote users using `PATCH /admin/users/{user_id}/role`.

### Other

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Authentication (how to stay logged in)

- **Swagger UI (`/docs`)**: Click **Authorize**, enter your **email** in the _username_ field and your password, then click Authorize. All subsequent requests will send the Bearer token automatically.
- **curl / app**: After `POST /auth/login`, copy `access_token` from the response and send it in the header: `Authorization: Bearer <access_token>` on every request.

## Usage Examples

### Auth APIs

#### `POST /auth/register` – Register a new user

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

#### `POST /auth/login` – Get access token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Chat Management APIs

#### `POST /chats` – Create a new chat

```bash
curl -X POST "http://localhost:8000/chats" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Chat"
  }'
```

#### `GET /chats` – List all chats for the current user

```bash
curl "http://localhost:8000/chats" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### `GET /chats/{chat_id}` – Get a single chat

```bash
curl "http://localhost:8000/chats/CHAT_ID_HERE" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### `GET /chats/{chat_id}/messages` – Get messages in a chat

```bash
curl "http://localhost:8000/chats/CHAT_ID_HERE/messages" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### `PATCH /chats/{chat_id}` – Update chat title

```bash
curl -X PATCH "http://localhost:8000/chats/CHAT_ID_HERE" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Renamed Chat"
  }'
```

#### `DELETE /chats/{chat_id}` – Delete a chat

```bash
curl -X DELETE "http://localhost:8000/chats/CHAT_ID_HERE" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Chat Interaction APIs

#### `POST /chat` – Send a message to the AI in a chat

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "chat-uuid-here",
    "message": "Hello, AI!"
  }'
```

### Admin / Bootstrap APIs

#### `POST /admin/bootstrap/users/{email}/make-admin` – **DEV ONLY** bootstrap first admin

1. Register a user and remember their `email`.
2. Call this (no auth required, only for local development):

```bash
curl -X POST "http://localhost:8000/admin/bootstrap/users/user@example.com/make-admin"
```

### Admin APIs (require `role=admin`)

#### `GET /admin/users` – List all users

```bash
curl "http://localhost:8000/admin/users" \
  -H "Authorization: Bearer ADMIN_TOKEN_HERE"
```

#### `PATCH /admin/users/{user_id}/role` – Change a user's role

```bash
curl -X PATCH "http://localhost:8000/admin/users/USER_ID_HERE/role" \
  -H "Authorization: Bearer ADMIN_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "admin"
  }'
```

#### `GET /admin/users/{user_id}/chats` – List a user's chats

```bash
curl "http://localhost:8000/admin/users/USER_ID_HERE/chats" \
  -H "Authorization: Bearer ADMIN_TOKEN_HERE"
```

#### `GET /admin/chats/{chat_id}/messages` – Get messages in any chat

```bash
curl "http://localhost:8000/admin/chats/CHAT_ID_HERE/messages" \
  -H "Authorization: Bearer ADMIN_TOKEN_HERE"
```

## Database

The application uses SQLite by default (can be configured via `DATABASE_URL`). The database file (`ai_chat.db`) will be created automatically on first run.

**If you already have a database** from before the admin feature: add the `role` column so existing users get a default role, e.g. in SQLite: `ALTER TABLE users ADD COLUMN role VARCHAR NOT NULL DEFAULT 'user';` (or remove the DB file to recreate from scratch).

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

### Testing (like Flutter unit/feature tests)

Tests are in `tests/`. You **don’t** test APIs one-by-one by hand: you write test code once, then run the whole suite in one command.

- **Run all tests**: `pytest` or `pytest -v` (verbose)
- **Run with coverage**: `pytest --cov=app`
- **Run one file**: `pytest tests/test_auth.py -v`
- **Run one test**: `pytest tests/test_auth.py::test_login_ok -v`

**Fixtures** (in `tests/conftest.py`):

- `client` – FastAPI `TestClient` with a **fresh in-memory DB per test** (no real DB touched).
- `auth_headers` – Registers a user, logs in, returns `{"Authorization": "Bearer <token>"}` so you can call protected endpoints.

**Adding tests for new APIs**: Add a test file (e.g. `tests/test_chat_messages.py`) and use `client` and `auth_headers` the same way. One test per behavior (e.g. “create chat without auth → 401”, “create with auth → 201”). Then `pytest` runs everything in seconds.

## License

MIT – see the `LICENSE` file for full text.
