#!/usr/bin/env python3
"""
Generate OpenAPI 3.0 specification from Synnovator data schema.

Usage:
    uv run python generate_openapi.py [--output PATH] [--title TITLE] [--version VERSION]

Output:
    Writes openapi.yaml to the specified path (default: .synnovator/openapi.yaml)
"""

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def generate_openapi_spec(title: str = "Synnovator API", version: str = "1.0.0") -> dict:
    """Generate complete OpenAPI 3.0 specification for Synnovator."""

    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": title,
            "version": version,
            "description": "API for Synnovator - Activity and Competition Management Platform",
            "contact": {"name": "API Support"},
            "license": {"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
        },
        "servers": [
            {"url": "http://localhost:8000", "description": "Development server"},
            {"url": "https://api.synnovator.com", "description": "Production server"}
        ],
        "tags": _generate_tags(),
        "paths": _generate_paths(),
        "components": {
            "securitySchemes": _generate_security_schemes(),
            "schemas": _generate_schemas(),
            "parameters": _generate_common_parameters(),
            "responses": _generate_common_responses()
        },
        "security": [{"oauth2": ["read", "write"]}]
    }

    return spec


def _generate_tags() -> list:
    """Generate API tags for grouping endpoints."""
    return [
        {"name": "categories", "description": "Activity and competition categories"},
        {"name": "posts", "description": "User posts and submissions"},
        {"name": "resources", "description": "File resources and attachments"},
        {"name": "rules", "description": "Category rules and scoring criteria"},
        {"name": "users", "description": "User management"},
        {"name": "groups", "description": "Teams and groups"},
        {"name": "interactions", "description": "Likes, comments, and ratings"},
        {"name": "admin", "description": "Admin batch operations"}
    ]


def _generate_security_schemes() -> dict:
    """Generate OAuth2 security scheme."""
    return {
        "oauth2": {
            "type": "oauth2",
            "flows": {
                "authorizationCode": {
                    "authorizationUrl": "/oauth/authorize",
                    "tokenUrl": "/oauth/token",
                    "scopes": {
                        "read": "Read access to resources",
                        "write": "Write access to resources",
                        "admin": "Admin access for batch operations"
                    }
                }
            }
        },
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }


def _generate_common_parameters() -> dict:
    """Generate common query parameters."""
    return {
        "SkipParam": {
            "name": "skip",
            "in": "query",
            "schema": {"type": "integer", "default": 0, "minimum": 0},
            "description": "Number of records to skip"
        },
        "LimitParam": {
            "name": "limit",
            "in": "query",
            "schema": {"type": "integer", "default": 20, "minimum": 1, "maximum": 100},
            "description": "Maximum number of records to return"
        },
        "IncludeDeletedParam": {
            "name": "include_deleted",
            "in": "query",
            "schema": {"type": "boolean", "default": False},
            "description": "Include soft-deleted records (admin only)"
        }
    }


def _generate_common_responses() -> dict:
    """Generate common response definitions."""
    return {
        "NotFound": {
            "description": "Resource not found",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Error"}
                }
            }
        },
        "ValidationError": {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Error"}
                }
            }
        },
        "Unauthorized": {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Error"}
                }
            }
        },
        "Forbidden": {
            "description": "Permission denied",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Error"}
                }
            }
        }
    }


