"""Synnovator API Server"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import engine, Base, get_db
from app.routers import users, resources, categories, posts, rules, groups, interactions, admin, auth, notifications, meta
from app import models

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


@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get platform statistics (counts excluding soft-deleted records)"""
    user_count = db.query(func.count(models.User.id)).filter(
        models.User.deleted_at.is_(None)
    ).scalar() or 0

    category_count = db.query(func.count(models.Category.id)).filter(
        models.Category.deleted_at.is_(None)
    ).scalar() or 0

    post_count = db.query(func.count(models.Post.id)).filter(
        models.Post.deleted_at.is_(None)
    ).scalar() or 0

    return {
        "user_count": user_count,
        "category_count": category_count,
        "post_count": post_count,
    }


# Include routers
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(resources.router, prefix="/api", tags=["resources"])
app.include_router(meta.router, prefix="/api", tags=["meta"])
app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(posts.router, prefix="/api", tags=["posts"])
app.include_router(rules.router, prefix="/api", tags=["rules"])
app.include_router(groups.router, prefix="/api", tags=["groups"])
app.include_router(interactions.router, prefix="/api", tags=["interactions"])
app.include_router(admin.router, prefix="/api", tags=["admin"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(notifications.router, prefix="/api", tags=["notifications"])
