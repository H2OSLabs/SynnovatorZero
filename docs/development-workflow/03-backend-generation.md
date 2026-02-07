# 阶段 2: 后端代码生成

> 从 OpenAPI 规范生成 FastAPI 后端代码。

## 使用 api-builder Skill

```bash
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml \
  --output app \
  --setup-alembic \
  --run-migrations
```

### 冲突处理策略

| 策略 | 说明 |
|------|------|
| `--conflict-strategy skip` | 默认，不覆盖已存在文件 |
| `--conflict-strategy backup` | 先备份再覆盖（推荐更新项目） |
| `--conflict-strategy overwrite` | 直接覆盖（仅限全新项目） |
| `--dry-run` | 预览将生成的文件 |

## 生成内容

```
app/
├── models/               # SQLAlchemy ORM 模型
├── schemas/              # Pydantic 验证 schemas
├── routers/              # FastAPI 路由
├── crud/                 # CRUD 操作
├── tests/                # pytest 测试
├── alembic/              # 数据库迁移
├── main.py               # FastAPI 应用入口
├── database.py           # 数据库配置
└── alembic.ini           # Alembic 配置
```

## 验证

```bash
# 查看数据库表
sqlite3 data/synnovator.db ".tables"

# 启动开发服务器
make backend

# 访问 API 文档
open http://localhost:8000/docs
```

## 补充业务逻辑

生成的代码包含 TODO 注释，需要补充：

```python
# app/routers/users.py
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # TODO: 添加业务逻辑
    # - 验证用户名/邮箱唯一性
    # - 密码哈希
    return crud_user.create(db, user)
```

## 增量测试

> 每完成一个模块，立即测试该模块。

```bash
# 用户模块
uv run pytest app/tests/test_users.py -v

# 活动模块
uv run pytest app/tests/test_events.py -v

# 帖子模块
uv run pytest app/tests/test_posts.py -v
```

**开发顺序：**

| 顺序 | 模块 | 对应测试用例 |
|------|------|-------------|
| 1 | user | TC-USER-* |
| 2 | event | TC-CAT-* |
| 3 | rule | TC-RULE-*, TC-ENGINE-* |
| 4 | group | TC-GRP-* |
| 5 | post | TC-POST-* |
| 6 | resource | TC-RES-* |
| 7 | interaction | TC-IACT-* |
| 8 | relations | TC-REL-* |

## 下一步

完成后端生成后，进入 [阶段 2.5-3: 种子数据](04-seed-data.md)。
