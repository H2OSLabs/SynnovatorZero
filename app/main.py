"""Synnovator API Server"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import users, resources, categories, posts, rules, groups, interactions, admin

# Import all models so Base.metadata knows about them
import app.models  # noqa: F401

# Create tables
Base.metadata.create_all(bind=engine)

# App
app = FastAPI(
    title="Synnovator API",
    description="协创者 - Creative Collaboration Platform API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


# Include routers
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(resources.router, prefix="/api", tags=["resources"])
app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(posts.router, prefix="/api", tags=["posts"])
app.include_router(rules.router, prefix="/api", tags=["rules"])
app.include_router(groups.router, prefix="/api", tags=["groups"])
app.include_router(interactions.router, prefix="/api", tags=["interactions"])
app.include_router(admin.router, prefix="/api", tags=["admin"])
