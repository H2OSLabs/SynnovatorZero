"""Test configuration — in-memory SQLite for isolation"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def make_auth_headers(user_id: int) -> dict:
    """Create authentication headers for a user."""
    return {"X-User-Id": str(user_id)}


@pytest.fixture()
def auth_headers():
    """Factory fixture to create auth headers for a given user_id."""
    return make_auth_headers


@pytest.fixture()
def admin_user(client):
    """Create an admin user and return their data."""
    resp = client.post("/api/users", json={
        "username": "test_admin",
        "email": "test_admin@example.com",
        "role": "admin",
    })
    return resp.json()


@pytest.fixture()
def organizer_user(client):
    """Create an organizer user and return their data."""
    resp = client.post("/api/users", json={
        "username": "test_organizer",
        "email": "test_organizer@example.com",
        "role": "organizer",
    })
    return resp.json()


@pytest.fixture()
def participant_user(client):
    """Create a participant user and return their data."""
    resp = client.post("/api/users", json={
        "username": "test_participant",
        "email": "test_participant@example.com",
        "role": "participant",
    })
    return resp.json()
