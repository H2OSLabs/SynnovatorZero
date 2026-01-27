# Synnovator 完整开发流程

## 概述

从需求设计到前后端实现和测试的完整开发流程。本流程涵盖数据建模、代码生成、数据注入、后端实现、前端集成（不含 UI 组件）和全栈测试。

## 完整工作流图

```
┌────────────────────────────────────────────────────────────────┐
│ 阶段 0: 项目初始化                                              │
│  - 定义技术栈                                                   │
│  - 创建项目结构                                                 │
│  - 配置开发环境                                                 │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│ 阶段 1: 需求设计与数据建模                                      │
│  schema.md (数据模型定义)                                       │
│      ├─→ 7 种内容类型: user, category, post, rule...         │
│      └─→ 7 种关系类型: category_rule, post_resource...        │
│                                                                │
│  [手工] 创建示例数据                                            │
│      ↓ [synnovator skill]                                     │
│  .synnovator/*.md (测试数据)                                   │
│                                                                │
│  [schema-to-openapi skill]                                     │
│      ↓                                                        │
│  OpenAPI 3.x 规范 (.synnovator/openapi.yaml)                  │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│ 阶段 2: 后端代码生成                                            │
│  [api-builder skill]                                          │
│      ↓                                                        │
│  FastAPI 后端                                                  │
│      ├─→ models/ (SQLAlchemy ORM)                            │
│      ├─→ schemas/ (Pydantic 验证)                            │
│      ├─→ routers/ (FastAPI 路由)                             │
│      ├─→ crud/ (CRUD 操作)                                   │
│      └─→ tests/ (pytest 测试)                                │
│                                                                │
│  [api-builder --setup-alembic --run-migrations]               │
│      ↓                                                        │
│  SQLite database (空表结构)                                    │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│ 阶段 3: 数据注入                                                │
│  .synnovator/*.md                                              │
│      ↓ [data-importer skill]                                  │
│  SQLite database (填充测试数据)                                │
│      ├─→ 按依赖顺序导入 (user → post → relations)             │
│      ├─→ 类型转换 (datetime, JSON, enum)                     │
│      └─→ 跳过重复记录                                         │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│ 阶段 4: 前端开发                                               │
│                                                                │
│  4.1 UI 设计稿 (.pen)                                         │
│      ↓ [pen-page-gen skill]                                   │
│  specs/ui/components/*.pen (页面布局规范)                       │
│                                                                │
│  4.2 React 组件生成                                            │
│      ↓ [pen-to-react skill]                                   │
│  components/pages/*.tsx (静态页面组件)                          │
│  components/ui/*.tsx (shadcn/ui 基础组件)                      │
│                                                                │
│  4.3 路由配置                                                  │
│      ↓ [手工]                                                 │
│  app/**/page.tsx (Next.js App Router)                         │
│                                                                │
│  4.4 API 客户端生成                                            │
│      ↓ [api-builder --generate-client]                        │
│  frontend/utils/api-client.ts (TypeScript API 客户端)          │
│                                                                │
│  4.5 API 对接                                                  │
│      ↓ [手工]                                                 │
│  组件接入真实数据（替换 mock → fetch）                          │
│                                                                │
│  4.6 交互与导航验证                                            │
│      ↓ [手工]                                                 │
│  页面跳转、表单提交、状态管理                                   │
│                                                                │
│  4.7 前端测试                                                  │
│      ├─→ Jest 单元测试（组件渲染）                             │
│      └─→ Playwright E2E 测试（用户旅程）                      │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│ 阶段 5: 测试与验证                                              │
│  后端测试                                                      │
│      ├─→ pytest 单元测试                                      │
│      ├─→ API 集成测试                                         │
│      └─→ 数据库迁移测试                                       │
│                                                                │
│  全栈测试                                                      │
│      ├─→ 启动 FastAPI 服务                                   │
│      ├─→ 前端调用 API                                        │
│      └─→ 端到端测试                                          │
└────────────────────────────────────────────────────────────────┘
```

## 使用的 Skills

