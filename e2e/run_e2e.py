#!/usr/bin/env python3
"""Run E2E tests with managed backend and frontend servers.

This script uses the with_server.py helper from webapp-testing skill to:
1. Start the backend server (FastAPI on port 8000)
2. Start the frontend server (Next.js on port 3000)
3. Run pytest E2E tests
4. Shut down servers when done

Usage:
    # Run all E2E tests
    python e2e/run_e2e.py

    # Run specific test file
    python e2e/run_e2e.py test_home.py

    # Run with verbose output
    python e2e/run_e2e.py -v

    # Run with screenshot on failure
    python e2e/run_e2e.py --screenshot
"""
import os
import sys
import subprocess
from pathlib import Path


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
E2E_DIR = PROJECT_ROOT / "e2e"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
WITH_SERVER_SCRIPT = Path.home() / ".claude/plugins/cache/anthropic-agent-skills/document-skills/69c0b1a06741/skills/webapp-testing/scripts/with_server.py"


def main():
    # Parse arguments
    args = sys.argv[1:]
    test_args = []
    extra_pytest_args = ["-v"]

    for arg in args:
        if arg.startswith("-"):
            extra_pytest_args.append(arg)
        elif arg.endswith(".py"):
            test_args.append(str(E2E_DIR / arg))
        else:
            test_args.append(arg)

    # Default to all E2E tests if none specified
    if not test_args:
        test_args = [str(E2E_DIR)]

    # Build the command
    # Backend: uv run uvicorn app.main:app --port 8000
    # Frontend: npm run dev -- -p 3000
    backend_cmd = "uv run uvicorn app.main:app --port 8000"
    frontend_cmd = f"cd {FRONTEND_DIR} && npm run dev -- -p 3000"
    pytest_cmd = f"uv run pytest {' '.join(test_args)} {' '.join(extra_pytest_args)}"

    cmd = [
        "python3",
        str(WITH_SERVER_SCRIPT),
        "--server", backend_cmd,
        "--port", "8000",
        "--server", frontend_cmd,
        "--port", "3000",
        "--timeout", "60",
        "--",
        *pytest_cmd.split(),
    ]

    print(f"Running E2E tests...")
    print(f"Backend: {backend_cmd}")
    print(f"Frontend: {frontend_cmd}")
    print(f"Tests: {pytest_cmd}")
    print("-" * 60)

    # Change to project root
    os.chdir(PROJECT_ROOT)

    # Run the command
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
