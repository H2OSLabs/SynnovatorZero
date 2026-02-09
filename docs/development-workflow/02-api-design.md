# 阶段 1: API 设计

> 从领域模型生成 OpenAPI 3.x 规范。

## 使用 schema-to-openapi Skill

```bash
# 从 docs/ + specs/ 综合生成 OpenAPI 规范
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py \
  --output .synnovator/openapi.yaml \
  --title "Synnovator API" \
  --version "1.0.0" \
  --format yaml
```

## 输入

| 文件 | 描述 |
|------|------|
| `docs/data-types.md` | 内容类型字段定义 |
| `docs/relationships.md` | 关系类型定义 |
| `docs/crud-operations.md` | CRUD 操作与权限 |
| `specs/data-integrity.md` | 数据约束 |

## 输出

**`.synnovator/openapi.yaml`** 包含：

- 7 种内容类型的 CRUD endpoints (`/users`, `/events`, `/posts` 等)
- 9 种关系类型的嵌套 endpoints (`/events/{id}/posts`, `/posts/{id}/comments` 等)
- 交互 endpoints (点赞、评论、评分)
- 用户关系 endpoints（关注/屏蔽）
- 活动关联 endpoints（阶段/赛道/前置条件）
- 管理批量操作
- OAuth2 认证配置

## 验证

```bash
# 验证 OpenAPI 规范格式
uv run python .claude/skills/api-builder/scripts/validate_spec.py .synnovator/openapi.yaml

# 验证测试用例与 schema 一致
uv run python .claude/skills/tests-kit/scripts/check_testcases.py
```

**测试范围：** 验证 `specs/testcases/` 中的数据模型相关测试用例（01-07）是否与当前 schema 一致。

## 修改影响

| 修改内容 | 受影响的测试用例前缀 |
|----------|---------------------|
| 内容类型字段 | TC-USER, TC-CAT, TC-RULE, TC-GRP, TC-POST, TC-RES, TC-IACT |
| 关系类型 | TC-REL-* |
| 权限规则 | TC-PERM-* |
| 规则引擎 | TC-ENGINE-*, TC-ENTRY-*, TC-CLOSE-* |

## 下一步

完成 API 设计后，进入 [阶段 2: 后端代码生成](03-backend-generation.md)。
