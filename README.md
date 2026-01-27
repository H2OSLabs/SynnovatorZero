# SynnovatorZero

Synnovator Rebuild from Scratch

## Tech Stack

- **Frontend**: Next.js 14 + React 18 + TypeScript
- **Backend**: FastAPI + SQLAlchemy
- **Database**: SQLite

## Quick Start

```bash
make start
```

This will:
1. Install dependencies (Python & Node.js)
2. Start backend on http://localhost:8000
3. Start frontend on http://localhost:3000

## Project Structure

```
.
├── pyproject.toml      # Python dependencies & project config
├── Makefile            # Build commands
├── backend/            # FastAPI backend (Python package)
│   ├── __init__.py
│   └── main.py         # API entry point
├── frontend/           # Next.js frontend
│   ├── app/            # App router pages
│   └── package.json    # Node.js dependencies
└── data/               # SQLite database (gitignored)
```

## Dependency Management

- **Python**: Dependencies defined in `pyproject.toml`, managed by [uv](https://docs.astral.sh/uv/)
- **Node.js**: Dependencies defined in `frontend/package.json`, managed by npm

## API Endpoints

- `GET /health` - Health check
- `GET /api/items` - List all items
- `POST /api/items` - Create item
- `DELETE /api/items/{id}` - Delete item
- `GET /docs` - Swagger UI

## Commands

| Command | Description |
|---------|-------------|
| `make start` | Install deps & start all services |
| `make stop` | Stop all services |
| `make backend` | Start backend only |
| `make frontend` | Start frontend only |
| `make clean` | Remove build artifacts |
