---
name: pen-page-gen
description: Generate Penpot-compatible .pen page layout files in specs/ui/components/ from FastAPI router endpoints. Scans backend Python router files to extract endpoints, Pydantic schemas, and CRUD operations, then produces full page .pen files (list view + create/edit form) following the Neon Forge design system. Use when the user asks to generate UI pages, create .pen files from endpoints, scaffold page layouts for API routes, or wants to turn backend endpoints into UI specifications. Trigger phrases include "generate pen pages", "create UI pages from endpoints", "pen file from router", "scaffold pages for API".
---

# Pen Page Gen

Generate `.pen` page layout files from FastAPI router endpoints. For each endpoint group (resource), produce a **list page** and a **form page** in `specs/ui/components/`.

## Workflow

```
1. Parse FastAPI router files → extract endpoints, schemas, fields
2. Group endpoints by resource (e.g., /api/users → "users")
3. For each resource group:
   a. Generate {resource}-list.pen  (table + pagination + actions)
   b. Generate {resource}-form.pen  (create/edit form with fields)
4. Write files to specs/ui/components/
```

## Step 1: Parse Router Files

Scan `backend/` for FastAPI router files. Extract:
- **Endpoint paths** and HTTP methods (`@app.get`, `@app.post`, `@router.get`, etc.)
- **Pydantic response/request models** (from `response_model` and function parameters)
- **Model fields** with types from Pydantic `BaseModel` classes and SQLAlchemy model `Column` definitions

Group endpoints by resource prefix (first path segment after `/api/`).

Example extraction from a router:
```python
@app.get("/api/items", response_model=list[ItemResponse])   → resource: "items", action: "list"
@app.post("/api/items", response_model=ItemResponse)         → resource: "items", action: "create"
@app.get("/api/items/{item_id}", response_model=ItemResponse) → resource: "items", action: "detail"
@app.put("/api/items/{item_id}", response_model=ItemResponse) → resource: "items", action: "update"
@app.delete("/api/items/{item_id}")                           → resource: "items", action: "delete"
```

## Step 2: Generate .pen Files

For the `.pen` JSON format and design tokens, read [references/pen-format.md](references/pen-format.md).

### Field Type → Component Mapping

| Python/Pydantic Type | .pen Component |
|----------------------|----------------|
| `str` | Input (text) |
| `str` (long/content) | Textarea |
| `int`, `float` | Input (number) |
| `bool` | Switch |
| `datetime` | Input (datetime placeholder) |
| `Optional[...]` | Same component, with `enabled: false` helper text "(Optional)" |
| `Enum` / `Literal[...]` | Select |
| Foreign key / ID ref | Select (with related resource name) |
| `list[str]` / tags | Input with Badge display |

### Auto-excluded Fields

Do NOT generate form fields for: `id`, `created_at`, `updated_at`, `deleted_at`, `created_by`. These are system-managed.

### List Page Structure

```
Frame "PageName/List" (1440px wide)
├── Header section
│   ├── Page title (H1, Space Grotesk)
│   ├── Description text (Body, Inter)
│   └── Action bar: [Search Input] + [Create Button/Primary]
├── Table
│   ├── HeaderRow (columns from response model fields)
│   └── Body rows (3 sample data rows)
└── Pagination
```

### Form Page Structure

```
Frame "PageName/Form" (1440px wide)
├── Header section
│   ├── Breadcrumb (List → Create/Edit)
│   ├── Page title (H2, Space Grotesk)
│   └── Description text
├── Card (form container)
│   ├── cardHeader: "Resource Information / 资源信息"
│   ├── cardContent: vertical layout of Input/Group fields
│   │   └── One Input/Group per schema field
│   └── cardFooter: [Cancel Button/Outline] + [Submit Button/Primary]
└── (empty)
```

## Step 3: Write Output

Write each generated `.pen` file to `specs/ui/components/{resource}-list.pen` and `specs/ui/components/{resource}-form.pen`.

After generation, report:
- Number of endpoint groups found
- Files generated (with paths)
- Fields mapped per resource

## Important Rules

1. **Always use design tokens** from the Neon Forge theme — never hardcode colors without checking the reference.
2. **Generate unique IDs** for every node — use 5-char alphanumeric strings (e.g., `"aB3xK"`).
3. **Bilingual labels** — section titles should include both English and Chinese (e.g., "User List / 用户列表").
4. **Reusable components** — page-level frames should have `"reusable": true`.
5. **Follow existing patterns** — reference `specs/ui/basic.pen` for component structure when uncertain about a specific component's JSON shape.
6. **Version field** — every `.pen` file must start with `"version": "2.6"`.