| Skill | 用途 | 阶段 | 状态 |
|-------|------|------|------|
| **synnovator** | 管理 .synnovator/*.md 文件数据（CRUD） | 1 | ✅ 可用 |
| **schema-to-openapi** | 从 Synnovator 数据模型生成 OpenAPI 3.0 规范 | 1 | ✅ 可用 |
| **api-builder** | 从 OpenAPI 生成 FastAPI 后端 + 迁移 + 测试 + TypeScript 客户端 | 2, 4 | ✅ 可用 |
| **data-importer** | 从 .synnovator 导入数据到 SQLite | 3 | ✅ 可用 |
| **pen-page-gen** | 从后端 router 生成 .pen 页面布局规范 | 4.1 | ✅ 可用 |
| **pen-to-react** | 从 .pen 设计稿生成 React 组件 (shadcn/ui + Tailwind) | 4.2 | ✅ 可用 |

---

## 详细步骤

### 阶段 0: 项目初始化

#### 0.1 创建项目结构

```bash
# 项目目录结构
SynnovatorZero/
├── backend/              # FastAPI 后端（将由 api-builder 生成）
├── frontend/             # Next.js 前端
├── .synnovator/          # 文件数据存储
├── docs/                 # 项目文档
│   ├── command.md        # 数据模型定义（schema 参考）
│   ├── development-workflow.md  # 本文档
│   └── user-journey.md   # 用户旅程测试
├── specs/                # OpenAPI 规范存放目录
├── pyproject.toml        # Python 依赖
└── Makefile              # 构建命令
```

#### 0.2 配置开发环境

```bash
# 安装 Python 依赖管理工具
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 Node.js (使用 nvm)
nvm install 18
nvm use 18

# 初始化 Python 环境
uv venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows
```

---

### 阶段 1: 需求设计与数据建模

#### 1.1 定义数据模型

参考 `docs/command.md` 定义数据模型：

**7 种内容类型：**
- **user**: 用户账户
- **category**: 活动/竞赛
- **post**: 用户帖子（支持多种 type）
- **rule**: 活动规则
- **resource**: 文件资源
- **group**: 团队/分组
- **interaction**: 交互记录（点赞、评论、评分）

**7 种关系类型：**
- **category_rule**: 活动-规则绑定
- **category_post**: 活动-帖子关联（报名/提交）
- **category_group**: 团队-活动报名
- **post_post**: 帖子间关联（引用/回复/嵌入）
- **post_resource**: 帖子-资源关联
- **group_user**: 成员-团队关系（含审批流程）
- **target_interaction**: 内容-交互绑定

详细字段定义见 `docs/command.md`。

#### 1.2 创建示例数据

使用 **synnovator skill** 创建测试数据：

```bash
# 创建用户
python .claude/skills/synnovator/scripts/engine.py \
  --user admin create user \
  --data '{"username": "alice", "email": "alice@example.com", "display_name": "Alice", "role": "participant"}'

python .claude/skills/synnovator/scripts/engine.py \
  --user admin create user \
  --data '{"username": "bob", "email": "bob@example.com", "display_name": "Bob", "role": "organizer"}'

# 创建活动
python .claude/skills/synnovator/scripts/engine.py \
  --user user_xxx create category \
  --data '{"name": "2025 AI Hackathon", "description": "AI innovation competition", "type": "competition", "status": "published"}' \
  --body "# Welcome\n\nJoin us for an AI innovation competition!"

# 创建帖子
python .claude/skills/synnovator/scripts/engine.py \
  --user user_xxx create post \
  --data '{"title": "My AI Project", "type": "for_category", "tags": ["ai", "demo"], "status": "published"}' \
  --body "## Project Description\n\nThis is my AI project."

# 创建团队
python .claude/skills/synnovator/scripts/engine.py \
  --user user_xxx create group \
  --data '{"name": "Team Synnovator", "description": "Our team", "visibility": "public", "require_approval": false}'

# 创建关系（团队成员）
python .claude/skills/synnovator/scripts/engine.py \
  --user user_xxx create group_user \
  --data '{"group_id": "grp_xxx", "user_id": "user_xxx", "role": "owner", "status": "accepted"}'
```

数据文件存储在 `.synnovator/` 目录：

```
.synnovator/
├── user/
│   ├── user_alice.md
│   └── user_bob.md
├── category/
│   └── cat_hackathon.md
├── post/
│   └── post_myproject.md
├── group/
│   └── grp_team.md
└── relations/
    └── group_user/
        └── grp_team_user_alice.md
```

#### 1.3 生成 OpenAPI 规范

**方式 1: 使用 schema-to-openapi skill（推荐）**

```bash
# 从 Synnovator 数据模型生成 OpenAPI 规范
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py

# 指定输出路径和格式
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py \
  --output specs/synnovator-api.yaml \
  --title "Synnovator API" \
  --version "1.0.0" \
  --format yaml
```

生成的规范包括:
- 7 种内容类型的 CRUD endpoints (`/users`, `/categories`, `/posts`, 等)
- 嵌套关系 endpoints (`/categories/{id}/posts`, `/posts/{id}/comments`, 等)
- 交互 endpoints (点赞、评论、评分)
- 管理批量操作
- OAuth2 认证配置

**方式 2: 手工编写 OpenAPI 规范**

创建 `specs/synnovator-api.yaml`，定义所有 endpoints 和 schemas。参考 OpenAPI 3.x 规范格式。

示例结构：

```yaml
openapi: 3.0.0
info:
  title: Synnovator API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    post:
      summary: Create user
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
  # ... 其他 endpoints

components:
  schemas:
    User:
      type: object
      properties:
        id: {type: string}
        username: {type: string}
        email: {type: string, format: email}
        display_name: {type: string}
        role: {type: string, enum: [participant, organizer, admin]}
        created_at: {type: string, format: date-time}
        updated_at: {type: string, format: date-time}
    UserCreate:
      type: object
      required: [username, email]
      properties:
        username: {type: string}
        email: {type: string, format: email}
        display_name: {type: string}
        role: {type: string, enum: [participant, organizer, admin]}
    # ... 其他 schemas
```

---

### 阶段 2: 后端代码生成

#### 2.1 使用 api-builder 生成后端

**前提**: 已使用 schema-to-openapi 生成 OpenAPI 规范

```bash
# 从生成的 OpenAPI 规范创建后端
cd .claude/skills/api-builder/scripts

python cli.py \
  --spec ../../../.synnovator/openapi.yaml \
  --output ../../../backend \
  --setup-alembic \
  --run-migrations

# 或使用自定义规范路径
python cli.py \
  --spec ../../../specs/synnovator-api.yaml \
  --output ../../../backend \
  --setup-alembic \
  --run-migrations
```

**生成内容：**

```
backend/
├── models/               # SQLAlchemy ORM 模型
│   ├── __init__.py
│   ├── user.py
│   ├── category.py
│   ├── post.py
│   └── ...
├── schemas/              # Pydantic 验证 schemas
│   ├── __init__.py
│   ├── user.py
│   ├── category.py
│   └── ...
├── routers/              # FastAPI 路由
│   ├── __init__.py
│   ├── users.py
│   ├── categories.py
│   └── ...
├── crud/                 # CRUD 操作
│   ├── __init__.py
│   ├── base.py
│   └── user.py
├── tests/                # pytest 测试
│   ├── conftest.py
│   ├── test_api/
│   └── test_crud/
├── alembic/              # 数据库迁移
│   ├── versions/
│   └── env.py
├── main.py               # FastAPI 应用入口
├── database.py           # 数据库配置
└── alembic.ini           # Alembic 配置
```

#### 2.2 验证生成的代码

```bash
cd backend

# 查看数据库表
sqlite3 data/synnovator.db ".tables"

# 预期输出: user category post rule resource group interaction ...

# 运行类型检查
mypy app/

# 启动开发服务器
uvicorn app.main:app --reload
```

访问 http://localhost:8000/docs 查看 Swagger API 文档。

#### 2.3 补充业务逻辑

生成的代码包含 TODO 注释，标记需要补充的部分：

```python
# backend/routers/users.py
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # TODO: 添加业务逻辑
    # - 验证用户名/邮箱唯一性
    # - 密码哈希
    # - 发送欢迎邮件
    return crud_user.create(db, user)
```

补充要点：
- 认证/授权逻辑（JWT、OAuth）
- 业务验证规则
- 错误处理
- 日志记录

---

### 阶段 3: 数据注入

#### 3.1 使用 data-importer 导入测试数据

```bash
cd .claude/skills/data-importer/scripts

# 导入所有数据
python cli.py import \
  --source ../../../.synnovator \
  --db ../../../backend/data/synnovator.db \
  --models ../../../backend/models

# 只导入特定类型
python cli.py import \
  --source ../../../.synnovator \
  --db ../../../backend/data/synnovator.db \
  --models ../../../backend/models \
  --types user,post,category
```

**导入过程：**
1. 解析 `.synnovator/*.md` 文件（YAML frontmatter + Markdown body）
2. 按依赖顺序导入：
   - Phase 1: user, category, rule
   - Phase 2: group, post, resource
   - Phase 3: interaction
   - Phase 4: 所有关系类型
3. 自动类型转换（datetime, JSON, enum）
4. 跳过已存在记录（基于 ID）
5. 生成导入报告

#### 3.2 验证导入结果

```bash
# 查看导入的数据
sqlite3 backend/data/synnovator.db << EOF
SELECT COUNT(*) FROM user;
SELECT COUNT(*) FROM post;
SELECT COUNT(*) FROM category;
SELECT * FROM user LIMIT 3;
EOF
```

#### 3.3 数据更新流程

**场景 1: 添加新的测试数据**

```bash
# 1. 使用 synnovator engine 创建新数据
python .claude/skills/synnovator/scripts/engine.py \
  --user user_xxx create post \
  --data '{"title": "New Post", "type": "general"}' \
  --body "New content..."

# 2. 重新导入（增量模式，自动跳过已存在记录）
python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator \
  --db backend/data/synnovator.db \
  --models backend/models
```

**场景 2: 更新现有数据**

```bash
# 1. 使用 synnovator engine 更新
python .claude/skills/synnovator/scripts/engine.py \
  update post --id post_xxx \
  --data '{"status": "published"}'

# 2. 清空数据库重新导入
rm backend/data/synnovator.db
cd backend && alembic upgrade head
cd ..
python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator \
  --db backend/data/synnovator.db \
  --models backend/models
```

---

### 阶段 4: 前端开发

前端开发分为 7 个子步骤，从设计稿到可测试的完整页面。

```
.pen 设计稿 → React 组件 → 路由配置 → API 客户端 → API 对接 → 交互验证 → 测试
```

#### 4.1 生成 UI 设计稿 (.pen)

使用 **pen-page-gen skill** 从后端 router 自动生成页面布局规范。

```bash
# 输入: 后端 router 文件
# 输出: specs/ui/components/*.pen
```

也可手工编写 `.pen` 文件。设计稿需遵循 `specs/ui/style.pen` 定义的设计系统（Neon Forge 主题）。

**当前项目 .pen 文件：**

```
specs/ui/
├── style.pen                    # 全局样式规范（颜色、字体、间距）
├── basic.pen                    # 基础 UI 组件规范
└── components/
    ├── home.pen                 # 首页
    ├── post-list.pen            # 帖子列表
    ├── post-detail.pen          # 帖子详情
    ├── proposal-list.pen        # 提案列表
    ├── proposal-detail.pen      # 提案详情
    ├── category-detail.pen      # 活动详情
    ├── user-profile.pen         # 用户主页
    ├── team.pen                 # 团队页
    ├── following-list.pen       # 关注列表
    └── assets.pen               # 我的资产
```

**验收标准：** 每个页面有对应的 `.pen` 文件，包含布局、组件层级、文案和样式标注。

#### 4.2 生成 React 组件

使用 **pen-to-react skill** 将 `.pen` 转换为 React 组件。

```bash
# 输入: specs/ui/components/*.pen + specs/ui/style.pen
# 输出: components/pages/*.tsx + components/ui/*.tsx
```

**生成结果：**

```
frontend/
├── components/
│   ├── ui/             # shadcn/ui 基础组件（Button, Card, Badge, Tabs...）
│   └── pages/          # 页面级组件（纯展示，使用 mock 数据）
│       ├── home.tsx
│       ├── post-list.tsx
│       ├── post-detail.tsx
│       ├── proposal-list.tsx
│       ├── proposal-detail.tsx
│       ├── category-detail.tsx
│       ├── user-profile.tsx
│       ├── team.tsx
│       ├── following-list.tsx
│       └── assets.tsx
```

**验收标准：**
- 每个 `.pen` 文件有对应的 `.tsx` 组件
- 组件使用 shadcn/ui 基础组件 + Tailwind CSS
- 组件内使用硬编码 mock 数据（此阶段不接 API）
- `npm run build` 编译通过

#### 4.3 路由配置

为每个页面组件创建 Next.js App Router 路由页面。

```
frontend/app/
├── layout.tsx                    # 根布局
├── page.tsx                      # / → Home
├── posts/
│   ├── page.tsx                  # /posts → PostList
│   └── [id]/page.tsx             # /posts/:id → PostDetail
├── proposals/
│   ├── page.tsx                  # /proposals → ProposalList
│   └── [id]/page.tsx             # /proposals/:id → ProposalDetail
├── categories/
│   └── [id]/page.tsx             # /categories/:id → CategoryDetail
├── profile/page.tsx              # /profile → UserProfile
├── team/page.tsx                 # /team → Team
├── following/page.tsx            # /following → FollowingList
└── assets/page.tsx               # /assets → Assets
```

路由页面是薄层包装，仅导入并渲染对应的页面组件：

```typescript
// app/posts/page.tsx
import { PostList } from "@/components/pages/post-list"
export default function PostsPage() {
  return <PostList />
}
```

**验收标准：**
- 每个路由页面能独立访问，不抛异常
- `npm run build` 编译通过，所有页面 SSG/SSR 正常

#### 4.4 生成 API 客户端

使用 **api-builder skill** 从 OpenAPI 规范生成 TypeScript API 客户端。

```bash
cd .claude/skills/api-builder/scripts

python cli.py \
  --spec ../../../specs/synnovator-api.yaml \
  --output ../../../backend \
  --generate-client \
  --client-output ../../../frontend/utils/api-client.ts
```

**生成内容：**

```
frontend/utils/
├── utils.ts             # cn() 工具函数
└── api-client.ts        # 自动生成的 API 客户端
    ├── 类型定义          # 从 OpenAPI schemas 生成
    ├── API 方法          # 从 OpenAPI paths 生成
    └── 错误处理          # 统一异常处理
```

**配置环境变量：**

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**验收标准：**
- `api-client.ts` 包含所有后端 endpoint 对应的 TypeScript 方法
- 类型定义与后端 Pydantic schema 一致
- TypeScript 类型检查通过

#### 4.5 API 对接

将页面组件从 mock 数据切换到真实 API 调用。**逐页面改造**，每完成一个页面立即验证。

**改造模式：**

| 数据场景 | 实现方式 |
|----------|----------|
| 页面初始数据加载 | Server Component 直接 `await apiClient.listXxx()` |
| 用户触发的操作（提交、点赞等） | Client Component + `useState` + `apiClient.createXxx()` |
| 列表分页/筛选 | Client Component + `useEffect` + URL 参数 |

**Server Component 示例（列表页）：**

```typescript
// app/posts/page.tsx
import { apiClient } from '@/utils/api-client';
import { PostList } from "@/components/pages/post-list"

export default async function PostsPage() {
  const posts = await apiClient.listPosts();
  return <PostList posts={posts} />
}
```

**Client Component 示例（交互操作）：**

```typescript
// components/pages/post-detail.tsx
'use client';
import { apiClient } from '@/utils/api-client';

export function PostDetail({ post }: { post: Post }) {
  const handleLike = async () => {
    await apiClient.createInteraction({
      target_type: 'post',
      target_id: post.id,
      type: 'like',
    });
  };
  // ...
}
```

**改造顺序（按依赖关系）：**
1. 首页 (home) — 聚合数据，最后改造
2. 列表页 (post-list, proposal-list, following-list, assets)
3. 详情页 (post-detail, proposal-detail, category-detail)
4. 个人页 (user-profile, team)

**验收标准：**
- 每个页面使用真实 API 数据渲染
- 启动 `FastAPI + Next.js` 后，页面正常显示
- 网络请求无 4xx/5xx 错误

#### 4.6 交互与导航验证

验证所有页面间的跳转和用户交互是否正常工作。

**导航验证清单：**

| 起始页 | 操作 | 目标页 |
|--------|------|--------|
| 首页 | 点击帖子卡片 | /posts/:id |
| 首页 | 点击提案卡片 | /proposals/:id |
| 首页 | 点击「发布新内容」 | 发布页/弹窗 |
| 帖子列表 | 点击帖子 | /posts/:id |
| 提案列表 | 点击提案 | /proposals/:id |
| 提案详情 | 点击「返回提案广场」 | /proposals |
| 提案详情 | 点击「查看团队」 | /team |
| 用户主页 | 点击「关注」按钮 | 触发关注 API |
| 活动详情 | 切换 Tabs | 面板内容切换 |
| 侧边栏 | 点击「探索/星球/营地」 | 页面切换 |

**交互验证清单：**

| 组件 | 交互行为 | 预期结果 |
|------|----------|----------|
| Header 搜索框 | 输入关键词 | 触发搜索/跳转 |
| 「发布新内容」按钮 | 点击 | 打开发布流程 |
| Tab 组件 | 切换 tab | 显示对应面板内容 |
| 点赞按钮 | 点击 | 调用 API + 更新计数 |
| 评论输入 | 提交 | 调用 API + 刷新列表 |
| 分页/加载更多 | 滚动/点击 | 加载下一页数据 |

**验收标准：**
- 所有页面间跳转使用 `next/link`（客户端导航，无整页刷新）
- 动态路由参数 `[id]` 正确传递
- 表单提交后有成功/失败反馈
- Tab 切换正常，默认选中正确

#### 4.7 前端测试

##### 4.7.1 单元测试（Jest + React Testing Library）

验证组件能正常渲染、关键文本和结构存在。

```bash
cd frontend && npm test
```

**测试结构：**

```
frontend/__tests__/
├── components/        # 页面组件测试（每个组件一个文件）
│   ├── home.test.tsx
│   ├── post-list.test.tsx
│   ├── post-detail.test.tsx
│   ├── proposal-list.test.tsx
│   ├── proposal-detail.test.tsx
│   ├── category-detail.test.tsx
│   ├── user-profile.test.tsx
│   ├── team.test.tsx
│   ├── following-list.test.tsx
│   └── assets.test.tsx
└── pages/
    └── routes.test.tsx  # 路由页面统一渲染测试
```

**每个组件测试覆盖：**
- 组件能正常渲染（不抛异常）
- 关键文本存在（页面标题、按钮文字）
- 关键结构存在（header、sidebar、main content）

##### 4.7.2 E2E 测试（Playwright）

验证完整的用户旅程，对照 `docs/user-journey.md` 中的 13 个场景。

```bash
cd frontend && npx playwright test
```

**E2E 测试覆盖（按 user-journey.md 顺序）：**

| 测试文件 | 对应用户旅程 | 核心验证 |
|----------|-------------|----------|
| `browse.spec.ts` | #2 浏览探索页 | 首页渲染、卡片展示、Tab 切换 |
| `posts.spec.ts` | #9 发送帖子 | 帖子列表 → 详情 → 创建 |
| `proposals.spec.ts` | — | 提案列表 → 详情 → 标签/Tab |
| `category.spec.ts` | #6 创建活动, #7 加入活动 | 活动详情 → Tab 切换 |
| `team.spec.ts` | #8 创建团队 | 团队页 → 成员 → 资产 |
| `profile.spec.ts` | — | 用户主页 → 关注 → Tab |
| `navigation.spec.ts` | — | 跨页面跳转完整验证 |

**验收标准：**
- `npm test` — 全部单元测试通过
- `npx playwright test` — 全部 E2E 测试通过
- `npm run build` — 生产构建正常

---

### 阶段 5: 测试与验证

#### 5.1 后端单元测试

```bash
cd backend

# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_api/test_users_api.py -v

# 测试覆盖率
pytest tests/ --cov=app --cov-report=html
```

生成的测试包括：

```python
# tests/test_api/test_users_api.py
def test_create_user(client):
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_list_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_not_found(client):
    response = client.get("/users/nonexistent")
    assert response.status_code == 404
```

#### 5.2 API 集成测试

使用 curl 或 httpie 测试 API：

```bash
# 启动服务器
uvicorn app.main:app --reload &

# 测试 API
curl http://localhost:8000/users
curl http://localhost:8000/users/user_alice
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "charlie", "email": "charlie@example.com"}'

# 查看 Swagger 文档
open http://localhost:8000/docs
```

#### 5.3 前端测试（使用 Playwright）

```bash
cd frontend

# 安装 Playwright
npm install -D @playwright/test
npx playwright install

# 创建测试
mkdir -p tests
cat > tests/users.spec.ts << 'EOF'
import { test, expect } from '@playwright/test';

test('list users', async ({ page }) => {
  await page.goto('http://localhost:3000/users');
  await expect(page.locator('h1')).toContainText('Users');
  await expect(page.locator('li')).toHaveCount(2); // alice, bob
});

test('create user', async ({ page }) => {
  await page.goto('http://localhost:3000/users/create');
  await page.fill('input[placeholder="Username"]', 'charlie');
  await page.fill('input[placeholder="Email"]', 'charlie@example.com');
  await page.click('button[type="submit"]');
  await expect(page.locator('text=User created')).toBeVisible();
});
EOF

# 运行测试
npx playwright test
```

#### 5.4 端到端测试流程

**完整的用户旅程测试：**

1. 启动服务
2. 导入测试数据
3. 测试 API endpoints
4. 测试前端集成
5. 验证数据一致性

```bash
# 启动后端
cd backend && uvicorn app.main:app --reload &

# 启动前端
cd frontend && npm run dev &

# 导入测试数据
python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator --db backend/data/synnovator.db --models backend/models

# 运行后端测试
cd backend && pytest tests/ -v

# 运行前端测试
cd frontend && npx playwright test

# 手动验证
open http://localhost:3000
open http://localhost:8000/docs
```

---

## 数据模型更新流程

### 场景 1: 添加新字段

```bash
# 1. 更新 docs/command.md（数据模型定义）

# 2. 重新生成 OpenAPI spec
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py

# 3. 重新生成后端代码
cd .claude/skills/api-builder/scripts
python cli.py --spec ../../../.synnovator/openapi.yaml --output ../../../backend

# 4. 生成数据库迁移
cd ../../../backend
alembic revision --autogenerate -m "Add new field"
alembic upgrade head

# 5. 更新 .synnovator 测试数据
python .claude/skills/synnovator/scripts/engine.py update user --id user_xxx --data '{"new_field": "value"}'

# 6. 重新导入数据
python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator --db backend/data/synnovator.db --models backend/models

# 7. 运行测试
cd backend && pytest tests/ -v
```

### 场景 2: 添加新的内容类型

```bash
# 1. 更新 docs/command.md
# 2. 重新生成 OpenAPI spec
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py
# 3. 重新生成后端
cd .claude/skills/api-builder/scripts
python cli.py --spec ../../../.synnovator/openapi.yaml --output ../../../backend
# 4. 更新 data-importer（在 IMPORT_ORDER 中添加新类型）
# 5. 创建测试数据
# 6. 导入并测试
```

### 场景 3: 修改关系类型

```bash
# 1. 更新 docs/command.md
# 2. 重新生成 OpenAPI spec
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py
# 3. 重新生成后端
cd .claude/skills/api-builder/scripts
python cli.py --spec ../../../.synnovator/openapi.yaml --output ../../../backend
# 4. 生成迁移（可能需要手动调整）
cd ../../../backend && alembic revision --autogenerate -m "Update relations"
alembic upgrade head
# 5. 更新测试数据
# 6. 重新导入
python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator --db data/synnovator.db --models models
```

---

## 常见问题

### Q: 如何清空数据库重新开始？

```bash
rm backend/data/synnovator.db
cd backend && alembic upgrade head
python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator --db backend/data/synnovator.db --models backend/models
```

### Q: 数据导入失败怎么办？

1. 查看错误报告
2. 验证 .md 文件格式
3. 检查外键依赖
4. 使用 `--types` 单独导入失败的类型

### Q: 如何添加认证？

```python
# backend/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # TODO: 验证 token
    return user

# backend/routers/users.py
@router.get("/me")
def get_current_user_info(user: User = Depends(get_current_user)):
    return user
```

### Q: 如何处理文件上传？

```python
# backend/routers/resources.py
from fastapi import File, UploadFile

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 保存文件
    contents = await file.read()
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)

    # 创建 resource 记录
    resource = crud_resource.create(db, {
        "filename": file.filename,
        "mime_type": file.content_type,
        "size": len(contents),
        "url": file_path
    })
    return resource
```

---

## 最佳实践

### 1. 数据一致性
- 优先在 `.synnovator/` 中维护测试数据
- 使用 data-importer 同步到数据库
- 避免直接修改数据库

### 2. 版本控制
- `.synnovator/` 纳入 Git
- `backend/data/*.db` 添加到 .gitignore
- 迁移文件纳入版本控制

### 3. 增量开发
- 设计 → 生成 → 导入 → 测试
- 每次迭代只修改必要部分
- 保持数据与 schema 同步

### 4. 测试策略
- 使用真实的 .synnovator 数据
- 编写 API 集成测试
- 测试外键约束和级联删除

### 5. 环境隔离
- 开发环境: SQLite
- 测试环境: SQLite（独立数据库）
- 生产环境: PostgreSQL/MySQL

---

## 技术栈总结

### 后端
- **语言**: Python 3.12+
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **数据库**: SQLite（开发）/ PostgreSQL（生产）
- **迁移**: Alembic
- **验证**: Pydantic
- **测试**: pytest, httpx
- **包管理**: uv

### 前端
- **框架**: Next.js 14 (App Router)
- **语言**: TypeScript
- **UI 组件**: shadcn/ui + Radix UI + Tailwind CSS v4
- **设计规范**: .pen 文件 (Neon Forge 主题)
- **API 客户端**: 自动生成（TypeScript，从 OpenAPI）
- **单元测试**: Jest + React Testing Library + @swc/jest
- **E2E 测试**: Playwright
- **包管理**: npm

### 工具链
- **synnovator**: 文件数据管理（CRUD 操作）
- **schema-to-openapi**: 从 Synnovator 数据模型生成 OpenAPI 3.0 规范
- **api-builder**: 后端代码生成（FastAPI + SQLAlchemy + Alembic + 测试 + TypeScript 客户端）
- **data-importer**: 数据导入（.synnovator → SQLite）

---

## 总结

完整开发流程 7 个阶段：

0. **项目初始化** - 创建结构、配置环境
1. **需求设计** - 定义 schema、创建示例数据、生成 OpenAPI spec
2. **后端生成** - 使用 api-builder 生成 FastAPI + 迁移
3. **数据注入** - 使用 data-importer 导入测试数据
4. **前端集成** - 生成 TypeScript 客户端、集成到 Next.js
5. **测试验证** - 单元测试、集成测试、端到端测试

这个流程确保：
- ✅ 从设计到实现的一致性
- ✅ 自动化代码生成，减少重复工作
- ✅ 测试数据与生产 schema 同步
- ✅ 类型安全的全栈开发
- ✅ 快速迭代和验证
