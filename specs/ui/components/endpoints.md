# API Endpoints / 接口清单

> Auto-generated from `backend/main.py`

## Overview

| Resource | Endpoints | Methods |
|----------|-----------|---------|
| health | 1 | GET |
| items | 5 | GET, POST, PUT, DELETE |

---

## health

| Method | Path | Function | Description |
|--------|------|----------|-------------|
| GET | `/health` | `health` | Health check / 健康检查 |

**Response:**
```json
{ "status": "ok" }
```

---

## items

| Method | Path | Function | Request Body | Response Model |
|--------|------|----------|--------------|----------------|
| GET | `/api/items` | `get_items` | — | `list[ItemResponse]` |
| GET | `/api/items/{item_id}` | `get_item` | — | `ItemResponse` |
| POST | `/api/items` | `create_item` | `ItemCreate` | `ItemResponse` |
| PUT | `/api/items/{item_id}` | `update_item` | `ItemUpdate` | `ItemResponse` |
| DELETE | `/api/items/{item_id}` | `delete_item` | — | `{ "message": "..." }` |

### Schemas

#### ItemCreate (Request — POST)

| Field | Type | Required |
|-------|------|----------|
| `name` | `str` | Yes |

#### ItemUpdate (Request — PUT)

| Field | Type | Required |
|-------|------|----------|
| `name` | `str` | No (Optional) |

#### ItemResponse (Response)

| Field | Type | Note |
|-------|------|------|
| `id` | `int` | auto, primary key |
| `name` | `str` | — |
| `created_at` | `datetime` | auto, default=utcnow |

### Database Model: Item

| Column | SQLAlchemy Type | Constraints |
|--------|----------------|-------------|
| `id` | `Integer` | primary_key, index |
| `name` | `String` | index |
| `created_at` | `DateTime` | default=utcnow |

### Query Parameters (GET list)

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `skip` | `int` | 0 | Pagination offset / 分页偏移 |
| `limit` | `int` | 20 | Page size / 每页数量 |
| `q` | `str` | — | Search by name / 按名称搜索 |

---

## UI Pages / 页面映射

| .pen File | Endpoint(s) Covered | Description |
|-----------|---------------------|-------------|
| `items-list.pen` | `GET /api/items` | List page with table, search, pagination / 列表页 |
| `items-form.pen` | `POST /api/items` | Create form page / 新建表单页 |
| `items-edit.pen` | `GET /api/items/{id}` + `PUT /api/items/{id}` + `DELETE /api/items/{id}` | Edit form with pre-filled data + delete / 编辑表单页 |

---

## Notes

- Database: SQLite (`sqlite:///./data/app.db`)
- CORS: allows `http://localhost:3000`
- The full domain model (category, post, resource, rule, user, group, interaction) defined in `docs/command.md` has not yet been implemented
