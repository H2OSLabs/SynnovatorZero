# Synnovator 协创者

A creative collaboration platform for hackathons, competitions, and community events.

## Tech Stack

- **Frontend**: Next.js 14 + React 18 + TypeScript + shadcn/ui
- **Backend**: FastAPI + SQLAlchemy + Pydantic
- **Database**: SQLite (with Alembic migrations)
- **Theme**: Neon Forge (dark theme with lime green accents)

## Quick Start

```bash
# Start all services
make start

# Or start individually
make backend   # FastAPI on http://localhost:8000
make frontend  # Next.js on http://localhost:3000
```

## Project Structure

```
.
├── app/                    # FastAPI backend
│   ├── crud/               # CRUD operations
│   ├── models/             # SQLAlchemy models
│   ├── routers/            # API route handlers
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic services
│   └── tests/              # Pytest test suite (327 tests)
├── frontend/               # Next.js frontend
│   ├── app/                # App router pages
│   ├── components/         # React components
│   │   ├── ui/             # shadcn/ui base components
│   │   ├── auth/           # LoginForm, RegisterForm
│   │   ├── user/           # UserFollowButton, FollowersList, FollowingList
│   │   ├── category/       # CategoryStageView, CategoryTrackView
│   │   └── notification/   # NotificationDropdown
│   └── lib/                # API client & types
├── alembic/                # Database migrations
├── docs/                   # Documentation
├── specs/                  # Design specs & UI assets
└── plans/                  # Implementation plans
```

## API Endpoints

### Core Resources

| Resource | Endpoints |
|----------|-----------|
| Users | `GET/POST /api/users`, `GET/PATCH/DELETE /api/users/{id}` |
| Posts | `GET/POST /api/posts`, `GET/PATCH/DELETE /api/posts/{id}` |
| Categories | `GET/POST /api/categories`, `GET/PATCH/DELETE /api/categories/{id}` |
| Groups | `GET/POST /api/groups`, `GET/PATCH/DELETE /api/groups/{id}` |
| Resources | `GET/POST /api/resources`, `GET/PATCH/DELETE /api/resources/{id}` |
| Rules | `GET/POST /api/rules`, `GET/PATCH/DELETE /api/rules/{id}` |

### Auth

| Endpoint | Description |
|----------|-------------|
| `POST /api/auth/login` | Login (returns user_id for X-User-Id header) |
| `POST /api/auth/logout` | Logout |
| `POST /api/auth/refresh` | Refresh token (not implemented) |

### User Relations

| Endpoint | Description |
|----------|-------------|
| `POST /api/users/{id}/follow` | Follow a user |
| `DELETE /api/users/{id}/follow` | Unfollow a user |
| `GET /api/users/{id}/followers` | List followers |
| `GET /api/users/{id}/following` | List following |
| `POST /api/users/{id}/block` | Block a user |
| `DELETE /api/users/{id}/block` | Unblock a user |
| `GET /api/users/{id}/is-friend/{other_id}` | Check friendship |

### Notifications

| Endpoint | Description |
|----------|-------------|
| `GET /api/notifications` | List notifications (with pagination & filters) |
| `GET /api/notifications/{id}` | Get notification |
| `PATCH /api/notifications/{id}` | Mark as read |
| `GET /api/notifications/unread-count` | Get unread count |
| `POST /api/notifications/read-all` | Mark all as read |

### Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Authentication

Currently uses header-based authentication:
```
X-User-Id: <user_id>
```

> Note: JWT authentication is planned for a future release.

## Development

### Run Tests

```bash
# Run all tests
uv run pytest app/tests/ -v

# Run specific test file
uv run pytest app/tests/test_auth.py -v

# Run with coverage
uv run pytest app/tests/ --cov=app
```

### Database Migrations

```bash
# Generate migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback
uv run alembic downgrade -1
```

### Add Dependencies

```bash
# Python
uv add <package>

# Node.js
cd frontend && npm install <package>
```

## Commands

| Command | Description |
|---------|-------------|
| `make start` | Install deps & start all services |
| `make stop` | Stop all services |
| `make backend` | Start backend only |
| `make frontend` | Start frontend only |
| `make clean` | Remove build artifacts |

## Design System

The frontend uses the **Neon Forge** theme:
- Primary: Lime Green `#BBFD3B`
- Background: Near Black `#181818`
- Card: Dark Gray `#222222`
- Text: White `#FFFFFF` / Light Gray `#DCDCDC` / Muted `#8E8E8E`

View component demos at http://localhost:3000/demo

## License

Private - H2OSLabs