def _generate_schemas() -> dict:
    """Generate all OpenAPI schemas."""
    schemas = {}

    # Error schema
    schemas["Error"] = {
        "type": "object",
        "required": ["error"],
        "properties": {
            "error": {
                "type": "object",
                "required": ["code", "message"],
                "properties": {
                    "code": {"type": "string", "example": "NOT_FOUND"},
                    "message": {"type": "string", "example": "Resource not found"},
                    "details": {"type": "object", "additionalProperties": True}
                }
            }
        }
    }

    # Enums
    schemas["CategoryType"] = {
        "type": "string",
        "enum": ["competition", "operation"],
        "description": "Type of category"
    }
    schemas["CategoryStatus"] = {
        "type": "string",
        "enum": ["draft", "published", "closed"],
        "description": "Category status"
    }
    schemas["PostType"] = {
        "type": "string",
        "enum": ["profile", "team", "category", "for_category", "certificate", "general"],
        "description": "Type of post"
    }
    schemas["PostStatus"] = {
        "type": "string",
        "enum": ["draft", "pending_review", "published", "rejected"],
        "description": "Post status"
    }
    schemas["UserRole"] = {
        "type": "string",
        "enum": ["participant", "organizer", "admin"],
        "description": "User role"
    }
    schemas["GroupVisibility"] = {
        "type": "string",
        "enum": ["public", "private"],
        "description": "Group visibility"
    }
    schemas["InteractionType"] = {
        "type": "string",
        "enum": ["like", "comment", "rating"],
        "description": "Type of interaction"
    }
    schemas["MemberRole"] = {
        "type": "string",
        "enum": ["owner", "admin", "member"],
        "description": "Group member role"
    }
    schemas["MemberStatus"] = {
        "type": "string",
        "enum": ["pending", "accepted", "rejected"],
        "description": "Group membership status"
    }

    # Category schemas
    schemas["CategoryCreate"] = {
        "type": "object",
        "required": ["name", "description", "type"],
        "properties": {
            "name": {"type": "string", "minLength": 1, "maxLength": 200},
            "description": {"type": "string", "minLength": 1},
            "type": {"$ref": "#/components/schemas/CategoryType"},
            "status": {"$ref": "#/components/schemas/CategoryStatus"},
            "cover_image": {"type": "string", "format": "uri"},
            "start_date": {"type": "string", "format": "date-time"},
            "end_date": {"type": "string", "format": "date-time"},
            "content": {"type": "string", "description": "Markdown content body"}
        }
    }
    schemas["CategoryUpdate"] = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1, "maxLength": 200},
            "description": {"type": "string"},
            "status": {"$ref": "#/components/schemas/CategoryStatus"},
            "cover_image": {"type": "string", "format": "uri"},
            "start_date": {"type": "string", "format": "date-time"},
            "end_date": {"type": "string", "format": "date-time"},
            "content": {"type": "string"}
        }
    }
    schemas["Category"] = {
        "type": "object",
        "required": ["id", "name", "description", "type", "status", "created_at", "updated_at"],
        "properties": {
            "id": {"type": "string", "example": "cat_abc123"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "type": {"$ref": "#/components/schemas/CategoryType"},
            "status": {"$ref": "#/components/schemas/CategoryStatus"},
            "cover_image": {"type": "string", "format": "uri"},
            "start_date": {"type": "string", "format": "date-time"},
            "end_date": {"type": "string", "format": "date-time"},
            "content": {"type": "string"},
            "created_by": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"},
            "updated_at": {"type": "string", "format": "date-time"}
        }
    }

    # Post schemas
    schemas["PostCreate"] = {
        "type": "object",
        "required": ["title"],
        "properties": {
            "title": {"type": "string", "minLength": 1, "maxLength": 500},
            "type": {"$ref": "#/components/schemas/PostType"},
            "tags": {"type": "array", "items": {"type": "string"}},
            "status": {"$ref": "#/components/schemas/PostStatus"},
            "content": {"type": "string", "description": "Markdown content body"}
        }
    }
    schemas["PostUpdate"] = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "minLength": 1, "maxLength": 500},
            "type": {"$ref": "#/components/schemas/PostType"},
            "tags": {"type": "array", "items": {"type": "string"}},
            "status": {"$ref": "#/components/schemas/PostStatus"},
            "content": {"type": "string"}
        }
    }
    schemas["Post"] = {
        "type": "object",
        "required": ["id", "title", "type", "status", "created_at", "updated_at"],
        "properties": {
            "id": {"type": "string", "example": "post_abc123"},
            "title": {"type": "string"},
            "type": {"$ref": "#/components/schemas/PostType"},
            "tags": {"type": "array", "items": {"type": "string"}},
            "status": {"$ref": "#/components/schemas/PostStatus"},
            "content": {"type": "string"},
            "like_count": {"type": "integer", "readOnly": True},
            "comment_count": {"type": "integer", "readOnly": True},
            "average_rating": {"type": "number", "format": "float", "readOnly": True, "nullable": True},
            "created_by": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"},
            "updated_at": {"type": "string", "format": "date-time"}
        }
    }

    # Resource schemas
    schemas["ResourceCreate"] = {
        "type": "object",
        "required": ["filename"],
        "properties": {
            "filename": {"type": "string"},
            "display_name": {"type": "string"},
            "description": {"type": "string"}
        }
    }
    schemas["Resource"] = {
        "type": "object",
        "required": ["id", "filename", "created_at"],
        "properties": {
            "id": {"type": "string", "example": "res_abc123"},
            "filename": {"type": "string"},
            "display_name": {"type": "string"},
            "description": {"type": "string"},
            "mime_type": {"type": "string", "readOnly": True},
            "size": {"type": "integer", "readOnly": True, "description": "File size in bytes"},
            "url": {"type": "string", "format": "uri", "readOnly": True},
            "created_by": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"},
            "updated_at": {"type": "string", "format": "date-time"}
        }
    }

    # Rule schemas
    schemas["ScoringCriterion"] = {
        "type": "object",
        "required": ["name", "weight"],
        "properties": {
            "name": {"type": "string", "example": "Innovation"},
            "weight": {"type": "integer", "minimum": 0, "maximum": 100, "example": 30},
            "description": {"type": "string"}
        }
    }
    schemas["RuleCreate"] = {
        "type": "object",
        "required": ["name", "description"],
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "description": {"type": "string", "minLength": 1},
            "allow_public": {"type": "boolean", "default": False},
            "require_review": {"type": "boolean", "default": False},
            "reviewers": {"type": "array", "items": {"type": "string"}},
            "submission_start": {"type": "string", "format": "date-time"},
            "submission_deadline": {"type": "string", "format": "date-time"},
            "submission_format": {"type": "array", "items": {"type": "string"}},
            "max_submissions": {"type": "integer", "minimum": 1},
            "min_team_size": {"type": "integer", "minimum": 1},
            "max_team_size": {"type": "integer", "minimum": 1},
            "scoring_criteria": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/ScoringCriterion"}
            },
            "content": {"type": "string", "description": "Markdown content body"}
        }
    }
    schemas["Rule"] = {
        "type": "object",
        "required": ["id", "name", "description", "created_at"],
        "properties": {
            "id": {"type": "string", "example": "rule_abc123"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "allow_public": {"type": "boolean"},
            "require_review": {"type": "boolean"},
            "reviewers": {"type": "array", "items": {"type": "string"}},
            "submission_start": {"type": "string", "format": "date-time"},
            "submission_deadline": {"type": "string", "format": "date-time"},
            "submission_format": {"type": "array", "items": {"type": "string"}},
            "max_submissions": {"type": "integer"},
            "min_team_size": {"type": "integer"},
            "max_team_size": {"type": "integer"},
            "scoring_criteria": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/ScoringCriterion"}
            },
            "content": {"type": "string"},
            "created_by": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"},
            "updated_at": {"type": "string", "format": "date-time"}
        }
    }

    # User schemas
    schemas["UserCreate"] = {
        "type": "object",
        "required": ["username", "email"],
        "properties": {
            "username": {"type": "string", "minLength": 3, "maxLength": 50, "pattern": "^[a-zA-Z0-9_-]+$"},
            "email": {"type": "string", "format": "email"},
            "display_name": {"type": "string", "maxLength": 100},
            "avatar_url": {"type": "string", "format": "uri"},
            "bio": {"type": "string", "maxLength": 500},
            "role": {"$ref": "#/components/schemas/UserRole"}
        }
    }
    schemas["UserUpdate"] = {
        "type": "object",
        "properties": {
            "display_name": {"type": "string", "maxLength": 100},
            "avatar_url": {"type": "string", "format": "uri"},
            "bio": {"type": "string", "maxLength": 500}
        }
    }
    schemas["User"] = {
        "type": "object",
        "required": ["id", "username", "email", "role", "created_at"],
        "properties": {
            "id": {"type": "string", "example": "user_abc123"},
            "username": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "display_name": {"type": "string"},
            "avatar_url": {"type": "string", "format": "uri"},
            "bio": {"type": "string"},
            "role": {"$ref": "#/components/schemas/UserRole"},
            "created_at": {"type": "string", "format": "date-time"},
            "updated_at": {"type": "string", "format": "date-time"}
        }
    }

    # Group schemas
    schemas["GroupCreate"] = {
        "type": "object",
        "required": ["name"],
        "properties": {
            "name": {"type": "string", "minLength": 1, "maxLength": 100},
            "description": {"type": "string"},
            "visibility": {"$ref": "#/components/schemas/GroupVisibility"},
            "max_members": {"type": "integer", "minimum": 2},
            "require_approval": {"type": "boolean", "default": False}
        }
    }
    schemas["GroupUpdate"] = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1, "maxLength": 100},
            "description": {"type": "string"},
            "visibility": {"$ref": "#/components/schemas/GroupVisibility"},
            "max_members": {"type": "integer", "minimum": 2},
            "require_approval": {"type": "boolean"}
        }
    }
    schemas["Group"] = {
        "type": "object",
        "required": ["id", "name", "visibility", "created_at"],
        "properties": {
            "id": {"type": "string", "example": "grp_abc123"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "visibility": {"$ref": "#/components/schemas/GroupVisibility"},
            "max_members": {"type": "integer"},
            "require_approval": {"type": "boolean"},
            "created_by": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"},
            "updated_at": {"type": "string", "format": "date-time"}
        }
    }

    # Group member schemas
    schemas["MemberAdd"] = {
        "type": "object",
        "required": ["user_id"],
        "properties": {
            "user_id": {"type": "string"},
            "role": {"$ref": "#/components/schemas/MemberRole"}
        }
    }
    schemas["MemberUpdate"] = {
        "type": "object",
        "properties": {
            "role": {"$ref": "#/components/schemas/MemberRole"},
            "status": {"$ref": "#/components/schemas/MemberStatus"}
        }
    }
    schemas["Member"] = {
        "type": "object",
        "required": ["user_id", "role", "status"],
        "properties": {
            "user_id": {"type": "string"},
            "user": {"$ref": "#/components/schemas/User"},
            "role": {"$ref": "#/components/schemas/MemberRole"},
            "status": {"$ref": "#/components/schemas/MemberStatus"},
            "joined_at": {"type": "string", "format": "date-time"},
            "status_changed_at": {"type": "string", "format": "date-time"}
        }
    }

    # Interaction schemas
    schemas["CommentCreate"] = {
        "type": "object",
        "required": ["content"],
        "properties": {
            "content": {"type": "string", "minLength": 1, "maxLength": 2000},
            "parent_id": {"type": "string", "description": "Parent comment ID for replies"}
        }
    }
    schemas["Comment"] = {
        "type": "object",
        "required": ["id", "content", "created_by", "created_at"],
        "properties": {
            "id": {"type": "string", "example": "iact_abc123"},
            "content": {"type": "string"},
            "parent_id": {"type": "string"},
            "created_by": {"type": "string"},
            "author": {"$ref": "#/components/schemas/User"},
            "created_at": {"type": "string", "format": "date-time"},
            "updated_at": {"type": "string", "format": "date-time"}
        }
    }
    schemas["RatingCreate"] = {
        "type": "object",
        "required": ["scores"],
        "properties": {
            "scores": {
                "type": "object",
                "additionalProperties": {"type": "number", "minimum": 0, "maximum": 100},
                "example": {"Innovation": 87, "Technical": 82, "Practical": 78}
            },
            "comment": {"type": "string", "description": "Optional rating comment"}
        }
    }
    schemas["Rating"] = {
        "type": "object",
        "required": ["id", "scores", "created_by", "created_at"],
        "properties": {
            "id": {"type": "string"},
            "scores": {"type": "object", "additionalProperties": {"type": "number"}},
            "comment": {"type": "string"},
            "created_by": {"type": "string"},
            "author": {"$ref": "#/components/schemas/User"},
            "created_at": {"type": "string", "format": "date-time"}
        }
    }

    # Relation schemas
    schemas["CategoryRuleAdd"] = {
        "type": "object",
        "required": ["rule_id"],
        "properties": {
            "rule_id": {"type": "string"},
            "priority": {"type": "integer", "default": 0}
        }
    }
    schemas["CategoryPostAdd"] = {
        "type": "object",
        "required": ["post_id"],
        "properties": {
            "post_id": {"type": "string"},
            "relation_type": {
                "type": "string",
                "enum": ["submission", "reference"],
                "default": "submission"
            }
        }
    }
    schemas["CategoryGroupAdd"] = {
        "type": "object",
        "required": ["group_id"],
        "properties": {
            "group_id": {"type": "string"}
        }
    }
    schemas["PostResourceAdd"] = {
        "type": "object",
        "required": ["resource_id"],
        "properties": {
            "resource_id": {"type": "string"},
            "display_type": {
                "type": "string",
                "enum": ["attachment", "inline"],
                "default": "attachment"
            },
            "position": {"type": "integer"}
        }
    }
    schemas["PostRelationAdd"] = {
        "type": "object",
        "required": ["target_post_id"],
        "properties": {
            "target_post_id": {"type": "string"},
            "relation_type": {
                "type": "string",
                "enum": ["reference", "reply", "embed"],
                "default": "reference"
            },
            "position": {"type": "integer"}
        }
    }

    # Paginated response schemas
    for resource in ["Category", "Post", "Resource", "Rule", "User", "Group", "Comment", "Rating", "Member"]:
        schemas[f"Paginated{resource}List"] = {
            "type": "object",
            "required": ["items", "total", "skip", "limit"],
            "properties": {
                "items": {"type": "array", "items": {"$ref": f"#/components/schemas/{resource}"}},
                "total": {"type": "integer", "description": "Total number of records"},
                "skip": {"type": "integer"},
                "limit": {"type": "integer"}
            }
        }

    # Batch operation schemas
    schemas["BatchIds"] = {
        "type": "object",
        "required": ["ids"],
        "properties": {
            "ids": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 100}
        }
    }
    schemas["BatchStatusUpdate"] = {
        "type": "object",
        "required": ["ids", "status"],
        "properties": {
            "ids": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 100},
            "status": {"$ref": "#/components/schemas/PostStatus"}
        }
    }
    schemas["BatchRoleUpdate"] = {
        "type": "object",
        "required": ["ids", "role"],
        "properties": {
            "ids": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 100},
            "role": {"$ref": "#/components/schemas/UserRole"}
        }
    }
    schemas["BatchResult"] = {
        "type": "object",
        "required": ["success_count", "failed_count"],
        "properties": {
            "success_count": {"type": "integer"},
            "failed_count": {"type": "integer"},
            "failed_ids": {"type": "array", "items": {"type": "string"}},
            "errors": {"type": "object", "additionalProperties": {"type": "string"}}
        }
    }

    return schemas


