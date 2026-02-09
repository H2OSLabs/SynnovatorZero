# 附录 B: 数据模型更新流程

## 场景 1: 添加新字段

```bash
# 0. [tests-kit Guard] 先检查现有测试用例
uv run python .claude/skills/tests-kit/scripts/check_testcases.py

# 1. 更新 docs/data-types.md（内容类型字段定义）

# 2. 重新生成 OpenAPI spec
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py

# 3. 重新生成后端代码（skip 策略保护已有文件）
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml --output app \
  --conflict-strategy skip

# 4. 手动更新已有文件（如需要）

# 5. 生成数据库迁移
alembic revision --autogenerate -m "Add new field"
alembic upgrade head

# 6. [tests-kit Guard] 验证测试用例
uv run pytest app/tests/ -v

# 7. 重新生成前端客户端
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml --output app \
  --generate-client --client-output frontend/lib/
```

## 场景 2: 添加新关系类型

```bash
# 1. 更新 docs/relationships.md（关系类型定义）

# 2. 更新 docs/crud-operations.md（操作与权限）

# 3. [tests-kit Insert] 添加新关系的测试用例
# 在 specs/testcases/ 添加 TC-REL-XX-*

# 4. 重新生成 OpenAPI spec
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py

# 5. 重新生成后端代码
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml --output app \
  --conflict-strategy skip

# 6. 手动实现关系路由和 CRUD 逻辑

# 7. 生成数据库迁移（新关系表）
alembic revision --autogenerate -m "Add new relation table"
alembic upgrade head

# 8. 更新种子数据
vim scripts/seed_dev_data.py

# 9. 运行测试
make resetdb && make seed
uv run pytest app/tests/ -v
```

## 场景 3: 修改已有字段约束

```bash
# 1. 更新 docs/data-types.md（约束变更）

# 2. 更新 specs/data-integrity.md（如涉及唯一性/索引）

# 3. 检查受影响的测试用例
grep -r "field_name" specs/testcases/

# 4. 更新受影响的测试用例

# 5. 更新后端 schema（Pydantic 验证）

# 6. 生成迁移（如涉及数据库约束）
alembic revision --autogenerate -m "Update field constraint"
alembic upgrade head

# 7. 运行测试验证
uv run pytest app/tests/ -v
```

## 场景 4: 前端-后端 API 不一致

> 当前端调用的 API 在后端不存在时。

```bash
# 1. 检查 .synnovator/openapi.yaml 是否有该 endpoint

# 2a. 如果 OpenAPI 缺失 → 更新 docs/ 并重新生成
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py

# 2b. 如果 OpenAPI 存在但后端缺失 → 重新生成后端
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml --output app

# 3. 重新生成前端客户端
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml --output app \
  --generate-client --client-output frontend/lib/

# 4. 更新前端页面使用新 API

# 5. 验证集成
make start
curl http://localhost:3000/api/new-endpoint
```

## 变更影响矩阵

| 变更类型 | 影响的文档 | 影响的代码 | 需要迁移 |
|---------|-----------|-----------|---------|
| 添加字段 | data-types.md | models, schemas | 是 |
| 删除字段 | data-types.md | models, schemas, routers | 是 |
| 修改约束 | data-types.md, data-integrity.md | schemas | 可能 |
| 添加关系 | relationships.md, crud-operations.md | models, routers | 是 |
| 修改权限 | crud-operations.md | routers, deps | 否 |
| 添加规则类型 | rule-engine.md | services/rule_engine.py | 否 |
