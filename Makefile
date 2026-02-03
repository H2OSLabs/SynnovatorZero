.PHONY: start stop install dev backend frontend clean resetdb seed test test-unit test-e2e

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
	@uv run python -m uvicorn app.main:app --reload --port 8000

frontend:
	@echo "Starting frontend on http://localhost:3000"
	@cd frontend && npm run dev

stop:
	@echo "Stopping services..."
	@pkill -f "uvicorn app.main:app" || true
	@pkill -f "next dev" || true

resetdb:
	@echo "Resetting database (schema changed)..."
	@rm -f data/synnovator.db
	@echo "Done. Run 'make start' to recreate tables."

seed:
	@echo "Seeding development data..."
	@uv run python scripts/seed_dev_data.py

clean:
	@rm -rf app/__pycache__ data/*.db
	@rm -rf frontend/node_modules frontend/.next
	@rm -rf .venv

dev: start

# Testing targets
test: test-unit
	@echo "All tests passed!"

test-unit:
	@echo "Running unit tests..."
	@uv run pytest app/tests/ -v

test-e2e:
	@echo "Running E2E tests (requires servers)..."
	@python3 e2e/run_e2e.py