def _generate_paths() -> dict:
    """Generate all API paths."""
    paths = {}

    # Categories
    paths["/categories"] = {
        "get": {
            "summary": "List categories",
            "operationId": "list_categories",
            "tags": ["categories"],
            "parameters": [
                {"$ref": "#/components/parameters/SkipParam"},
                {"$ref": "#/components/parameters/LimitParam"},
                {"name": "type", "in": "query", "schema": {"$ref": "#/components/schemas/CategoryType"}},
                {"name": "status", "in": "query", "schema": {"$ref": "#/components/schemas/CategoryStatus"}}
            ],
            "responses": {
                "200": {
                    "description": "List of categories",
                    "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PaginatedCategoryList"}}}
                }
            }
        },
        "post": {
            "summary": "Create category",
            "operationId": "create_category",
            "tags": ["categories"],
            "requestBody": {
                "required": True,
                "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CategoryCreate"}}}
            },
            "responses": {
                "201": {
                    "description": "Category created",
                    "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Category"}}}
                },
                "422": {"$ref": "#/components/responses/ValidationError"}
            }
        }
    }
    paths["/categories/{category_id}"] = {
        "get": {
            "summary": "Get category",
            "operationId": "get_category",
            "tags": ["categories"],
            "parameters": [{"name": "category_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {
                "200": {"description": "Category details", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Category"}}}},
                "404": {"$ref": "#/components/responses/NotFound"}
            }
        },
        "patch": {
            "summary": "Update category",
            "operationId": "update_category",
            "tags": ["categories"],
            "parameters": [{"name": "category_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CategoryUpdate"}}}},
            "responses": {
                "200": {"description": "Category updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Category"}}}},
                "404": {"$ref": "#/components/responses/NotFound"}
            }
        },
        "delete": {
            "summary": "Delete category",
            "operationId": "delete_category",
            "tags": ["categories"],
            "parameters": [{"name": "category_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"204": {"description": "Category deleted"}, "404": {"$ref": "#/components/responses/NotFound"}}
        }
    }

    # Category nested resources
    paths["/categories/{category_id}/rules"] = {
        "get": {
            "summary": "List category rules",
            "operationId": "list_category_rules",
            "tags": ["categories"],
            "parameters": [{"name": "category_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "List of rules", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Rule"}}}}}}
        },
        "post": {
            "summary": "Add rule to category",
            "operationId": "add_category_rule",
            "tags": ["categories"],
            "parameters": [{"name": "category_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CategoryRuleAdd"}}}},
            "responses": {"201": {"description": "Rule added"}, "404": {"$ref": "#/components/responses/NotFound"}}
        }
    }
    paths["/categories/{category_id}/rules/{rule_id}"] = {
        "delete": {
            "summary": "Remove rule from category",
            "operationId": "remove_category_rule",
            "tags": ["categories"],
            "parameters": [
                {"name": "category_id", "in": "path", "required": True, "schema": {"type": "string"}},
                {"name": "rule_id", "in": "path", "required": True, "schema": {"type": "string"}}
            ],
            "responses": {"204": {"description": "Rule removed"}, "404": {"$ref": "#/components/responses/NotFound"}}
        }
    }
    paths["/categories/{category_id}/posts"] = {
        "get": {
            "summary": "List category posts",
            "operationId": "list_category_posts",
            "tags": ["categories"],
            "parameters": [
                {"name": "category_id", "in": "path", "required": True, "schema": {"type": "string"}},
                {"$ref": "#/components/parameters/SkipParam"},
                {"$ref": "#/components/parameters/LimitParam"},
                {"name": "relation_type", "in": "query", "schema": {"type": "string", "enum": ["submission", "reference"]}}
            ],
            "responses": {"200": {"description": "List of posts", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PaginatedPostList"}}}}}
        },
        "post": {
            "summary": "Add post to category",
            "operationId": "add_category_post",
            "tags": ["categories"],
            "parameters": [{"name": "category_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CategoryPostAdd"}}}},
            "responses": {"201": {"description": "Post added"}, "404": {"$ref": "#/components/responses/NotFound"}}
        }
    }
    paths["/categories/{category_id}/groups"] = {
        "get": {
            "summary": "List registered groups",
            "operationId": "list_category_groups",
            "tags": ["categories"],
            "parameters": [{"name": "category_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "List of groups", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Group"}}}}}}
        },
        "post": {
            "summary": "Register group for category",
            "operationId": "register_category_group",
            "tags": ["categories"],
            "parameters": [{"name": "category_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CategoryGroupAdd"}}}},
            "responses": {"201": {"description": "Group registered"}, "404": {"$ref": "#/components/responses/NotFound"}}
        }
    }

    # Posts
    paths["/posts"] = {
        "get": {
            "summary": "List posts",
            "operationId": "list_posts",
            "tags": ["posts"],
            "parameters": [
                {"$ref": "#/components/parameters/SkipParam"},
                {"$ref": "#/components/parameters/LimitParam"},
                {"name": "type", "in": "query", "schema": {"$ref": "#/components/schemas/PostType"}},
                {"name": "status", "in": "query", "schema": {"$ref": "#/components/schemas/PostStatus"}},
                {"name": "tags", "in": "query", "schema": {"type": "array", "items": {"type": "string"}}, "style": "form", "explode": False}
            ],
            "responses": {"200": {"description": "List of posts", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PaginatedPostList"}}}}}
        },
        "post": {
            "summary": "Create post",
            "operationId": "create_post",
            "tags": ["posts"],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PostCreate"}}}},
            "responses": {"201": {"description": "Post created", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Post"}}}}}
        }
    }
    paths["/posts/{post_id}"] = {
        "get": {
            "summary": "Get post",
            "operationId": "get_post",
            "tags": ["posts"],
            "parameters": [{"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "Post details", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Post"}}}}, "404": {"$ref": "#/components/responses/NotFound"}}
        },
        "patch": {
            "summary": "Update post",
            "operationId": "update_post",
            "tags": ["posts"],
            "parameters": [{"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PostUpdate"}}}},
            "responses": {"200": {"description": "Post updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Post"}}}}}
        },
        "delete": {
            "summary": "Delete post",
            "operationId": "delete_post",
            "tags": ["posts"],
            "parameters": [{"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"204": {"description": "Post deleted"}}
        }
    }

    # Post interactions
    paths["/posts/{post_id}/like"] = {
        "post": {
            "summary": "Like post",
            "operationId": "like_post",
            "tags": ["interactions"],
            "parameters": [{"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"201": {"description": "Post liked"}, "409": {"description": "Already liked"}}
        },
        "delete": {
            "summary": "Unlike post",
            "operationId": "unlike_post",
            "tags": ["interactions"],
            "parameters": [{"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"204": {"description": "Like removed"}}
        }
    }
    paths["/posts/{post_id}/comments"] = {
        "get": {
            "summary": "List post comments",
            "operationId": "list_post_comments",
            "tags": ["interactions"],
            "parameters": [
                {"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}},
                {"$ref": "#/components/parameters/SkipParam"},
                {"$ref": "#/components/parameters/LimitParam"}
            ],
            "responses": {"200": {"description": "List of comments", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PaginatedCommentList"}}}}}
        },
        "post": {
            "summary": "Add comment",
            "operationId": "add_post_comment",
            "tags": ["interactions"],
            "parameters": [{"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CommentCreate"}}}},
            "responses": {"201": {"description": "Comment added", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Comment"}}}}}
        }
    }
    paths["/posts/{post_id}/comments/{comment_id}"] = {
        "patch": {
            "summary": "Update comment",
            "operationId": "update_post_comment",
            "tags": ["interactions"],
            "parameters": [
                {"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}},
                {"name": "comment_id", "in": "path", "required": True, "schema": {"type": "string"}}
            ],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CommentCreate"}}}},
            "responses": {"200": {"description": "Comment updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Comment"}}}}}
        },
        "delete": {
            "summary": "Delete comment",
            "operationId": "delete_post_comment",
            "tags": ["interactions"],
            "parameters": [
                {"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}},
                {"name": "comment_id", "in": "path", "required": True, "schema": {"type": "string"}}
            ],
            "responses": {"204": {"description": "Comment deleted"}}
        }
    }
    paths["/posts/{post_id}/ratings"] = {
        "get": {
            "summary": "List post ratings",
            "operationId": "list_post_ratings",
            "tags": ["interactions"],
            "parameters": [
                {"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}},
                {"$ref": "#/components/parameters/SkipParam"},
                {"$ref": "#/components/parameters/LimitParam"}
            ],
            "responses": {"200": {"description": "List of ratings", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PaginatedRatingList"}}}}}
        },
        "post": {
            "summary": "Submit rating",
            "operationId": "submit_post_rating",
            "tags": ["interactions"],
            "parameters": [{"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RatingCreate"}}}},
            "responses": {"201": {"description": "Rating submitted", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Rating"}}}}}
        }
    }

    # Post resources
    paths["/posts/{post_id}/resources"] = {
        "get": {
            "summary": "List post resources",
            "operationId": "list_post_resources",
            "tags": ["posts"],
            "parameters": [{"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "List of resources", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Resource"}}}}}}
        },
        "post": {
            "summary": "Add resource to post",
            "operationId": "add_post_resource",
            "tags": ["posts"],
            "parameters": [{"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PostResourceAdd"}}}},
            "responses": {"201": {"description": "Resource added"}}
        }
    }
    paths["/posts/{post_id}/related"] = {
        "get": {
            "summary": "List related posts",
            "operationId": "list_related_posts",
            "tags": ["posts"],
            "parameters": [
                {"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}},
                {"name": "relation_type", "in": "query", "schema": {"type": "string", "enum": ["reference", "reply", "embed"]}}
            ],
            "responses": {"200": {"description": "List of related posts", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Post"}}}}}}
        },
        "post": {
            "summary": "Add related post",
            "operationId": "add_related_post",
            "tags": ["posts"],
            "parameters": [{"name": "post_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PostRelationAdd"}}}},
            "responses": {"201": {"description": "Relation added"}}
        }
    }

    # Resources
    paths["/resources"] = {
        "get": {
            "summary": "List resources",
            "operationId": "list_resources",
            "tags": ["resources"],
            "parameters": [{"$ref": "#/components/parameters/SkipParam"}, {"$ref": "#/components/parameters/LimitParam"}],
            "responses": {"200": {"description": "List of resources", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PaginatedResourceList"}}}}}
        },
        "post": {
            "summary": "Create resource",
            "operationId": "create_resource",
            "tags": ["resources"],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ResourceCreate"}}}},
            "responses": {"201": {"description": "Resource created", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Resource"}}}}}
        }
    }
    paths["/resources/{resource_id}"] = {
        "get": {
            "summary": "Get resource",
            "operationId": "get_resource",
            "tags": ["resources"],
            "parameters": [{"name": "resource_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "Resource details", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Resource"}}}}}
        },
        "delete": {
            "summary": "Delete resource",
            "operationId": "delete_resource",
            "tags": ["resources"],
            "parameters": [{"name": "resource_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"204": {"description": "Resource deleted"}}
        }
    }

    # Rules
    paths["/rules"] = {
        "get": {
            "summary": "List rules",
            "operationId": "list_rules",
            "tags": ["rules"],
            "parameters": [{"$ref": "#/components/parameters/SkipParam"}, {"$ref": "#/components/parameters/LimitParam"}],
            "responses": {"200": {"description": "List of rules", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PaginatedRuleList"}}}}}
        },
        "post": {
            "summary": "Create rule",
            "operationId": "create_rule",
            "tags": ["rules"],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RuleCreate"}}}},
            "responses": {"201": {"description": "Rule created", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Rule"}}}}}
        }
    }
    paths["/rules/{rule_id}"] = {
        "get": {
            "summary": "Get rule",
            "operationId": "get_rule",
            "tags": ["rules"],
            "parameters": [{"name": "rule_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "Rule details", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Rule"}}}}}
        },
        "patch": {
            "summary": "Update rule",
            "operationId": "update_rule",
            "tags": ["rules"],
            "parameters": [{"name": "rule_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RuleCreate"}}}},
            "responses": {"200": {"description": "Rule updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Rule"}}}}}
        },
        "delete": {
            "summary": "Delete rule",
            "operationId": "delete_rule",
            "tags": ["rules"],
            "parameters": [{"name": "rule_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"204": {"description": "Rule deleted"}}
        }
    }

    # Users
    paths["/users"] = {
        "get": {
            "summary": "List users",
            "operationId": "list_users",
            "tags": ["users"],
            "parameters": [
                {"$ref": "#/components/parameters/SkipParam"},
                {"$ref": "#/components/parameters/LimitParam"},
                {"name": "role", "in": "query", "schema": {"$ref": "#/components/schemas/UserRole"}}
            ],
            "responses": {"200": {"description": "List of users", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PaginatedUserList"}}}}}
        },
        "post": {
            "summary": "Create user",
            "operationId": "create_user",
            "tags": ["users"],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/UserCreate"}}}},
            "responses": {"201": {"description": "User created", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/User"}}}}}
        }
    }
    paths["/users/me"] = {
        "get": {
            "summary": "Get current user",
            "operationId": "get_current_user",
            "tags": ["users"],
            "responses": {"200": {"description": "Current user", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/User"}}}}}
        },
        "patch": {
            "summary": "Update current user",
            "operationId": "update_current_user",
            "tags": ["users"],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/UserUpdate"}}}},
            "responses": {"200": {"description": "User updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/User"}}}}}
        }
    }
    paths["/users/{user_id}"] = {
        "get": {
            "summary": "Get user",
            "operationId": "get_user",
            "tags": ["users"],
            "parameters": [{"name": "user_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "User details", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/User"}}}}}
        },
        "patch": {
            "summary": "Update user",
            "operationId": "update_user",
            "tags": ["users"],
            "parameters": [{"name": "user_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/UserUpdate"}}}},
            "responses": {"200": {"description": "User updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/User"}}}}}
        },
        "delete": {
            "summary": "Delete user",
            "operationId": "delete_user",
            "tags": ["users"],
            "parameters": [{"name": "user_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"204": {"description": "User deleted"}}
        }
    }

    # Groups
    paths["/groups"] = {
        "get": {
            "summary": "List groups",
            "operationId": "list_groups",
            "tags": ["groups"],
            "parameters": [
                {"$ref": "#/components/parameters/SkipParam"},
                {"$ref": "#/components/parameters/LimitParam"},
                {"name": "visibility", "in": "query", "schema": {"$ref": "#/components/schemas/GroupVisibility"}}
            ],
            "responses": {"200": {"description": "List of groups", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PaginatedGroupList"}}}}}
        },
        "post": {
            "summary": "Create group",
            "operationId": "create_group",
            "tags": ["groups"],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/GroupCreate"}}}},
            "responses": {"201": {"description": "Group created", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Group"}}}}}
        }
    }
    paths["/groups/{group_id}"] = {
        "get": {
            "summary": "Get group",
            "operationId": "get_group",
            "tags": ["groups"],
            "parameters": [{"name": "group_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"200": {"description": "Group details", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Group"}}}}}
        },
        "patch": {
            "summary": "Update group",
            "operationId": "update_group",
            "tags": ["groups"],
            "parameters": [{"name": "group_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/GroupUpdate"}}}},
            "responses": {"200": {"description": "Group updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Group"}}}}}
        },
        "delete": {
            "summary": "Delete group",
            "operationId": "delete_group",
            "tags": ["groups"],
            "parameters": [{"name": "group_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "responses": {"204": {"description": "Group deleted"}}
        }
    }
    paths["/groups/{group_id}/members"] = {
        "get": {
            "summary": "List group members",
            "operationId": "list_group_members",
            "tags": ["groups"],
            "parameters": [
                {"name": "group_id", "in": "path", "required": True, "schema": {"type": "string"}},
                {"name": "status", "in": "query", "schema": {"$ref": "#/components/schemas/MemberStatus"}}
            ],
            "responses": {"200": {"description": "List of members", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PaginatedMemberList"}}}}}
        },
        "post": {
            "summary": "Add member to group",
            "operationId": "add_group_member",
            "tags": ["groups"],
            "parameters": [{"name": "group_id", "in": "path", "required": True, "schema": {"type": "string"}}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MemberAdd"}}}},
            "responses": {"201": {"description": "Member added", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Member"}}}}}
        }
    }
    paths["/groups/{group_id}/members/{user_id}"] = {
        "patch": {
            "summary": "Update member",
            "operationId": "update_group_member",
            "tags": ["groups"],
            "parameters": [
                {"name": "group_id", "in": "path", "required": True, "schema": {"type": "string"}},
                {"name": "user_id", "in": "path", "required": True, "schema": {"type": "string"}}
            ],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MemberUpdate"}}}},
            "responses": {"200": {"description": "Member updated", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Member"}}}}}
        },
        "delete": {
            "summary": "Remove member from group",
            "operationId": "remove_group_member",
            "tags": ["groups"],
            "parameters": [
                {"name": "group_id", "in": "path", "required": True, "schema": {"type": "string"}},
                {"name": "user_id", "in": "path", "required": True, "schema": {"type": "string"}}
            ],
            "responses": {"204": {"description": "Member removed"}}
        }
    }

    # Admin batch operations
    paths["/admin/posts"] = {
        "delete": {
            "summary": "Batch delete posts",
            "operationId": "batch_delete_posts",
            "tags": ["admin"],
            "security": [{"oauth2": ["admin"]}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BatchIds"}}}},
            "responses": {"200": {"description": "Batch result", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BatchResult"}}}}}
        }
    }
    paths["/admin/posts/status"] = {
        "patch": {
            "summary": "Batch update post status",
            "operationId": "batch_update_post_status",
            "tags": ["admin"],
            "security": [{"oauth2": ["admin"]}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BatchStatusUpdate"}}}},
            "responses": {"200": {"description": "Batch result", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BatchResult"}}}}}
        }
    }
    paths["/admin/users/role"] = {
        "patch": {
            "summary": "Batch update user roles",
            "operationId": "batch_update_user_roles",
            "tags": ["admin"],
            "security": [{"oauth2": ["admin"]}],
            "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BatchRoleUpdate"}}}},
            "responses": {"200": {"description": "Batch result", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BatchResult"}}}}}
        }
    }

    return paths


def to_yaml(spec: dict) -> str:
    """Convert spec to YAML string."""
    if yaml:
        return yaml.dump(spec, default_flow_style=False, allow_unicode=True, sort_keys=False)
    else:
        return json.dumps(spec, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Generate OpenAPI spec from Synnovator schema")
    parser.add_argument("--output", "-o", default=".synnovator/openapi.yaml",
                        help="Output file path (default: .synnovator/openapi.yaml)")
    parser.add_argument("--title", default="Synnovator API", help="API title")
    parser.add_argument("--version", default="1.0.0", help="API version")
    parser.add_argument("--format", choices=["yaml", "json"], default="yaml", help="Output format")

    args = parser.parse_args()

    spec = generate_openapi_spec(title=args.title, version=args.version)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        if args.format == "yaml" and yaml:
            f.write(to_yaml(spec))
        else:
            json.dump(spec, f, indent=2, ensure_ascii=False)

    print(f"Generated OpenAPI spec: {output_path}")
    print(f"  - {len(spec['paths'])} endpoints")
    print(f"  - {len(spec['components']['schemas'])} schemas")


if __name__ == "__main__":
    main()