.PHONY: start stop install dev backend frontend clean

# Default target
start: install
	@echo "Starting services..."
	@make -j2 backend frontend

install:
	@echo "Installing dependencies..."
	@uv sync
	@cd frontend && npm install

backend:
	@echo "Starting backend on http://localhost:8000"
	@mkdir -p data
	@uv run uvicorn backend.main:app --reload --port 8000

frontend:
	@echo "Starting frontend on http://localhost:3000"
	@cd frontend && npm run dev

stop:
	@echo "Stopping services..."
	@pkill -f "uvicorn backend.main:app" || true
	@pkill -f "next dev" || true

clean:
	@rm -rf backend/__pycache__ data/*.db
	@rm -rf frontend/node_modules frontend/.next
	@rm -rf .venv

dev: start
